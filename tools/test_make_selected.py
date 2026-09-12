#!/usr/bin/env python3
"""Test cho make_selected.py — dựng state `selected` của tool icon từ bản idle.

Yêu cầu UI (FARM-INTERACTION §4): icon không được nhảy khi người chơi chọn,
nên silhouette phải trùng pixel với idle. Vì vậy `selected` được dẫn xuất bằng
transform xác định, không generate lại.
"""
import unittest

from PIL import Image, ImageDraw

import make_selected


CANVAS = 512


def make_idle(margin=60, colour=(120, 90, 60, 255)):
    img = Image.new('RGBA', (CANVAS, CANVAS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([margin, margin, CANVAS - 1 - margin, CANVAS - 1 - margin], fill=colour)
    return img


def opaque_bbox(img, thr=250):
    return img.getchannel('A').point(lambda v: 255 if v >= thr else 0).getbbox()


class TestSelected(unittest.TestCase):
    def setUp(self):
        self.idle = make_idle()
        self.sel = make_selected.selected(self.idle)

    def test_same_canvas_and_mode(self):
        self.assertEqual(self.sel.size, self.idle.size)
        self.assertEqual(self.sel.mode, 'RGBA')

    def test_core_silhouette_unchanged(self):
        """Vùng đục của idle phải trùng khít — đây là lý do tồn tại của script."""
        self.assertEqual(opaque_bbox(self.sel), opaque_bbox(self.idle))

    def test_opaque_pixels_stay_opaque(self):
        ia = self.idle.getchannel('A')
        sa = self.sel.getchannel('A')
        for p in [(256, 256), (256, 100), (100, 256)]:
            if ia.getpixel(p) == 255:
                self.assertEqual(sa.getpixel(p), 255, f"{p} bị thủng")

    def test_glow_extends_outside(self):
        ib = self.idle.getchannel('A').point(lambda v: 255 if v >= 24 else 0).getbbox()
        sb = self.sel.getchannel('A').point(lambda v: 255 if v >= 24 else 0).getbbox()
        self.assertLess(sb[0], ib[0])
        self.assertLess(sb[1], ib[1])
        self.assertGreater(sb[2], ib[2])
        self.assertGreater(sb[3], ib[3])

    def test_glow_stays_inside_canvas_margin(self):
        """Glow không được tràn ra ngoài margin 24px của master."""
        sb = self.sel.getchannel('A').point(lambda v: 255 if v >= 24 else 0).getbbox()
        self.assertGreaterEqual(sb[0], 24)
        self.assertGreaterEqual(sb[1], 24)
        self.assertLessEqual(sb[2], CANVAS - 24)
        self.assertLessEqual(sb[3], CANVAS - 24)

    def test_far_background_stays_transparent(self):
        sa = self.sel.getchannel('A')
        for p in [(0, 0), (5, 5), (511, 511), (0, 511)]:
            self.assertEqual(sa.getpixel(p), 0)

    def test_object_gets_brighter(self):
        def lum(img):
            px = img.load()
            vals = [sum(px[x, y][:3]) for y in range(200, 312) for x in range(200, 312)]
            return sum(vals) / len(vals)
        self.assertGreater(lum(self.sel), lum(self.idle))

    def test_rim_is_warm_on_upper_left(self):
        """Rim light nằm ở mép trên-trái, đúng hướng đèn của cả pack."""
        spx = self.sel.load()
        ipx = self.idle.load()
        ia = self.idle.getchannel('A')

        def edge_gain(sign):
            best = 0
            for t in range(60, 260):
                x = y = t if sign < 0 else CANVAS - 1 - t
                if ia.getpixel((x, y)) == 255:
                    best = max(best, spx[x, y][0] - ipx[x, y][0])
                    if best:
                        return best
            return best

        self.assertGreater(edge_gain(-1), edge_gain(1))

    def test_deterministic(self):
        again = make_selected.selected(make_idle())
        self.assertEqual(list(again.getdata()), list(self.sel.getdata()))

    def test_rejects_fully_transparent_input(self):
        with self.assertRaises(ValueError):
            make_selected.selected(Image.new('RGBA', (64, 64), (0, 0, 0, 0)))


if __name__ == '__main__':
    unittest.main()
