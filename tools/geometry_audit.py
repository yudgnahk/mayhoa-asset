#!/usr/bin/env python3
"""Geometry audit cho master asset Mayhoa (stdlib-only, không cần Pillow).

Đo alpha bbox, contactY, visible W/H và rootX (bottom-band centroid) theo đúng
contract trong MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md:

- alpha threshold: >= 24/255 (§6.1)
- bottom band: 3% visible height, tối thiểu 8 px (§7)

Hỗ trợ PNG RGBA8 (colortype 6) và palette+tRNS (colortype 3 — chỉ để audit
known-issue pack; master mới bắt buộc RGBA8 theo §6.3).

Lưu ý §7.1: rootX bottom-band chỉ tin cậy cho morphology thân đơn; với
radial/rosette (lotus, culantro...) chỉ dùng tham khảo, không PASS/FAIL tự động.

Usage:
    python3 tools/geometry_audit.py masters/farm/trees/coffee/*.png
"""
import struct
import sys
import zlib

ALPHA_THRESHOLD = 24
BAND_RATIO = 0.03
BAND_MIN_PX = 8


def _unfilter(raw, h, stride, bpp):
    """Giải PNG filter, trả về list các scanline đã unfilter."""
    prev = bytearray(stride)
    out = []
    off = 0
    for _ in range(h):
        ft = raw[off]
        off += 1
        line = bytearray(raw[off:off + stride])
        off += stride
        if ft == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 255
        elif ft == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif ft == 3:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif ft == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        prev = line
        out.append(line)
    return out


def alpha_rows(path):
    """Trả về (w, h, colortype, [bytes alpha mỗi row]) hoặc raise ValueError."""
    with open(path, 'rb') as f:
        data = f.read()
    pos = 8
    idat = b''
    trns = b''
    w = h = bd = ct = None
    try:
        while pos < len(data):
            ln = struct.unpack('>I', data[pos:pos + 4])[0]
            typ = data[pos + 4:pos + 8]
            chunk = data[pos + 8:pos + 8 + ln]
            if typ == b'IHDR':
                w, h, bd, ct = struct.unpack('>IIBB', chunk[:10])
            elif typ == b'IDAT':
                idat += chunk
            elif typ == b'tRNS':
                trns = chunk
            pos += 12 + ln
    except struct.error as err:
        raise ValueError(f"chunk header hỏng/cụt: {err}") from err
    if bd != 8 or ct not in (3, 6):
        raise ValueError(f"unsupported PNG: colortype={ct} bitdepth={bd} (master phải RGBA8)")
    try:
        raw = zlib.decompress(idat)
    except zlib.error as err:
        raise ValueError(f"IDAT corrupt: {err}") from err
    stride = w * 4 if ct == 6 else w
    need = h * (stride + 1)
    if len(raw) < need:
        raise ValueError(f"IDAT thiếu scanline: cần {need} byte, giải nén được {len(raw)}")
    if ct == 6:
        lines = _unfilter(raw, h, stride, 4)
        return w, h, ct, [bytes(l[3::4]) for l in lines]
    alpha = [trns[i] if i < len(trns) else 255 for i in range(256)]
    lines = _unfilter(raw, h, stride, 1)
    return w, h, ct, [bytes(alpha[v] for v in l) for l in lines]


def measure(path):
    w, h, ct, rows = alpha_rows(path)
    minx, miny, maxx, maxy = w, h, -1, -1
    for y, row in enumerate(rows):
        for x in range(w):
            if row[x] >= ALPHA_THRESHOLD:
                if x < minx:
                    minx = x
                if x > maxx:
                    maxx = x
                if y < miny:
                    miny = y
                if y > maxy:
                    maxy = y
    if maxx < 0:
        raise ValueError("empty image (không có pixel vượt alpha threshold)")
    vis_h = maxy - miny + 1
    band = max(BAND_MIN_PX, int(vis_h * BAND_RATIO))
    xs = [x for y in range(max(miny, maxy - band + 1), maxy + 1)
          for x in range(w) if rows[y][x] >= ALPHA_THRESHOLD]
    root_x = sum(xs) / len(xs)
    return {
        'canvas': (w, h),
        'colortype': ct,
        'bbox': (minx, miny, maxx, maxy),
        'contact_y': maxy,
        'vis_w': maxx - minx + 1,
        'vis_h': vis_h,
        'root_x': root_x,
    }


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    status = 0
    for path in argv:
        try:
            m = measure(path)
        except ValueError as err:
            print(f"{path}: ERR {err}")
            status = 1
            continue
        w, h = m['canvas']
        minx, miny, maxx, maxy = m['bbox']
        ct_note = '' if m['colortype'] == 6 else ' [PALETTE — vi phạm §6.3]'
        print(
            f"{path}: {w}x{h}{ct_note} bbox=({minx},{miny})-({maxx},{maxy}) "
            f"contactY={m['contact_y']} visW={m['vis_w']} visH={m['vis_h']} "
            f"rootX~{m['root_x']:.1f}"
        )
    return status


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
