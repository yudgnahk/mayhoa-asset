#!/usr/bin/env python3
"""Normalize master asset pack theo MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md.

Chỉ dùng transform được phép theo spec §12.1: uniform scale (LANCZOS) + translate
trên transparent canvas. Không đụng artwork.

Mode `root` (tree/perennial/aquatic):
    Đo root từng file (contactY = alpha bbox maxY; rootX = bottom-band centroid
    3%/min 8px, threshold alpha >= 24 — hoặc override bằng --rootx cho morphology
    radial §7.1), scale đồng nhất cả pack, translate để root về đúng target.

Mode `anchor` (crop soil-plate):
    Scale quanh fixed anchor (anchor giữ nguyên tọa độ), không translate theo
    contactY (spec §5.3).

Auto-scale = min các constraint để mọi pixel cách mép >= 24 px (safety 1 px),
không bao giờ tự upscale (cap 1.0). Override bằng --scale (cả pack) hoặc
--file-scale name=s (per-file, ví dụ coconut Profile B).

Usage:
    python3 tools/normalize_pack.py --mode root --canvas 1024 1024 \
        --target 512 970 masters/farm/trees/mango/*.png
    python3 tools/normalize_pack.py --mode anchor --canvas 512 512 \
        --target 256 350 masters/farm/crops/corn/*.png
"""
import argparse
import os
import sys

from PIL import Image

ALPHA_THRESHOLD = 24
MARGIN = 24
SAFETY = 1  # px cushion cho jitter khi resample


def alpha_mask(img):
    return img.getchannel('A').point(lambda v: 255 if v >= ALPHA_THRESHOLD else 0)


def measure(img):
    """Trả về dict bbox/contactY/rootX trên ảnh RGBA."""
    mask = alpha_mask(img)
    box = mask.getbbox()  # (l, t, r, b) exclusive
    if box is None:
        raise ValueError("empty alpha")
    minx, miny, maxx, maxy = box[0], box[1], box[2] - 1, box[3] - 1
    vis_h = maxy - miny + 1
    band = max(8, int(vis_h * 0.03))
    band_top = max(miny, maxy - band + 1)
    region = mask.crop((0, band_top, img.width, maxy + 1))
    data = region.getdata()
    w = img.width
    xs_sum = 0
    n = 0
    for i, v in enumerate(data):
        if v:
            xs_sum += i % w
            n += 1
    root_x = xs_sum / n
    return {
        'minx': minx, 'miny': miny, 'maxx': maxx, 'maxy': maxy,
        'vis_w': maxx - minx + 1, 'vis_h': vis_h,
        'contact_y': maxy, 'root_x': root_x,
    }


def scale_constraint(m, mode, canvas, target, root_x):
    """Scale tối đa để mọi extent quanh điểm cố định nằm trong margin."""
    cw, ch = canvas
    tx, ty = target
    lim_l = tx - MARGIN - SAFETY
    lim_r = (cw - 1 - MARGIN - SAFETY) - tx
    lim_t = ty - MARGIN - SAFETY
    lim_b = (ch - 1 - MARGIN - SAFETY) - ty
    if mode == 'root':
        # root nằm ở lowest pixel: toàn bộ content ở trên root
        ext = {
            'left': root_x - m['minx'],
            'right': m['maxx'] - root_x,
            'top': float(m['vis_h']),
            'bottom': 0.0,
        }
    else:
        ext = {
            'left': root_x - m['minx'],
            'right': m['maxx'] - root_x,
            'top': float(ty - m['miny']),
            'bottom': float(m['maxy'] - ty),
        }
    s = 1.0
    for key, lim in (('left', lim_l), ('right', lim_r), ('top', lim_t), ('bottom', lim_b)):
        if ext[key] > 0:
            s = min(s, lim / ext[key])
    return s


def normalize_file(path, mode, canvas, target, s, root_x_override):
    img = Image.open(path).convert('RGBA')
    m = measure(img)
    root_x = root_x_override if root_x_override is not None else m['root_x']

    new_size = (max(1, round(img.width * s)), max(1, round(img.height * s)))
    scaled = img.resize(new_size, Image.LANCZOS) if s != 1.0 or img.size != new_size else img
    ms = measure(scaled)

    tx, ty = target
    if mode == 'root':
        rx = root_x * s if root_x_override is not None else ms['root_x']
        off_x = round(tx - rx)
        off_y = ty - ms['contact_y']
    else:
        # anchor cố định: anchor nguồn (tx, ty) map về chính nó
        off_x = round(tx - tx * s)
        off_y = round(ty - ty * s)

    out = Image.new('RGBA', canvas, (0, 0, 0, 0))
    if (ms['minx'] + off_x < 0 or ms['maxx'] + off_x >= canvas[0]
            or ms['miny'] + off_y < 0 or ms['maxy'] + off_y >= canvas[1]):
        raise ValueError(f"{path}: content vượt canvas sau transform (scale {s:.4f})")
    out.paste(scaled, (off_x, off_y))

    fm = measure(out)
    out.save(path)
    margins = (fm['minx'], fm['miny'], canvas[0] - 1 - fm['maxx'], canvas[1] - 1 - fm['maxy'])
    print(
        f"{os.path.basename(path)}: s={s:.4f} -> contactY={fm['contact_y']} "
        f"rootX~{fm['root_x']:.1f} visW={fm['vis_w']} visH={fm['vis_h']} "
        f"margins L/T/R/B={margins[0]}/{margins[1]}/{margins[2]}/{margins[3]}"
    )
    return fm


def parse_kv(pairs, cast):
    out = {}
    for p in pairs or []:
        name, _, val = p.partition('=')
        out[name] = cast(val)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mode', choices=['root', 'anchor'], required=True)
    ap.add_argument('--canvas', nargs=2, type=int, required=True)
    ap.add_argument('--target', nargs=2, type=int, required=True)
    ap.add_argument('--scale', type=float, help='scale cố định cho cả pack (bỏ qua auto)')
    ap.add_argument('--file-scale', nargs='*', help='override per-file: basename=scale')
    ap.add_argument('--rootx', nargs='*', help='override rootX nguồn per-file: basename=x')
    ap.add_argument('files', nargs='+')
    args = ap.parse_args()

    canvas = tuple(args.canvas)
    target = tuple(args.target)
    file_scales = parse_kv(args.file_scale, float)
    rootx_over = parse_kv(args.rootx, float)

    # Pass 1: đo để tính auto-scale pack-wide
    metas = []
    pack_s = args.scale if args.scale else 1.0
    for path in args.files:
        img = Image.open(path).convert('RGBA')
        m = measure(img)
        rx = rootx_over.get(os.path.basename(path), m['root_x'])
        metas.append((path, m, rx))
        if not args.scale:
            pack_s = min(pack_s, scale_constraint(m, args.mode, canvas, target, rx))
    if not args.scale:
        print(f"auto pack scale = {pack_s:.4f}")

    # Pass 2: transform
    for path, m, rx in metas:
        base = os.path.basename(path)
        s = file_scales.get(base, pack_s)
        rxo = rootx_over.get(base)
        normalize_file(path, args.mode, canvas, target, s, rxo)
    return 0


if __name__ == '__main__':
    sys.exit(main())
