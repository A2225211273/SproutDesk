"""Draw the SproutDesk sprout logo and write every icon file the Windows build uses.

Run from the repo root: python sproutdesk/make_icons.py
Geometry is defined on a 64x64 grid (same as flutter/assets/icon.svg).
"""
from PIL import Image, ImageDraw

TEAL = "#1D9E75"
LEAF_LIGHT = "#E1F5EE"
WHITE = "#FFFFFF"
GRID = 64
SIZE = 1024
S = SIZE / GRID

RIGHT_LEAF = [(32, 18), (32, 11), (38, 8), (44, 9), (44, 15), (39, 19), (32, 18)]
LEFT_LEAF = [(32, 20), (32, 14), (27, 11), (21, 12), (21, 18), (26, 21), (32, 20)]

SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="{TEAL}"/>
<rect x="13" y="26" width="38" height="24" rx="4" fill="none" stroke="{WHITE}" stroke-width="3.5"/>
<path d="M26 56 h12" stroke="{WHITE}" stroke-width="3.5" stroke-linecap="round"/>
<path d="M32 26 V17" stroke="{WHITE}" stroke-width="3" stroke-linecap="round"/>
<path d="M32 18 C32 11 38 8 44 9 C44 15 39 19 32 18 Z" fill="{WHITE}"/>
<path d="M32 20 C32 14 27 11 21 12 C21 18 26 21 32 20 Z" fill="{LEAF_LIGHT}"/>
</svg>
"""


def bezier_path(pts, steps=48):
    """Closed path made of two cubic segments: p0 c1 c2 p3, p3 c4 c5 p6."""
    out = []
    for seg in (pts[0:4], pts[3:7]):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = seg
        for i in range(steps + 1):
            t = i / steps
            a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
            out.append(((a * x0 + b * x1 + c * x2 + d * x3) * S, (a * y0 + b * y1 + c * y2 + d * y3) * S))
    return out


def draw_logo():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=14 * S, fill=TEAL)
    d.rounded_rectangle([13 * S, 26 * S, 51 * S, 50 * S], radius=4 * S, outline=WHITE, width=round(3.5 * S))
    d.line([26 * S, 56 * S, 38 * S, 56 * S], fill=WHITE, width=round(3.5 * S))
    for x in (26, 38):
        d.ellipse([(x - 1.75) * S, (56 - 1.75) * S, (x + 1.75) * S, (56 + 1.75) * S], fill=WHITE)
    d.line([32 * S, 26 * S, 32 * S, 17 * S], fill=WHITE, width=3 * round(S))
    d.polygon(bezier_path(RIGHT_LEAF), fill=WHITE)
    d.polygon(bezier_path(LEFT_LEAF), fill=LEAF_LIGHT)
    return img


def main():
    logo = draw_logo()
    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    for path in ("flutter/windows/runner/resources/app_icon.ico", "res/icon.ico", "res/tray-icon.ico"):
        logo.save(path, sizes=ico_sizes)
    for path, px in (("res/icon.png", 512), ("res/32x32.png", 32), ("res/64x64.png", 64),
                     ("res/128x128.png", 128), ("res/128x128@2x.png", 256)):
        logo.resize((px, px), Image.LANCZOS).save(path)
    with open("flutter/assets/icon.svg", "w", encoding="utf-8", newline="\n") as f:
        f.write(SVG)
    print("Icons written")


if __name__ == "__main__":
    main()
