#!/usr/bin/env python3
"""Dựng atlas runtime từ masters/ — tái tạo được, không dựng tay nữa.

Hợp đồng đặt tên: một atlas cho mỗi class, `<domain>_<class>_v01`.

    farm_crops_v01    masters/farm/crops/*/          cell 192
    farm_trees_v01    masters/farm/trees/*/          cell 256
    farm_aquatic_v01  masters/farm/aquatic-crops/*/  cell 192
    farm_soil_v01     masters/farm/soil/*.png        cell 192

Output theo layout sẵn có:
    runtime/<atlas>.json
    runtime/1x/<domain>/<class>/<atlas>.png

Nguyên tắc (xem báo cáo kèm PR để biết vì sao):
- Danh sách species/tile ĐỌC TỪ FILESYSTEM, sort alphabetical. Không hardcode.
- masterCanvas đọc từ chính file PNG, không hardcode theo bảng. Atlas trộn nhiều
  canvas (aquatic: lotus 1024, water-* 768) BẮT BUỘC có `masterCanvasBySpecies`
  để game bù được display-scale (§9.5) — cell giữ đồng nhất, tỷ lệ hiển thị
  tương đối do calibration của game lo, không phải việc của atlas.
- anchorX LUÔN = 0.5, không đo. Mọi pack master đã được căn về tâm canvas: nhóm
  thân đơn căn bottom-band về canvasW/2, nhóm rosette (culantro, mint,
  tonkin-jasmine, water-mimosa, water-spinach) căn bbox center về canvasW/2
  (§7.1). Bottom-band centroid đo được lệch tâm chỉ là artifact của heuristic
  trên morphology tán xoè — nó vẫn được đo và báo ở dòng `NOTE` như tín hiệu QC
  master, KHÔNG dùng làm anchor và KHÔNG làm fail build.
- anchorY = contactY / canvasH ĐO TỪ FILE (chính xác và nhất quán: 458/512,
  970/1024, 728/768). Ghi anchor cho TỪNG frame; `placementAnchor` là giá trị
  đại diện, kèm `anchorUniform` / `anchorSpread`.
- Frame key LUÔN là slot id `<species>_stage-0N` cho mọi atlas có stage, kể cả
  khi nhãn semantic trùng nhau — game truy cập đồng nhất, không phải tra bảng.
  Nhãn semantic (`berry`, `tapping`...) nằm ở `stageNames`, chỉ để hiển thị.
- Cùng một tile có nhiều version thì lấy version CAO NHẤT ĐỌC ĐƯỢC; version cao
  hơn nhưng hỏng thì tụt xuống và ghi rõ lý do. Không version nào đọc được ->
  FAIL cả build, không im lặng bỏ qua.
- Idempotent: chạy 2 lần ra byte y hệt nhau. Build fail thì không ghi gì.

Usage:
    python3 tools/build_atlas.py --dry-run
    python3 tools/build_atlas.py --atlas farm_soil_v01
"""
import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image  # noqa: E402

import normalize_pack  # noqa: E402  (tái dùng measure(), không copy code)

# --- hằng số hợp đồng ------------------------------------------------------
MASTERS_DIR = 'masters'
RUNTIME_DIR = 'runtime'
SCALE_DIR = '1x'
PNG_EXT = '.png'
ANCHOR_PRECISION = 6
ANCHOR_X = 0.5  # master đã căn tâm canvas -> anchorX là hằng số, không đo
MAX_TEXTURE_PX = 4096
CENTROID_QC_PX = 2.0  # centroid lệch tâm quá ngần này (px trong cell) thì ghi NOTE
FORMAT_TEMPLATE = 'mayhoa-{name}-atlas-v1'
VERSION_RE = re.compile(r'^(?P<stem>.+)_v(?P<version>\d+)$')
STAGE_RE = re.compile(r'stage-\d+')
STAGE_LABEL_RE = re.compile(r'^stage-\d+_(?P<label>.+)$')
UNVERSIONED = 0


@dataclass(frozen=True)
class AtlasSpec:
    """Khai báo 1 atlas: nguồn master, kích thước cell, key entity trong JSON."""

    atlas: str
    domain: str
    cls: str
    source: str          # đường dẫn tương đối trong masters/
    cell: int
    entity_key: str      # key chứa danh sách species/tile trong JSON
    staged: bool         # True = mỗi species 1 thư mục 5 stage


ATLAS_SPECS = (
    AtlasSpec('farm_crops_v01', 'farm', 'crops', 'farm/crops', 192, 'crops', True),
    AtlasSpec('farm_trees_v01', 'farm', 'trees', 'farm/trees', 256, 'trees', True),
    AtlasSpec('farm_aquatic_v01', 'farm', 'aquatic', 'farm/aquatic-crops', 192,
              'aquatic', True),
    AtlasSpec('farm_soil_v01', 'farm', 'soil', 'farm/soil', 192, 'tiles', False),
)


class AtlasBuildError(Exception):
    """Lỗi làm hỏng cả build — luôn phải nổ ra ngoài, không nuốt."""


@dataclass(frozen=True)
class Candidate:
    """Một file master ứng viên cho 1 tile/stage, kèm số version."""

    path: str
    version: int


@dataclass(frozen=True)
class Pick:
    """Version được chọn + số đo, kèm lý do loại các version cao hơn."""

    path: str
    version: int
    canvas: tuple
    root_x: float
    contact_y: int
    mode: str
    rejected: tuple = ()

    @property
    def anchor(self):
        """anchorX pin 0.5 (theo normalize), anchorY đo từ contactY của file."""
        return (ANCHOR_X, round(self.contact_y / self.canvas[1], ANCHOR_PRECISION))

    @property
    def measured_x(self):
        """rootX chuẩn hoá ĐO ĐƯỢC — chỉ dùng cho QC, không dùng làm anchor."""
        return round(self.root_x / self.canvas[0], ANCHOR_PRECISION)


@dataclass(frozen=True)
class Frame:
    """Một ô trong atlas."""

    key: str
    species: str
    stage: Optional[str]   # nhãn semantic ('berry'), None với atlas không stage
    col: int
    row: int
    x: int
    y: int
    path: str
    canvas: tuple
    anchor: tuple
    measured_x: float      # centroid đo được, chỉ để QC


@dataclass(frozen=True)
class AtlasPlan:
    """Kế hoạch đầy đủ của 1 atlas — đủ để render và sinh JSON, chưa ghi gì."""

    spec: AtlasSpec
    species: tuple
    stage_slots: tuple
    stage_names: dict
    canvases: dict
    frames: tuple
    cols: int
    rows: int
    warnings: tuple = ()   # vấn đề thật sự của build
    notes: tuple = ()      # tín hiệu QC master, không làm fail build

    @property
    def tex_w(self):
        return self.cols * self.spec.cell

    @property
    def tex_h(self):
        return self.rows * self.spec.cell


# --- tra cứu spec ----------------------------------------------------------
def spec_by_name(atlas):
    """Trả về AtlasSpec theo tên atlas, raise nếu không có trong hợp đồng."""
    for spec in ATLAS_SPECS:
        if spec.atlas == atlas:
            return spec
    known = ', '.join(s.atlas for s in ATLAS_SPECS)
    raise AtlasBuildError(f"atlas không có trong hợp đồng: {atlas} (biết: {known})")


# --- chọn version ----------------------------------------------------------
def split_version(filename):
    """'soil_tilled_v02.png' -> ('soil_tilled', 2); không có _vNN -> version 0."""
    stem = os.path.splitext(os.path.basename(filename))[0]
    match = VERSION_RE.match(stem)
    if not match:
        return stem, UNVERSIONED
    return match.group('stem'), int(match.group('version'))


def group_versions(paths):
    """Gom các path theo stem, mỗi stem là tuple Candidate sort version giảm dần."""
    buckets = {}
    for path in paths:
        stem, version = split_version(path)
        buckets.setdefault(stem, []).append(Candidate(path, version))
    return {stem: tuple(sorted(items, key=lambda c: (-c.version, c.path)))
            for stem, items in buckets.items()}


def probe_master(path):
    """Đọc + đo 1 master. Raise AtlasBuildError nếu file không dùng được."""
    try:
        with Image.open(path) as src:
            mode = src.mode
            img = src.convert('RGBA')
    except (OSError, ValueError, SyntaxError) as err:
        raise AtlasBuildError(f"không đọc được ({err})") from err
    try:
        measured = normalize_pack.measure(img)
    except ValueError as err:
        raise AtlasBuildError(f"không đo được ({err})") from err
    finally:
        canvas = img.size
        img.close()
    return Pick(path=path, version=split_version(path)[1], canvas=canvas,
                root_x=measured['root_x'], contact_y=measured['contact_y'],
                mode=mode)


def pick_readable_version(candidates):
    """Lấy version cao nhất ĐỌC ĐƯỢC. Không có cái nào -> AtlasBuildError."""
    if not candidates:
        raise AtlasBuildError('không có file ứng viên nào')
    rejected = []
    for cand in candidates:
        try:
            pick = probe_master(cand.path)
        except AtlasBuildError as err:
            rejected.append(f'{os.path.basename(cand.path)}: {err}')
            continue
        return Pick(path=pick.path, version=cand.version, canvas=pick.canvas,
                    root_x=pick.root_x, contact_y=pick.contact_y, mode=pick.mode,
                    rejected=tuple(rejected))
    stem = split_version(candidates[0].path)[0]
    detail = '; '.join(rejected)
    raise AtlasBuildError(
        f"{stem}: không version nào đọc được ({len(candidates)} ứng viên) -> {detail}")


# --- quét filesystem -------------------------------------------------------
def list_pngs(directory):
    """Các file .png trực tiếp trong directory, sort theo tên."""
    return sorted(os.path.join(directory, n) for n in os.listdir(directory)
                  if n.lower().endswith(PNG_EXT) and not n.startswith('.'))


def list_species_dirs(directory):
    """Tên các thư mục species, sort alphabetical (đọc từ filesystem)."""
    return tuple(sorted(n for n in os.listdir(directory)
                        if not n.startswith('.')
                        and os.path.isdir(os.path.join(directory, n))))


def stage_token(stem, species):
    """'carrot_stage-01_seeded' + 'carrot' -> 'stage-01_seeded'. None nếu không rõ."""
    prefix = f'{species}_'
    if stem.startswith(prefix):
        return stem[len(prefix):]
    match = STAGE_RE.search(stem)
    return stem[match.start():] if match else None


def stage_slot(token):
    """'stage-04_flowering' -> 'stage-04'. None nếu token không phải stage."""
    match = STAGE_RE.match(token)
    return match.group(0) if match else None


def stage_label(token):
    """'stage-05_berry' -> 'berry'. None nếu token không có phần semantic."""
    match = STAGE_LABEL_RE.match(token)
    return match.group('label') if match else None


def grid_shape(count):
    """Lưới gần vuông cho atlas không có stage: cols = ceil(sqrt(n))."""
    if count <= 0:
        return 0, 0
    cols = math.ceil(math.sqrt(count))
    return cols, math.ceil(count / cols)


def size_warnings(atlas, width, height):
    """Cảnh báo nếu texture vượt giới hạn an toàn của GPU cũ."""
    if max(width, height) <= MAX_TEXTURE_PX:
        return ()
    return (f'{atlas}: texture {width}x{height} vượt {MAX_TEXTURE_PX}px '
            f'— nhiều thiết bị sẽ không nạp được',)


def centroid_qc_notes(atlas, cell, frames):
    """NOTE QC: bottom-band centroid của master lệch tâm canvas bao nhiêu.

    Đây KHÔNG phải lỗi build và không ảnh hưởng output: anchorX luôn ghi 0.5 vì
    mọi pack đã được căn tâm canvas. Nhưng với morphology rosette/tán xoè
    (culantro, mint, water-mimosa...) heuristic bottom-band centroid lệch đi
    đúng như §7.1 cảnh báo, nên số này hữu ích khi QC lại master.
    """
    by_species = {}
    for frame in frames:
        by_species.setdefault(frame.species, []).append(frame.measured_x)
    out = []
    for species in sorted(by_species):
        xs = by_species[species]
        offset = max(abs(x - ANCHOR_X) for x in xs) * cell
        if offset <= CENTROID_QC_PX:
            continue
        out.append(
            f'QC {atlas}: {species} bottom-band centroid lệch tâm canvas tối đa '
            f'{offset:.1f}px (x {min(xs):.4f}..{max(xs):.4f}) — heuristic §7.1 không '
            f'tin cậy cho morphology này; anchorX vẫn ghi {ANCHOR_X} theo normalize')
    return tuple(out)


def _with_diagnostics(plan, warnings=(), notes=()):
    """Trả về AtlasPlan mới có thêm warnings/notes (không mutate plan cũ)."""
    if not warnings and not notes:
        return plan
    return AtlasPlan(spec=plan.spec, species=plan.species, stage_slots=plan.stage_slots,
                     stage_names=plan.stage_names, canvases=plan.canvases,
                     frames=plan.frames, cols=plan.cols, rows=plan.rows,
                     warnings=plan.warnings + tuple(warnings),
                     notes=plan.notes + tuple(notes))


# --- lập kế hoạch ----------------------------------------------------------
def _collect_species_stages(src_dir, species, warnings):
    """Quét 1 thư mục species -> dict slot -> (token, Pick)."""
    sp_dir = os.path.join(src_dir, species)
    groups = group_versions(list_pngs(sp_dir))
    stages = {}
    for stem in sorted(groups):
        token = stage_token(stem, species)
        if token is None:
            warnings.append(f'{species}: bỏ qua {stem}{PNG_EXT} — không có stage-NN')
            continue
        if not stem.startswith(f'{species}_'):
            warnings.append(
                f'{species}: {stem}{PNG_EXT} không mang tên species (rename dở dang?)')
        slot = stage_slot(token)
        if slot is None:
            warnings.append(f'{species}: bỏ qua {stem}{PNG_EXT} — slot stage không hợp lệ')
            continue
        pick = pick_readable_version(groups[stem])
        _note_pick(species, pick, warnings)
        stages[slot] = (token, pick)
    return stages


def _note_pick(owner, pick, warnings):
    """Ghi lại mọi version bị loại và các vi phạm format vào warnings."""
    for reason in pick.rejected:
        warnings.append(f'{owner}: bỏ {reason} -> dùng {os.path.basename(pick.path)}')
    if pick.mode != 'RGBA':
        warnings.append(
            f'{owner}: {os.path.basename(pick.path)} là {pick.mode}, không phải RGBA8 (§6.3)')
    if pick.canvas[0] != pick.canvas[1]:
        warnings.append(
            f'{owner}: canvas {pick.canvas[0]}x{pick.canvas[1]} không vuông '
            f'— downscale về cell vuông sẽ méo')


def _plan_staged(spec, src_dir):
    """Kế hoạch cho atlas có stage: species = hàng, stage-NN = cột."""
    warnings = []
    species = list_species_dirs(src_dir)
    per_species = {sp: _collect_species_stages(src_dir, sp, warnings) for sp in species}
    species = tuple(sp for sp in species if per_species[sp])
    for sp in per_species:
        if not per_species[sp]:
            warnings.append(f'{spec.atlas}: species {sp} không có stage nào — bỏ khỏi atlas')
    if not species:
        raise AtlasBuildError(f'{spec.atlas}: không tìm thấy species nào dùng được trong {src_dir}')

    slots = tuple(sorted({slot for st in per_species.values() for slot in st}))
    frames = []
    stage_names = {}
    canvases = {}
    for row, sp in enumerate(species):
        stages = per_species[sp]
        stage_names[sp] = tuple(stage_label(stages[s][0]) if s in stages else None
                                for s in slots)
        canvases[sp] = stages[next(s for s in slots if s in stages)][1].canvas
        for col, slot in enumerate(slots):
            if slot not in stages:
                warnings.append(f'{spec.atlas}: {sp} thiếu {slot} — ô để trống')
                continue
            token, pick = stages[slot]
            frames.append(Frame(
                key=f'{sp}_{slot}', species=sp, stage=stage_label(token), col=col,
                row=row, x=col * spec.cell, y=row * spec.cell, path=pick.path,
                canvas=pick.canvas, anchor=pick.anchor, measured_x=pick.measured_x))
    return AtlasPlan(spec=spec, species=species, stage_slots=slots,
                     stage_names=stage_names, canvases=canvases,
                     frames=tuple(frames), cols=len(slots), rows=len(species),
                     warnings=tuple(warnings))


def _plan_flat(spec, src_dir):
    """Kế hoạch cho atlas không stage (soil): tile alphabetical trên lưới gần vuông."""
    warnings = []
    groups = group_versions(list_pngs(src_dir))
    names = tuple(sorted(groups))
    if not names:
        raise AtlasBuildError(f'{spec.atlas}: không tìm thấy tile nào trong {src_dir}')

    cols, rows = grid_shape(len(names))
    frames = []
    canvases = {}
    for index, name in enumerate(names):
        pick = pick_readable_version(groups[name])
        _note_pick(name, pick, warnings)
        canvases[name] = pick.canvas
        col, row = index % cols, index // cols
        frames.append(Frame(
            key=name, species=name, stage=None, col=col, row=row,
            x=col * spec.cell, y=row * spec.cell, path=pick.path,
            canvas=pick.canvas, anchor=pick.anchor, measured_x=pick.measured_x))
    return AtlasPlan(spec=spec, species=names, stage_slots=(), stage_names={},
                     canvases=canvases, frames=tuple(frames), cols=cols, rows=rows,
                     warnings=tuple(warnings))


def plan_atlas(spec, repo_root):
    """Dựng AtlasPlan cho 1 spec. Không đọc pixel màu, không ghi file."""
    src_dir = os.path.join(repo_root, MASTERS_DIR, *spec.source.split('/'))
    if not os.path.isdir(src_dir):
        raise AtlasBuildError(f'{spec.atlas}: thiếu thư mục nguồn {src_dir}')
    plan = _plan_staged(spec, src_dir) if spec.staged else _plan_flat(spec, src_dir)
    return _with_diagnostics(
        plan,
        warnings=size_warnings(spec.atlas, plan.tex_w, plan.tex_h),
        notes=centroid_qc_notes(spec.atlas, spec.cell, plan.frames))


# --- sinh metadata ---------------------------------------------------------
def _representative(values):
    """Giá trị xuất hiện nhiều nhất; hoà thì lấy nhỏ nhất (để deterministic)."""
    counts = Counter(values)
    top = max(counts.values())
    return min(v for v, c in counts.items() if c == top)


def _anchor_stats(anchors):
    """(anchor đại diện, đồng nhất?, spread x/y) của toàn bộ frame."""
    rep = _representative(anchors)
    xs = [a[0] for a in anchors]
    ys = [a[1] for a in anchors]
    spread = (round(max(xs) - min(xs), ANCHOR_PRECISION),
              round(max(ys) - min(ys), ANCHOR_PRECISION))
    return rep, len(set(anchors)) == 1, spread


def _stage_metadata(plan):
    """stageOrder luôn là slot id; stageNames giữ nhãn semantic để hiển thị.

    Không có nhánh đặc biệt cho trường hợp nhãn trùng nhau: game luôn dựng key
    `<species>_stage-0N` mà không cần tra bảng. Slot thiếu -> null, giữ chỉ số.
    """
    return {
        'stageOrder': list(plan.stage_slots),
        'stageNames': {sp: list(plan.stage_names[sp]) for sp in plan.species},
    }


def build_metadata(plan):
    """Sinh dict JSON theo schema của runtime/*.json hiện có."""
    spec = plan.spec
    cell = spec.cell
    anchors = [f.anchor for f in plan.frames]
    rep_anchor, uniform, spread = _anchor_stats(anchors)
    rep_canvas = _representative([plan.canvases[sp] for sp in plan.species])
    name = spec.atlas.rsplit('_v', 1)[0].replace('_', '-')

    meta = {
        'format': FORMAT_TEMPLATE.format(name=name),
        'image': '/'.join((SCALE_DIR, spec.domain, spec.cls, f'{spec.atlas}{PNG_EXT}')),
        'cellSize': {'w': cell, 'h': cell},
        'masterCanvas': {'w': rep_canvas[0], 'h': rep_canvas[1]},
    }
    if len(set(plan.canvases.values())) > 1:
        meta['masterCanvasBySpecies'] = {
            sp: {'w': plan.canvases[sp][0], 'h': plan.canvases[sp][1]}
            for sp in plan.species}
    meta['placementAnchor'] = {'x': rep_anchor[0], 'y': rep_anchor[1]}
    meta['anchorUniform'] = uniform
    meta['anchorSpread'] = {'x': spread[0], 'y': spread[1]}
    meta[spec.entity_key] = list(plan.species)
    if spec.staged:
        meta.update(_stage_metadata(plan))
    meta['frames'] = {
        f.key: {'x': f.x, 'y': f.y, 'w': cell, 'h': cell,
                'anchor': {'x': f.anchor[0], 'y': f.anchor[1]}}
        for f in plan.frames}
    return meta


# --- render & ghi ----------------------------------------------------------
def render_atlas(plan):
    """Compose sheet RGBA; ô trống để trong suốt; downscale bằng LANCZOS."""
    cell = plan.spec.cell
    sheet = Image.new('RGBA', (plan.tex_w, plan.tex_h), (0, 0, 0, 0))
    for frame in plan.frames:
        with Image.open(frame.path) as src:
            img = src.convert('RGBA')
        resized = img if img.size == (cell, cell) else img.resize((cell, cell), Image.LANCZOS)
        sheet.paste(resized, (frame.x, frame.y))
        img.close()
    return sheet


def output_paths(plan, repo_root):
    """(đường dẫn json, đường dẫn png) tuyệt đối của 1 atlas."""
    spec = plan.spec
    json_path = os.path.join(repo_root, RUNTIME_DIR, f'{spec.atlas}.json')
    png_path = os.path.join(repo_root, RUNTIME_DIR, SCALE_DIR, spec.domain, spec.cls,
                            f'{spec.atlas}{PNG_EXT}')
    return json_path, png_path


def write_atlas(plan, repo_root):
    """Ghi PNG + JSON. Cùng input -> cùng byte output (không nhúng timestamp)."""
    json_path, png_path = output_paths(plan, repo_root)
    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    render_atlas(plan).save(png_path, format='PNG')
    payload = json.dumps(build_metadata(plan), indent=2, ensure_ascii=False) + '\n'
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(payload)
    return json_path, png_path


# --- CLI -------------------------------------------------------------------
def describe(plan, repo_root):
    """Các dòng mô tả kế hoạch cho --dry-run."""
    spec = plan.spec
    rep_anchor, uniform, spread = _anchor_stats([f.anchor for f in plan.frames])
    unit = 'stage' if spec.staged else 'cột'
    json_path, png_path = output_paths(plan, repo_root)
    ys = sorted({f.anchor[1] for f in plan.frames})
    anchor_note = (f'x={ANCHOR_X} (pin), y={rep_anchor[1]} đồng nhất' if uniform else
                   f'x={ANCHOR_X} (pin), y PER-FRAME {ys[0]}..{ys[-1]} '
                   f'(đại diện {rep_anchor[1]}, spread {spread[1]})')
    canvases = sorted({c for c in plan.canvases.values()})
    canvas_note = ', '.join(f'{w}x{h}' for w, h in canvases)
    return [
        f'{spec.atlas}: {len(plan.species)} {spec.entity_key} x {plan.cols} {unit} '
        f'-> {plan.tex_w}x{plan.tex_h} px ({len(plan.frames)} frame, cell {spec.cell})',
        f'  master canvas: {canvas_note}',
        f'  anchor       : {anchor_note}',
        f'  json         : {os.path.relpath(json_path, repo_root)}',
        f'  png          : {os.path.relpath(png_path, repo_root)}',
    ]


def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--atlas', action='append', metavar='NAME',
                    help='chỉ dựng atlas này (lặp lại được); mặc định dựng tất cả')
    ap.add_argument('--repo-root', default=None,
                    help='gốc repo chứa masters/ và runtime/ (mặc định: repo của script)')
    ap.add_argument('--dry-run', action='store_true',
                    help='chỉ in kế hoạch, không ghi file nào')
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = args.repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    try:
        specs = ([spec_by_name(n) for n in args.atlas] if args.atlas else list(ATLAS_SPECS))
        plans = [plan_atlas(spec, repo_root) for spec in specs]
    except AtlasBuildError as err:
        print(f'ERROR {err}', file=sys.stderr)
        return 1

    for plan in plans:
        for line in describe(plan, repo_root):
            print(line)
        for warning in plan.warnings:
            print(f'  WARN {warning}')
        for note in plan.notes:
            print(f'  NOTE {note}')

    if args.dry_run:
        print('dry-run: không ghi file nào')
        return 0

    for plan in plans:
        json_path, png_path = write_atlas(plan, repo_root)
        print(f'wrote {os.path.relpath(json_path, repo_root)} '
              f'+ {os.path.relpath(png_path, repo_root)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
