#!/usr/bin/env python3
"""Test cho mode `center` của normalize_pack — dùng cho pest overlay và tool icon.

Hai class này lấy visual pivot ở tâm canvas (spec §5.5), không có world-contact
semantic nên không dùng được mode `root` hay `anchor`.
"""
import os
import tempfile
import unittest

from PIL import Image

import normalize_pack


CANVAS = (512, 512)
TARGET = (256, 256)
MARGIN = normalize_pack.MARGIN


def write_blob(path, canvas, box, colour=(200, 40, 40, 255)):
    """Ảnh có đúng một khối đục ở `box`, phần còn lại trong suốt."""
    img = Image.new('RGBA', canvas, (0, 0, 0, 0))
    Image.new('RGBA', (box[2] - box[0], box[3] - box[1]), colour).save
    img.paste(Image.new('RGBA', (box[2] - box[0], box[3] - box[1]), colour), (box[0], box[1]))
    img.save(path)
    return path


class TestCenterMode(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def _run(self, box, canvas_in=(1254, 1254)):
        p = write_blob(os.path.join(self.tmp, 'a.png'), canvas_in, box)
        normalize_pack.main(
            ['--mode', 'center', '--canvas', '512', '512',
             '--target', '256', '256', p]
        )
        return Image.open(p)

    def test_output_canvas_is_target(self):
        self.assertEqual(self._run((100, 200, 900, 700)).size, CANVAS)

    def test_content_is_centred(self):
        out = self._run((100, 200, 900, 700))
        m = normalize_pack.measure(out)
        cx = (m['minx'] + m['maxx']) / 2
        cy = (m['miny'] + m['maxy']) / 2
        self.assertLessEqual(abs(cx - 255.5), 1.0)
        self.assertLessEqual(abs(cy - 255.5), 1.0)

    def test_margins_respected(self):
        out = self._run((0, 0, 1254, 1254))
        m = normalize_pack.measure(out)
        for got in (m['minx'], m['miny'],
                    CANVAS[0] - 1 - m['maxx'], CANVAS[1] - 1 - m['maxy']):
            self.assertGreaterEqual(got, MARGIN)

    def test_aspect_ratio_preserved(self):
        """Scale phải đồng nhất — sprite dẹt không được kéo thành vuông."""
        out = self._run((100, 300, 1100, 800))
        m = normalize_pack.measure(out)
        self.assertAlmostEqual(m['vis_w'] / m['vis_h'], 1000 / 500, delta=0.03)

    def test_never_upscales(self):
        out = self._run((10, 10, 40, 40), canvas_in=(64, 64))
        m = normalize_pack.measure(out)
        self.assertEqual(m['vis_w'], 30)

    def test_wide_sprite_fits_width(self):
        out = self._run((0, 500, 1254, 700))
        m = normalize_pack.measure(out)
        self.assertLessEqual(m['maxx'], CANVAS[0] - 1 - MARGIN)
        self.assertGreaterEqual(m['minx'], MARGIN)


if __name__ == '__main__':
    unittest.main()
