#!/usr/bin/env python3
"""Dựng state `selected` của tool icon từ bản `idle`.

Thanh công cụ hiển thị đúng một icon cho mỗi tool và chỉ đổi rendering khi được
chọn (FARM-INTERACTION §4). Generate lại bằng model cho ra pose và scale khác
nhau mỗi lần, icon nhảy khi bấm — nên `selected` là transform xác định trên
chính master idle: rim light vàng ấm ở mép trên-trái, tăng nhẹ sáng/bão hoà,
thêm glow ấm tràn vài pixel ra ngoài silhouette.

Glow được giữ trong margin 24px của master nên geometry không đổi và không cần
normalize lại.

Usage:
    python3 tools/make_selected.py idle.png selected.png
"""
import argparse
import sys

from PIL import Image, ImageChops, ImageEnhance, ImageFilter

RIM_OFFSET = 4          # px dịch alpha để lấy dải mép trên-trái
RIM_BLUR = 2.0
RIM_COLOUR = (255, 214, 130)
RIM_STRENGTH = 0.75

GLOW_BLUR = 5.0
GLOW_COLOUR = (255, 190, 90)
GLOW_ALPHA = 0.62

BRIGHTNESS = 1.06
SATURATION = 1.14


def _rim_mask(alpha):
    """Dải mép trên-trái: alpha trừ đi chính nó khi dịch xuống-phải."""
    shifted = ImageChops.offset(alpha, RIM_OFFSET, RIM_OFFSET)
    rim = ImageChops.subtract(alpha, shifted)
    return rim.filter(ImageFilter.GaussianBlur(RIM_BLUR))


def _glow_mask(alpha):
    """Vầng sáng ngoài: alpha đã blur, trừ phần nằm trong silhouette."""
    blurred = alpha.filter(ImageFilter.GaussianBlur(GLOW_BLUR))
    return ImageChops.subtract(blurred, alpha)


def selected(idle):
    """Trả bản `selected` của một tool icon RGBA."""
    img = idle.convert('RGBA')
    alpha = img.getchannel('A')
    if alpha.getextrema()[1] == 0:
        raise ValueError("ảnh idle không có pixel đục")

    rgb = img.convert('RGB')
    rgb = ImageEnhance.Brightness(rgb).enhance(BRIGHTNESS)
    rgb = ImageEnhance.Color(rgb).enhance(SATURATION)

    rim = _rim_mask(alpha)
    rim_layer = Image.new('RGB', img.size, RIM_COLOUR)
    rim_weight = rim.point(lambda v: round(v * RIM_STRENGTH))
    rgb = Image.composite(rim_layer, rgb, rim_weight)

    body = Image.merge('RGBA', (*rgb.split(), alpha))

    glow = _glow_mask(alpha).point(lambda v: round(v * GLOW_ALPHA))
    glow_layer = Image.new('RGBA', img.size, GLOW_COLOUR + (0,))
    glow_layer.putalpha(glow)

    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.alpha_composite(glow_layer)
    out.alpha_composite(body)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('src')
    ap.add_argument('dst')
    args = ap.parse_args(argv)

    out = selected(Image.open(args.src))
    out.save(args.dst)
    bbox = out.getchannel('A').point(lambda v: 255 if v >= 24 else 0).getbbox()
    print(f"{args.dst}: {out.size} bbox={bbox}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
