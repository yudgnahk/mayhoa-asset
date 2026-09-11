#!/usr/bin/env python3
"""Test cho dechecker.py — khôi phục alpha từ nền caro vẽ chết vào pixel."""
import unittest

from PIL import Image

import dechecker


WHITE = (253, 253, 253)
GREY = (207, 207, 212)
CELL = 12


def make_checker(size, cell=CELL, tones=(WHITE, GREY)):
    """Dựng nền caro giống thứ ChatGPT vẽ ra."""
    img = Image.new('RGB', (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            px[x, y] = tones[((x // cell) + (y // cell)) % 2]
    return img


def composite(fg_rgb, alpha, size, cell=CELL):
    """Ghép một hình tròn màu fg_rgb với alpha cho trước lên nền caro."""
    bg = make_checker(size, cell)
    px = bg.load()
    cx = cy = size // 2
    r = size // 4
    truth = Image.new('L', (size, size), 0)
    tpx = truth.load()
    for y in range(size):
        for x in range(size):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d <= r:
                a = 1.0
            elif d <= r + 2:
                a = (r + 2 - d) / 2.0
            else:
                a = 0.0
            a *= alpha
            if a > 0:
                b = px[x, y]
                px[x, y] = tuple(round(a * f + (1 - a) * bb) for f, bb in zip(fg_rgb, b))
                tpx[x, y] = round(a * 255)
    return bg, truth


class TestCheckerTones(unittest.TestCase):
    def test_detects_both_tones(self):
        img = make_checker(96)
        tones = dechecker.checker_tones(img)
        self.assertEqual(len(tones), 2)
        found = {tuple(t) for t in tones}
        for want in (WHITE, GREY):
            self.assertTrue(
                any(sum(abs(a - b) for a, b in zip(want, f)) <= 9 for f in found),
                f"{want} không nằm trong {found}",
            )

    def test_rejects_image_without_checker(self):
        with self.assertRaises(ValueError):
            dechecker.checker_tones(Image.new('RGB', (64, 64), (12, 90, 40)))


class TestRecover(unittest.TestCase):
    def test_opaque_shape_becomes_opaque(self):
        img, truth = composite((40, 160, 60), 1.0, 160)
        out = dechecker.recover(img)
        self.assertEqual(out.mode, 'RGBA')
        a = out.getchannel('A')
        self.assertEqual(a.getpixel((80, 80)), 255)

    def test_background_becomes_transparent(self):
        img, _ = composite((40, 160, 60), 1.0, 160)
        a = dechecker.recover(img).getchannel('A')
        for p in [(0, 0), (5, 5), (159, 159), (0, 159), (159, 0)]:
            self.assertEqual(a.getpixel(p), 0, f"nền tại {p} phải trong suốt")

    def test_interior_white_is_kept(self):
        """Mắt trắng nằm trong sprite không được đục thủng — đây là lý do phải flood fill."""
        img, _ = composite((40, 160, 60), 1.0, 160)
        px = img.load()
        for y in range(76, 84):
            for x in range(76, 84):
                px[x, y] = (255, 255, 255)
        a = dechecker.recover(img).getchannel('A')
        self.assertEqual(a.getpixel((80, 80)), 255)

    def test_recovers_colour_without_light_fringe(self):
        img, _ = composite((40, 160, 60), 1.0, 160)
        out = dechecker.recover(img)
        r, g, b, _ = out.getpixel((80, 80))
        for got, want in zip((r, g, b), (40, 160, 60)):
            self.assertLessEqual(abs(got - want), 6)

    def test_edge_band_is_partially_transparent(self):
        img, truth = composite((40, 160, 60), 1.0, 160)
        a = dechecker.recover(img).getchannel('A')
        band = [
            (x, y)
            for y in range(160)
            for x in range(160)
            if 0 < truth.getpixel((x, y)) < 255
        ]
        self.assertTrue(band, "test fixture phải có rìa anti-alias")
        soft = [p for p in band if 0 < a.getpixel(p) < 255]
        self.assertGreater(len(soft) / len(band), 0.4)

    def test_already_rgba_passes_through(self):
        src = Image.new('RGBA', (32, 32), (10, 20, 30, 255))
        out = dechecker.recover(src)
        self.assertEqual(out.getpixel((0, 0)), (10, 20, 30, 255))


class TestCellSize(unittest.TestCase):
    def test_handles_other_cell_sizes(self):
        for cell in (8, 12, 16, 24):
            with self.subTest(cell=cell):
                img, _ = composite((200, 60, 50), 1.0, 192, cell=cell)
                a = dechecker.recover(img).getchannel('A')
                self.assertEqual(a.getpixel((0, 0)), 0)
                self.assertEqual(a.getpixel((96, 96)), 255)


if __name__ == '__main__':
    unittest.main()
