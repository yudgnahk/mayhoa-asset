#!/usr/bin/env python3
"""Test cho tools/build_atlas.py (chạy bằng unittest).

    python3 -m unittest discover -s tools -p 'test_*.py' -v

Fixture đều tự sinh trong tmpdir: test KHÔNG được phụ thuộc trạng thái thật của
masters/ (tên species đang bị đổi song song) và KHÔNG bao giờ ghi vào runtime/.

Trọng tâm:
- chọn đúng version cao nhất ĐỌC ĐƯỢC (v02 hỏng thì phải tụt về v01)
- không file nào đọc được -> FAIL to, không im lặng
- anchorX luôn pin 0.5 (master đã căn tâm canvas), anchorY đo từng file
- frame key luôn là slot id <species>_stage-0N, kèm stageNames cho nhãn semantic
- layout grid đúng ô, species đọc từ filesystem và sort alphabetical
- build 2 lần ra byte y hệt nhau
- --dry-run không ghi file nào
"""
import io
import json
import os
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build_atlas  # noqa: E402
from test_geometry_audit import _corrupt_idat_png, _rgba8_png  # noqa: E402

CELL = 'cellSize'
# Fixture nhỏ cho nhanh: _rgba8_png sinh pixel bằng vòng lặp Python thuần.
CANVAS = 64
BOX = (8, 8, 55, 57)  # rootX = 31.5, contactY = 57
FRAME_KEY_RE = re.compile(r'^[a-z-]+_stage-0[1-5]$')


def _write(path, blob):
    """Ghi blob ra path, tự tạo thư mục cha."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(blob)
    return path


def _stage_png(canvas, box):
    return _rgba8_png(canvas, canvas, box)


def _make_species(root, cls, species, stages, canvas, box, version='v01'):
    """Sinh 1 thư mục species với các file <sp>_<stage>_<version>.png."""
    base = os.path.join(root, 'masters', 'farm', cls, species)
    for stage in stages:
        _write(os.path.join(base, f'{species}_{stage}_{version}.png'),
               _stage_png(canvas, box))
    return base


def _capture(argv):
    """Chạy build_atlas.main(argv), trả về (status, stdout+stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        status = build_atlas.main(argv)
    return status, out.getvalue() + err.getvalue()


def _read_pair(root, atlas, spec_cls):
    """Đọc (json dict, png bytes) của 1 atlas đã build."""
    jpath = os.path.join(root, 'runtime', f'{atlas}.json')
    with open(jpath, encoding='utf-8') as f:
        meta = json.load(f)
    ppath = os.path.join(root, 'runtime', '1x', 'farm', spec_cls, f'{atlas}.png')
    with open(ppath, 'rb') as f:
        return meta, f.read()


CROP_STAGES = (
    'stage-01_seeded', 'stage-02_sprout', 'stage-03_young',
    'stage-04_mature', 'stage-05_harvestable',
)


class TestVersionSelection(unittest.TestCase):
    """Cùng 1 tile nhiều version: lấy version CAO NHẤT mà đọc được."""

    def _soil_root(self, tmp, files):
        for name, blob in files:
            _write(os.path.join(tmp, 'masters', 'farm', 'soil', name), blob)
        return tmp

    def test_picks_highest_version_when_all_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._soil_root(tmp, [
                ('soil_tilled_v01.png', _stage_png(64, (0, 0, 10, 10))),
                ('soil_tilled_v02.png', _stage_png(64, (0, 0, 20, 20))),
            ])
            pick = build_atlas.pick_readable_version(
                build_atlas.group_versions(
                    [os.path.join(tmp, 'masters', 'farm', 'soil', n)
                     for n in ('soil_tilled_v01.png', 'soil_tilled_v02.png')])['soil_tilled'])

        self.assertTrue(pick.path.endswith('soil_tilled_v02.png'))
        self.assertEqual(pick.version, 2)

    def test_falls_back_when_highest_version_corrupt(self):
        """soil_tilled_v01 hỏng trong repo thật -> phải chọn v02; đảo lại vẫn đúng."""
        with tempfile.TemporaryDirectory() as tmp:
            self._soil_root(tmp, [
                ('soil_tilled_v01.png', _stage_png(64, (0, 0, 10, 10))),
                ('soil_tilled_v02.png', _corrupt_idat_png()),
            ])
            paths = [os.path.join(tmp, 'masters', 'farm', 'soil', n)
                     for n in ('soil_tilled_v01.png', 'soil_tilled_v02.png')]
            pick = build_atlas.pick_readable_version(
                build_atlas.group_versions(paths)['soil_tilled'])

        self.assertEqual(pick.version, 1)
        self.assertTrue(any('v02' in r for r in pick.rejected),
                        'phải ghi lại lý do bỏ v02, không im lặng')

    def test_all_versions_unreadable_fails_loudly(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._soil_root(tmp, [
                ('soil_tilled_v01.png', _corrupt_idat_png()),
                ('soil_tilled_v02.png', _corrupt_idat_png()),
            ])
            paths = [os.path.join(tmp, 'masters', 'farm', 'soil', n)
                     for n in ('soil_tilled_v01.png', 'soil_tilled_v02.png')]
            with self.assertRaises(build_atlas.AtlasBuildError) as ctx:
                build_atlas.pick_readable_version(
                    build_atlas.group_versions(paths)['soil_tilled'])

        msg = str(ctx.exception)
        self.assertIn('soil_tilled', msg)
        self.assertIn('v01', msg)
        self.assertIn('v02', msg)

    def test_build_fails_when_a_tile_has_no_readable_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._soil_root(tmp, [
                ('soil_dry_v01.png', _stage_png(64, (0, 0, 10, 10))),
                ('soil_tilled_v01.png', _corrupt_idat_png()),
            ])
            status, out = _capture(['--repo-root', tmp, '--atlas', 'farm_soil_v01'])
            left_behind = os.path.exists(os.path.join(tmp, 'runtime'))

        self.assertEqual(status, 1, 'file hỏng phải làm build FAIL')
        self.assertIn('soil_tilled', out)
        self.assertFalse(left_behind, 'build fail thì không được để lại output nửa vời')


class TestAnchorFromMeasurement(unittest.TestCase):
    """anchorX = 0.5 theo normalize; anchorY = contactY/canvasH đo từng file."""

    def test_anchor_x_pinned_to_center_y_measured(self):
        canvas, box = CANVAS, BOX
        with tempfile.TemporaryDirectory() as tmp:
            _make_species(tmp, 'crops', 'carrot', CROP_STAGES, canvas, box)
            plan = build_atlas.plan_atlas(build_atlas.spec_by_name('farm_crops_v01'), tmp)

        frame = plan.frames[0]
        self.assertEqual(frame.anchor[0], build_atlas.ANCHOR_X)
        self.assertEqual(build_atlas.ANCHOR_X, 0.5)
        self.assertAlmostEqual(frame.anchor[1],
                               round(box[3] / canvas, build_atlas.ANCHOR_PRECISION),
                               places=6)

    def test_anchor_x_stays_center_even_when_centroid_drifts(self):
        """culantro/water-mimosa: bottom-band centroid lệch, anchorX vẫn phải 0.5."""
        with tempfile.TemporaryDirectory() as tmp:
            base = os.path.join(tmp, 'masters', 'farm', 'crops', 'culantro')
            for i, stage in enumerate(CROP_STAGES):
                _write(os.path.join(base, f'culantro_{stage}_v01.png'),
                       _stage_png(CANVAS, (8 + i * 4, 8, 40 + i * 4, 57)))
            plan = build_atlas.plan_atlas(build_atlas.spec_by_name('farm_crops_v01'), tmp)
            meta = build_atlas.build_metadata(plan)

        self.assertEqual({f.anchor[0] for f in plan.frames}, {0.5})
        self.assertEqual(meta['placementAnchor']['x'], 0.5)
        self.assertEqual(meta['anchorSpread']['x'], 0.0)
        for key, frame in meta['frames'].items():
            self.assertEqual(frame['anchor']['x'], 0.5, f'{key} lệch anchorX')

    def test_measured_centroid_is_kept_for_qc_even_though_unused(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_species(tmp, 'crops', 'carrot', CROP_STAGES, CANVAS, BOX)
            plan = build_atlas.plan_atlas(build_atlas.spec_by_name('farm_crops_v01'), tmp)

        expected = round(((BOX[0] + BOX[2]) / 2) / CANVAS, build_atlas.ANCHOR_PRECISION)
        self.assertAlmostEqual(plan.frames[0].measured_x, expected, places=6)

    def test_mixed_canvas_gives_different_anchors_per_frame(self):
        """farm_aquatic: lotus 1024, water-* 768 -> anchor KHÁC nhau."""
        stages = ('stage-01_planted', 'stage-02_sprout', 'stage-03_young',
                  'stage-04_mature', 'stage-05_harvestable')
        with tempfile.TemporaryDirectory() as tmp:
            _make_species(tmp, 'aquatic-crops', 'lotus', stages, 128, (8, 8, 119, 121))
            _make_species(tmp, 'aquatic-crops', 'water-mimosa', stages, 96, (8, 8, 87, 91))
            plan = build_atlas.plan_atlas(build_atlas.spec_by_name('farm_aquatic_v01'), tmp)
            meta = build_atlas.build_metadata(plan)

        anchors = {f.species: f.anchor for f in plan.frames}
        self.assertEqual({a[0] for a in anchors.values()}, {0.5})
        self.assertAlmostEqual(anchors['lotus'][1], round(121 / 128, 6), places=6)
        self.assertAlmostEqual(anchors['water-mimosa'][1], round(91 / 96, 6), places=6)
        self.assertNotEqual(anchors['lotus'][1], anchors['water-mimosa'][1])

        self.assertFalse(meta['anchorUniform'],
                         'anchor không đồng nhất thì JSON phải nói rõ')
        self.assertGreater(meta['anchorSpread']['y'], 0.0)
        self.assertIn('masterCanvasBySpecies', meta,
                      'canvas trộn thì phải ghi canvas theo từng species')
        for key, frame in meta['frames'].items():
            self.assertIn('anchor', frame, f'{key} thiếu anchor per-frame')

    def test_uniform_anchor_reported_as_uniform(self):
        with tempfile.TemporaryDirectory() as tmp:
            for sp in ('carrot', 'corn'):
                _make_species(tmp, 'crops', sp, CROP_STAGES, CANVAS, BOX)
            meta = build_atlas.build_metadata(
                build_atlas.plan_atlas(build_atlas.spec_by_name('farm_crops_v01'), tmp))

        self.assertTrue(meta['anchorUniform'])
        self.assertEqual(meta['anchorSpread'], {'x': 0.0, 'y': 0.0})
        self.assertNotIn('masterCanvasBySpecies', meta)


class TestGridLayout(unittest.TestCase):
    """Mỗi species 1 hàng, stage-01..05 là cột; species alphabetical."""

    def test_species_are_rows_and_stages_are_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            for sp in ('zucchini', 'carrot', 'mint'):
                _make_species(tmp, 'crops', sp, CROP_STAGES, CANVAS, BOX)
            meta = build_atlas.build_metadata(
                build_atlas.plan_atlas(build_atlas.spec_by_name('farm_crops_v01'), tmp))

        cell = meta[CELL]['w']
        self.assertEqual(meta['crops'], ['carrot', 'mint', 'zucchini'],
                         'species phải đọc từ filesystem và sort alphabetical')
        self.assertEqual(meta['frames']['carrot_stage-01']['x'], 0)
        self.assertEqual(meta['frames']['carrot_stage-01']['y'], 0)
        self.assertEqual(meta['frames']['carrot_stage-03']['x'], 2 * cell)
        self.assertEqual(meta['frames']['mint_stage-01']['y'], 1 * cell)
        self.assertEqual(meta['frames']['zucchini_stage-05'],
                         {'x': 4 * cell, 'y': 2 * cell, 'w': cell, 'h': cell,
                          'anchor': meta['placementAnchor']})

    def test_new_species_dir_is_picked_up_without_code_change(self):
        """Task đổi tên species chạy song song: tên MỚI phải tự vào atlas."""
        with tempfile.TemporaryDirectory() as tmp:
            _make_species(tmp, 'crops', 'tonkin-jasmine', CROP_STAGES, CANVAS, BOX)
            _make_species(tmp, 'crops', 'culantro', CROP_STAGES, CANVAS, BOX)
            meta = build_atlas.build_metadata(
                build_atlas.plan_atlas(build_atlas.spec_by_name('farm_crops_v01'), tmp))

        self.assertEqual(meta['crops'], ['culantro', 'tonkin-jasmine'])

    def test_texture_size_is_cols_x_rows_of_cell(self):
        with tempfile.TemporaryDirectory() as tmp:
            for sp in ('a-tree', 'b-tree'):
                _make_species(tmp, 'trees', sp,
                              ('stage-01_sprout', 'stage-02_sapling', 'stage-03_young',
                               'stage-04_flowering', 'stage-05_fruiting'),
                              CANVAS, BOX)
            plan = build_atlas.plan_atlas(build_atlas.spec_by_name('farm_trees_v01'), tmp)

        self.assertEqual((plan.tex_w, plan.tex_h), (5 * 256, 2 * 256))

    def test_soil_tiles_use_alphabetical_square_ish_grid(self):
        names = ('soil_dry', 'soil_empty', 'soil_harvested',
                 'soil_planted', 'soil_tilled', 'soil_wet')
        with tempfile.TemporaryDirectory() as tmp:
            for n in names:
                _write(os.path.join(tmp, 'masters', 'farm', 'soil', f'{n}_v01.png'),
                       _stage_png(CANVAS, BOX))
            meta = build_atlas.build_metadata(
                build_atlas.plan_atlas(build_atlas.spec_by_name('farm_soil_v01'), tmp))

        cell = meta[CELL]['w']
        self.assertEqual(meta['tiles'], list(names))
        self.assertNotIn('stageOrder', meta, 'soil không có stage')
        self.assertNotIn('stageNames', meta, 'soil không có stage')
        self.assertEqual(meta['frames']['soil_dry']['x'], 0)
        self.assertEqual(meta['frames']['soil_planted'], {
            'x': 0, 'y': cell, 'w': cell, 'h': cell,
            'anchor': meta['placementAnchor'],
        })
        self.assertEqual(meta['frames']['soil_wet']['x'], 2 * cell)

    def test_centroid_offset_is_reported_as_qc_note_not_warning(self):
        """§7.1: centroid lệch tâm là tín hiệu QC master, KHÔNG phải lỗi build."""
        with tempfile.TemporaryDirectory() as tmp:
            base = os.path.join(tmp, 'masters', 'farm', 'crops', 'culantro')
            for i, stage in enumerate(CROP_STAGES):
                # bbox trượt ngang dần theo stage -> bottom-band centroid lệch tâm
                _write(os.path.join(base, f'culantro_{stage}_v01.png'),
                       _stage_png(CANVAS, (8 + i * 4, 8, 40 + i * 4, 57)))
            plan = build_atlas.plan_atlas(build_atlas.spec_by_name('farm_crops_v01'), tmp)

        self.assertTrue(plan.notes, 'phải có note QC về centroid lệch tâm')
        self.assertIn('culantro', plan.notes[0])
        self.assertIn('QC', plan.notes[0])
        self.assertFalse([w for w in plan.warnings if 'centroid' in w],
                         'note QC không được lẫn vào warnings build')

    def test_centered_master_has_no_qc_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            # BOX đối xứng quanh tâm canvas 64 -> centroid = 31.5 ~ tâm
            _make_species(tmp, 'crops', 'carrot', CROP_STAGES, CANVAS, (8, 8, 55, 57))
            plan = build_atlas.plan_atlas(build_atlas.spec_by_name('farm_crops_v01'), tmp)

        self.assertFalse(plan.notes, f'master căn tâm không được sinh note: {plan.notes}')

    def test_oversize_texture_is_warned(self):
        plan_warnings = build_atlas.size_warnings('big_v01', 8192, 512)
        self.assertTrue(plan_warnings)
        self.assertIn('4096', plan_warnings[0])
        self.assertFalse(build_atlas.size_warnings('ok_v01', 1024, 1024))


class TestHeterogeneousStages(unittest.TestCase):
    """Tên stage-05 khác nhau giữa species (coffee=berry, rubber=tapping)."""

    def test_frame_keys_are_slot_ids_regardless_of_label(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_species(tmp, 'trees', 'coffee',
                          ('stage-01_sprout', 'stage-02_sapling', 'stage-03_young',
                           'stage-04_flowering', 'stage-05_berry'),
                          CANVAS, BOX)
            _make_species(tmp, 'trees', 'rubber',
                          ('stage-01_sprout', 'stage-02_sapling', 'stage-03_young',
                           'stage-04_mature', 'stage-05_tapping'),
                          CANVAS, BOX)
            meta = build_atlas.build_metadata(
                build_atlas.plan_atlas(build_atlas.spec_by_name('farm_trees_v01'), tmp))

        self.assertEqual(meta['stageOrder'],
                         ['stage-01', 'stage-02', 'stage-03', 'stage-04', 'stage-05'])
        self.assertEqual(meta['stageNames']['coffee'],
                         ['sprout', 'sapling', 'young', 'flowering', 'berry'])
        self.assertEqual(meta['stageNames']['rubber'],
                         ['sprout', 'sapling', 'young', 'mature', 'tapping'])
        self.assertIn('coffee_stage-05', meta['frames'])
        self.assertIn('rubber_stage-04', meta['frames'])
        self.assertNotIn('coffee_stage-05_berry', meta['frames'])
        for key in meta['frames']:
            self.assertRegex(key, FRAME_KEY_RE)

    def test_slot_ids_used_even_when_labels_match(self):
        """Không có nhánh đặc biệt: nhãn trùng nhau vẫn dùng slot id + stageNames."""
        with tempfile.TemporaryDirectory() as tmp:
            for sp in ('carrot', 'corn'):
                _make_species(tmp, 'crops', sp, CROP_STAGES, CANVAS, BOX)
            meta = build_atlas.build_metadata(
                build_atlas.plan_atlas(build_atlas.spec_by_name('farm_crops_v01'), tmp))

        self.assertEqual(meta['stageOrder'],
                         ['stage-01', 'stage-02', 'stage-03', 'stage-04', 'stage-05'])
        self.assertEqual(meta['stageNames']['carrot'],
                         ['seeded', 'sprout', 'young', 'mature', 'harvestable'])
        self.assertEqual(meta['stageNames']['corn'], meta['stageNames']['carrot'])
        self.assertNotIn('stageNamesBySpecies', meta)
        self.assertEqual(sorted(meta['frames']),
                         [f'{sp}_stage-0{i}' for sp in ('carrot', 'corn')
                          for i in range(1, 6)])

    def test_missing_stage_leaves_transparent_cell_and_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_species(tmp, 'crops', 'carrot', CROP_STAGES, CANVAS, BOX)
            _make_species(tmp, 'crops', 'corn', CROP_STAGES[:3], CANVAS, BOX)
            plan = build_atlas.plan_atlas(build_atlas.spec_by_name('farm_crops_v01'), tmp)
            meta = build_atlas.build_metadata(plan)
            sheet = build_atlas.render_atlas(plan)

        self.assertTrue(any('corn' in w and 'stage-04' in w for w in plan.warnings),
                        f'phải cảnh báo stage thiếu, warnings={plan.warnings}')
        self.assertNotIn('corn_stage-04', meta['frames'])
        self.assertIsNone(meta['stageNames']['corn'][3],
                          'stage thiếu phải là null trong stageNames, không tụt chỉ số')
        self.assertEqual(meta['stageNames']['corn'][:3], ['seeded', 'sprout', 'young'])
        cell = meta[CELL]['w']
        px = sheet.getpixel((3 * cell + cell // 2, cell + cell // 2))
        self.assertEqual(px[3], 0, 'ô trống phải trong suốt hoàn toàn')


class TestRenderAndWrite(unittest.TestCase):
    """Ảnh ra đúng kích thước/RGBA, ghi 2 lần byte y hệt, --dry-run không ghi."""

    def _one_crop_root(self, tmp):
        for sp in ('carrot', 'corn'):
            _make_species(tmp, 'crops', sp, CROP_STAGES, CANVAS, BOX)
        return tmp

    def test_rendered_sheet_is_rgba_and_correct_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = build_atlas.plan_atlas(
                build_atlas.spec_by_name('farm_crops_v01'), self._one_crop_root(tmp))
            sheet = build_atlas.render_atlas(plan)

        self.assertEqual(sheet.mode, 'RGBA')
        self.assertEqual(sheet.size, (5 * 192, 2 * 192))

    def test_build_is_idempotent_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._one_crop_root(tmp)
            status1, _ = _capture(['--repo-root', tmp, '--atlas', 'farm_crops_v01'])
            meta1, png1 = _read_pair(tmp, 'farm_crops_v01', 'crops')
            status2, _ = _capture(['--repo-root', tmp, '--atlas', 'farm_crops_v01'])
            meta2, png2 = _read_pair(tmp, 'farm_crops_v01', 'crops')

        self.assertEqual((status1, status2), (0, 0))
        self.assertEqual(png1, png2, 'PNG phải giống hệt từng byte giữa 2 lần chạy')
        self.assertEqual(meta1, meta2)

    def test_output_paths_follow_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._one_crop_root(tmp)
            status, _ = _capture(['--repo-root', tmp, '--atlas', 'farm_crops_v01'])
            meta, _ = _read_pair(tmp, 'farm_crops_v01', 'crops')
            png_exists = os.path.isfile(
                os.path.join(tmp, 'runtime', '1x', 'farm', 'crops', 'farm_crops_v01.png'))

        self.assertEqual(status, 0)
        self.assertEqual(meta['image'], '1x/farm/crops/farm_crops_v01.png')
        self.assertEqual(meta['format'], 'mayhoa-farm-crops-atlas-v1')
        self.assertTrue(png_exists)

    def test_dry_run_writes_nothing_but_reports_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._one_crop_root(tmp)
            status, out = _capture(['--repo-root', tmp, '--dry-run',
                                    '--atlas', 'farm_crops_v01'])
            wrote_anything = os.path.exists(os.path.join(tmp, 'runtime'))

        self.assertEqual(status, 0)
        self.assertFalse(wrote_anything, '--dry-run không được ghi gì')
        self.assertIn('farm_crops_v01', out)
        self.assertIn('960x384', out, 'phải in kích thước texture dự kiến')
        self.assertIn('2', out)

    def test_empty_source_fails_instead_of_writing_empty_atlas(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, 'masters', 'farm', 'crops'))
            status, out = _capture(['--repo-root', tmp, '--atlas', 'farm_crops_v01'])

        self.assertEqual(status, 1)
        self.assertIn('farm_crops_v01', out)


class TestSpecs(unittest.TestCase):
    """4 atlas trong hợp đồng phải khai báo đủ và không trùng đường dẫn."""

    def test_all_four_atlases_declared(self):
        names = [s.atlas for s in build_atlas.ATLAS_SPECS]
        self.assertEqual(sorted(names), [
            'farm_aquatic_v01', 'farm_crops_v01', 'farm_soil_v01', 'farm_trees_v01'])

    def test_unknown_atlas_name_is_rejected(self):
        with self.assertRaises(build_atlas.AtlasBuildError):
            build_atlas.spec_by_name('does_not_exist_v01')


TREE_STAGES = (
    'stage-01_sprout', 'stage-02_sapling', 'stage-03_young',
    'stage-04_flowering', 'stage-05_fruiting',
)

AQUATIC_STAGES = (
    'stage-01_planted', 'stage-02_sprout', 'stage-03_young',
    'stage-04_mature', 'stage-05_harvestable',
)

# canvas/box cho fixture guard. Anchor = contactY/canvas.
BIG_TREE = (128, (8, 8, 119, 120))    # anchorY 0.9375
SMALL_TREE = (64, (4, 4, 59, 60))     # anchorY 0.9375, canvas khác BIG_TREE
LOW_TREE = (64, (4, 4, 59, 40))       # anchorY 0.625, cùng canvas SMALL_TREE
LOTUS_LIKE = (128, (8, 8, 119, 121))  # anchorY 0.945313 (~970/1024)
WATER_LIKE = (96, (8, 8, 87, 91))     # anchorY 0.947917 (~728/768)


def _make_pack(root, cls, stages, packs):
    """packs: dict species -> (canvas, box). Trả về root cho tiện chain."""
    for species, (canvas, box) in packs.items():
        _make_species(root, cls, species, stages, canvas, box)
    return root


class TestCanvasUniformityGuard(unittest.TestCase):
    """Trộn master canvas ngoài ý muốn phải làm FAIL build, không ghi đè runtime.

    Tiền lệ: durian (canvas 1254) lọt vào farm_trees_v01 toàn canvas 1024
    (2026-09-10). Tool khi đó chỉ in NOTE QC rồi vẫn ghi đè runtime/.
    """

    def test_mixed_canvas_fails_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_pack(tmp, 'trees', TREE_STAGES,
                       {'lemon': BIG_TREE, 'mango': SMALL_TREE})
            status, out = _capture(['--repo-root', tmp, '--atlas', 'farm_trees_v01'])
            wrote = os.path.exists(os.path.join(tmp, 'runtime'))

        self.assertEqual(status, 1, 'canvas trộn phải fail, không được ghi im lặng')
        self.assertIn('canvas', out)
        self.assertIn('128x128', out)
        self.assertIn('64x64', out)
        self.assertFalse(wrote, 'build fail thì không được ghi file nào')

    def test_mixed_canvas_dry_run_also_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_pack(tmp, 'trees', TREE_STAGES,
                       {'lemon': BIG_TREE, 'mango': SMALL_TREE})
            status, out = _capture(['--repo-root', tmp, '--dry-run',
                                    '--atlas', 'farm_trees_v01'])

        self.assertEqual(status, 1, '--dry-run là bước kiểm trước khi build: phải báo lỗi')
        self.assertIn('farm_trees_v01', out)

    def test_allow_mixed_canvas_flag_unblocks_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_pack(tmp, 'trees', TREE_STAGES,
                       {'lemon': BIG_TREE, 'mango': SMALL_TREE})
            status, _ = _capture(['--repo-root', tmp, '--allow-mixed-canvas',
                                  '--atlas', 'farm_trees_v01'])
            meta, _ = _read_pair(tmp, 'farm_trees_v01', 'trees')

        self.assertEqual(status, 0)
        self.assertIn('masterCanvasBySpecies', meta)

    def test_aquatic_mixed_canvas_is_allowed_by_contract(self):
        """lotus 1024 vs water-* 768 là hợp lệ — không cần ai nhớ gõ flag."""
        with tempfile.TemporaryDirectory() as tmp:
            _make_pack(tmp, 'aquatic-crops', AQUATIC_STAGES,
                       {'lotus': LOTUS_LIKE, 'water-mimosa': WATER_LIKE})
            status, _ = _capture(['--repo-root', tmp, '--atlas', 'farm_aquatic_v01'])
            meta, _ = _read_pair(tmp, 'farm_aquatic_v01', 'aquatic')

        self.assertEqual(status, 0, 'atlas aquatic đang đúng không được bị chặn')
        self.assertIn('masterCanvasBySpecies', meta)
        self.assertTrue(build_atlas.spec_by_name('farm_aquatic_v01').mixed_canvas_ok)

    def test_uniform_canvas_produces_no_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_pack(tmp, 'trees', TREE_STAGES,
                       {'lemon': SMALL_TREE, 'mango': SMALL_TREE})
            plan = build_atlas.plan_atlas(build_atlas.spec_by_name('farm_trees_v01'), tmp)

        self.assertEqual(build_atlas.validate_plan(plan), ())


class TestAnchorSpreadGuard(unittest.TestCase):
    """anchorY lệch giữa các frame = sprite nhảy gốc khi đổi stage -> FAIL."""

    def test_anchor_spread_beyond_threshold_fails_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_pack(tmp, 'trees', TREE_STAGES,
                       {'lemon': SMALL_TREE, 'mango': LOW_TREE})
            status, out = _capture(['--repo-root', tmp, '--atlas', 'farm_trees_v01'])
            wrote = os.path.exists(os.path.join(tmp, 'runtime'))

        self.assertEqual(status, 1)
        self.assertIn('anchor', out.lower())
        self.assertFalse(wrote, 'build fail thì không được ghi file nào')

    def test_sub_pixel_spread_is_tolerated(self):
        """768 vs 1024 lệch nhau 1px làm tròn — đây là mức bình thường, phải qua."""
        with tempfile.TemporaryDirectory() as tmp:
            _make_pack(tmp, 'aquatic-crops', AQUATIC_STAGES,
                       {'lotus': LOTUS_LIKE, 'water-mimosa': WATER_LIKE})
            plan = build_atlas.plan_atlas(build_atlas.spec_by_name('farm_aquatic_v01'), tmp)
            meta = build_atlas.build_metadata(plan)

        self.assertGreater(meta['anchorSpread']['y'], 0.0)
        self.assertLess(meta['anchorSpread']['y'] * plan.spec.cell,
                        build_atlas.MAX_ANCHOR_DRIFT_PX)
        self.assertEqual(build_atlas.validate_plan(plan), ())

    def test_threshold_is_measured_in_cell_pixels(self):
        """Ngưỡng phải quy ra px trong cell — cùng ratio, cell to thì lệch nhiều hơn."""
        self.assertGreater(build_atlas.MAX_ANCHOR_DRIFT_PX, 0)
        self.assertLess(build_atlas.MAX_ANCHOR_DRIFT_PX, 8,
                        'ngưỡng lỏng quá thì durian 44.5px vẫn lọt')

    def test_allow_mixed_canvas_does_not_silence_anchor_guard(self):
        """Flag chỉ mở khoá canvas; anchor lệch luôn là lỗi master, không có escape."""
        with tempfile.TemporaryDirectory() as tmp:
            _make_pack(tmp, 'trees', TREE_STAGES,
                       {'lemon': SMALL_TREE, 'mango': LOW_TREE})
            status, out = _capture(['--repo-root', tmp, '--allow-mixed-canvas',
                                    '--atlas', 'farm_trees_v01'])

        self.assertEqual(status, 1)
        self.assertIn('anchor', out.lower())


if __name__ == '__main__':
    unittest.main()
