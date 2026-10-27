#!/usr/bin/env python3
"""Khôi phục alpha từ nền caro bị vẽ chết vào pixel.

Từ 2026-09-10 ChatGPT Create image trả PNG colortype 2 (RGB) và *vẽ* một lưới
caro trắng/xám thay cho nền trong suốt thật. Module này dựng lại alpha:

1. Đo hai tông caro ở viền ảnh.
2. Flood fill từ mép qua các pixel giống caro → vùng nền ngoài. Flood fill là
   bắt buộc: color key thuần sẽ đục thủng mắt trắng nằm *trong* sprite.
3. Difference matting ở dải rìa: biết nền B chính xác nên giải
   P = a*F + (1-a)*B để lấy alpha mượt và trả lại màu F, tránh viền sáng.

Usage:
    python3 tools/dechecker.py in.png out.png
"""
import argparse
import sys
from collections import Counter, deque

from PIL import Image

BORDER_BAND = 24        # dải viền dùng để đo tông caro
TONE_TOL = 26           # khoảng cách L1 tối đa để coi là pixel caro
SATURATION_MAX = 22     # caro là xám/trắng — chặn nhầm với artwork màu
EDGE_BAND = 3           # bề rộng dải rìa chạy difference matting
MIN_CONTRAST = 40       # |F-B| tối thiểu trên một kênh để kênh đó đáng tin


def _saturation(rgb):
    return max(rgb) - min(rgb)


def checker_tones(img, band=BORDER_BAND):
    """Trả về hai tông caro đo ở viền ảnh, sáng trước."""
    rgb = img.convert('RGB')
    w, h = rgb.size
    px = rgb.load()
    band = min(band, w // 2, h // 2)
    counts = Counter()
    for y in range(h):
        edge_row = y < band or y >= h - band
        step = 1 if edge_row else max(1, w - 1)
        for x in range(0, w, step):
            if not edge_row and band <= x < w - band:
                continue
            c = px[x, y]
            if _saturation(c) <= SATURATION_MAX:
                counts[tuple(v & ~3 for v in c)] += 1

    if not counts:
        raise ValueError("không tìm thấy pixel nền xám/trắng ở viền")

    ordered = [c for c, _ in counts.most_common()]
    first = ordered[0]
    second = None
    for c in ordered[1:]:
        if sum(abs(a - b) for a, b in zip(c, first)) > TONE_TOL:
            second = c
            break
    if second is None:
        raise ValueError("chỉ thấy một tông ở viền — ảnh này không có nền caro")

    tones = sorted([first, second], key=sum, reverse=True)
    return [tuple(v + 2 for v in t) for t in tones]


def _is_checker(c, tones):
    """Nhận cả pixel chuyển tiếp giữa hai ô caro, không chỉ hai tông đỉnh.

    Mép ô caro do model vẽ ra bị nhoè: bỏ qua dải trung gian thì flood fill
    tắc ngay ở ô đầu tiên."""
    if _saturation(c) > SATURATION_MAX:
        return False
    lum = sum(c) / 3.0
    lo = sum(tones[1]) / 3.0 - TONE_TOL
    hi = sum(tones[0]) / 3.0 + TONE_TOL
    return lo <= lum <= hi


def _exterior_mask(rgb, tones):
    """Flood fill 4 hướng từ mép qua pixel giống caro."""
    w, h = rgb.size
    px = rgb.load()
    outside = bytearray(w * h)
    seen = bytearray(w * h)
    q = deque()

    def push(x, y):
        i = y * w + x
        if seen[i]:
            return
        seen[i] = 1
        if _is_checker(px[x, y], tones):
            outside[i] = 1
            q.append((x, y))

    for x in range(w):
        push(x, 0)
        push(x, h - 1)
    for y in range(h):
        push(0, y)
        push(w - 1, y)

    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h:
                push(nx, ny)
    return outside


def _background_at(px, outside, w, h, x, y):
    """Màu nền dùng cho pixel rìa: lấy pixel nền ngoài gần nhất."""
    for r in range(1, EDGE_BAND + 2):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if max(abs(dx), abs(dy)) != r:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and outside[ny * w + nx]:
                    return px[nx, ny]
    return None


def _foreground_at(px, outside, near_edge, w, h, x, y):
    """Màu foreground tham chiếu: pixel đục gần nhất không nằm trong dải rìa."""
    for r in range(1, EDGE_BAND + 3):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if max(abs(dx), abs(dy)) != r:
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                i = ny * w + nx
                if not outside[i] and not near_edge[i]:
                    return px[nx, ny]
    return None


def _solve_alpha(p, f, b):
    """Giải a từ P = a*F + (1-a)*B trên các kênh đủ tương phản."""
    vals = []
    for pc, fc, bc in zip(p, f, b):
        if abs(fc - bc) < MIN_CONTRAST:
            continue
        vals.append((pc - bc) / (fc - bc))
    if not vals:
        return None
    vals.sort()
    return vals[len(vals) // 2]


def recover(img):
    """Trả RGBA với nền caro đã thành trong suốt."""
    if img.mode == 'RGBA':
        return img.copy()

    rgb = img.convert('RGB')
    w, h = rgb.size
    px = rgb.load()
    tones = checker_tones(rgb)
    outside = _exterior_mask(rgb, tones)

    near_edge = bytearray(w * h)
    for y in range(h):
        for x in range(w):
            if outside[y * w + x]:
                continue
            for dy in range(-EDGE_BAND, EDGE_BAND + 1):
                for dx in range(-EDGE_BAND, EDGE_BAND + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and outside[ny * w + nx]:
                        near_edge[y * w + x] = 1
                        break
                if near_edge[y * w + x]:
                    break

    out = Image.new('RGBA', (w, h))
    opx = out.load()
    for y in range(h):
        for x in range(w):
            i = y * w + x
            p = px[x, y]
            if outside[i]:
                opx[x, y] = (0, 0, 0, 0)
                continue
            if not near_edge[i]:
                opx[x, y] = p + (255,)
                continue

            b = _background_at(px, outside, w, h, x, y)
            f = _foreground_at(px, outside, near_edge, w, h, x, y)
            if b is None or f is None:
                opx[x, y] = p + (255,)
                continue
            a = _solve_alpha(p, f, b)
            if a is None:
                opx[x, y] = p + (255,)
                continue
            a = min(1.0, max(0.0, a))
            if a <= 0.004:
                opx[x, y] = (0, 0, 0, 0)
                continue
            unmat = tuple(
                min(255, max(0, round((pc - (1 - a) * bc) / a)))
                for pc, bc in zip(p, b)
            )
            opx[x, y] = unmat + (round(a * 255),)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('src')
    ap.add_argument('dst')
    args = ap.parse_args(argv)

    src = Image.open(args.src)
    try:
        out = recover(src)
    except ValueError as e:
        print(f"{args.src}: {e}", file=sys.stderr)
        return 1
    out.save(args.dst)
    alpha = out.getchannel('A')
    lo, hi = alpha.getextrema()
    print(f"{args.dst}: {out.size} RGBA alpha {lo}-{hi}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
