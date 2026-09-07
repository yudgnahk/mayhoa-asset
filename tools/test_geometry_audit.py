#!/usr/bin/env python3
"""Test cho tools/geometry_audit.py (stdlib-only, chạy bằng unittest).

    python3 -m unittest discover -s tools -p 'test_*.py' -v

Trọng tâm: một file PNG hỏng KHÔNG được phép làm crash cả run và nuốt im lặng
các file phía sau trong glob (regression của bug soil_tilled -> soil_wet).
"""
import io
import os
import struct
import sys
import tempfile
import unittest
import zlib
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import geometry_audit  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOIL_DIR = os.path.join(REPO_ROOT, 'masters', 'farm', 'soil')
CORRUPT_FIXTURE = os.path.join(SOIL_DIR, 'soil_tilled_v01.png')
HEALTHY_FIXTURE = os.path.join(SOIL_DIR, 'soil_wet_v01.png')

PNG_SIG = b'\x89PNG\r\n\x1a\n'


def _chunk(typ, payload):
    """Đóng gói 1 PNG chunk kèm CRC hợp lệ."""
    return (struct.pack('>I', len(payload)) + typ + payload
            + struct.pack('>I', zlib.crc32(typ + payload) & 0xFFFFFFFF))


def _rgba8_png(w, h, opaque_box):
    """PNG RGBA8 hợp lệ: nền trong suốt, 1 ô đục opaque_box=(x0,y0,x1,y1)."""
    x0, y0, x1, y1 = opaque_box
    raw = bytearray()
    for y in range(h):
        raw.append(0)  # filter type None
        for x in range(w):
            solid = x0 <= x <= x1 and y0 <= y <= y1
            raw += bytes((255, 255, 255, 255 if solid else 0))
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
    return (PNG_SIG + _chunk(b'IHDR', ihdr)
            + _chunk(b'IDAT', zlib.compress(bytes(raw)))
            + _chunk(b'IEND', b''))


def _corrupt_idat_png(w=16, h=16):
    """PNG có header hợp lệ nhưng payload IDAT không phải zlib stream hợp lệ."""
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
    return (PNG_SIG + _chunk(b'IHDR', ihdr)
            + _chunk(b'IDAT', b'\x78\x9c' + b'\xde\xad\xbe\xef' * 8)
            + _chunk(b'IEND', b''))


def _write(tmpdir, name, blob):
    path = os.path.join(tmpdir, name)
    with open(path, 'wb') as f:
        f.write(blob)
    return path


def _run_audit(paths):
    """Chạy geometry_audit.main(), trả về (exit_status, stdout)."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        status = geometry_audit.main(list(paths))
    return status, buf.getvalue()


class TestCorruptFileDoesNotHideOthers(unittest.TestCase):
    """Bug chính: file hỏng làm script chết giữa chừng, bỏ im lặng file sau."""

    def test_healthy_file_after_corrupt_is_still_measured(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = _write(tmp, 'a_bad.png', _corrupt_idat_png())
            good = _write(tmp, 'b_good.png', _rgba8_png(16, 16, (3, 4, 8, 10)))

            status, out = _run_audit([bad, good])

            self.assertIn('ERR', out, 'file hỏng phải in dòng ERR')
            self.assertIn(f'{good}: 16x16', out,
                          'file lành ĐỨNG SAU file hỏng vẫn phải được đo')
            self.assertIn('contactY=10', out)
            self.assertEqual(status, 1, 'exit code vẫn phải báo lỗi')

    def test_repo_soil_glob_measures_every_healthy_tile(self):
        if not os.path.isfile(CORRUPT_FIXTURE) or not os.path.isfile(HEALTHY_FIXTURE):
            self.skipTest('thiếu fixture masters/farm/soil/*.png')

        status, out = _run_audit([CORRUPT_FIXTURE, HEALTHY_FIXTURE])

        self.assertIn(f'{CORRUPT_FIXTURE}: ERR', out)
        self.assertIn(f'{HEALTHY_FIXTURE}: 512x512', out,
                      'soil_wet phải được đo dù soil_tilled hỏng')
        self.assertEqual(status, 1)

    def test_alpha_rows_raises_valueerror_on_corrupt_idat(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = _write(tmp, 'bad.png', _corrupt_idat_png())
            with self.assertRaises(ValueError):
                geometry_audit.alpha_rows(bad)

    def test_alpha_rows_raises_valueerror_on_truncated_chunk(self):
        with tempfile.TemporaryDirectory() as tmp:
            blob = _rgba8_png(16, 16, (3, 4, 8, 10))
            bad = _write(tmp, 'cut.png', blob[:len(blob) // 2])
            with self.assertRaises(ValueError):
                geometry_audit.alpha_rows(bad)

    def test_alpha_rows_raises_valueerror_on_missing_ihdr(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = _write(tmp, 'noihdr.png', PNG_SIG + _chunk(b'IEND', b''))
            with self.assertRaises(ValueError):
                geometry_audit.alpha_rows(bad)


class TestHappyPath(unittest.TestCase):
    """Format & số đo của file hợp lệ phải giữ nguyên."""

    def test_rgba8_measurements(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = _write(tmp, 'good.png', _rgba8_png(16, 16, (3, 4, 8, 10)))
            m = geometry_audit.measure(good)

        self.assertEqual(m['canvas'], (16, 16))
        self.assertEqual(m['colortype'], 6)
        self.assertEqual(m['bbox'], (3, 4, 8, 10))
        self.assertEqual(m['contact_y'], 10)
        self.assertEqual(m['vis_w'], 6)
        self.assertEqual(m['vis_h'], 7)
        self.assertAlmostEqual(m['root_x'], 5.5)

    def test_output_line_format_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = _write(tmp, 'good.png', _rgba8_png(16, 16, (3, 4, 8, 10)))
            status, out = _run_audit([good])

        self.assertEqual(status, 0)
        self.assertEqual(
            out.strip(),
            f'{good}: 16x16 bbox=(3,4)-(8,10) contactY=10 visW=6 visH=7 rootX~5.5',
        )


if __name__ == '__main__':
    unittest.main()
