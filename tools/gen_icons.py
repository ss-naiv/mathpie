#!/usr/bin/env python3
"""Generate MathPie PWA icons (icon-192.png, icon-512.png) with Pillow.

A cheerful pie with a slice cut and a happy face. Run from the repo root:
    .venv/bin/python tools/gen_icons.py
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw

REPO_ROOT = Path(__file__).resolve().parent.parent

BG = (255, 246, 236)      # app background cream
CRUST = (230, 111, 31)    # deep orange crust
FILLING = (255, 183, 77)  # amber filling
CUT = (255, 246, 236)     # slice cut = bg color
INK = (74, 63, 53)        # face


def draw_icon(size: int) -> Image.Image:
    s = size / 512  # design units on a 512 canvas
    img = Image.new("RGBA", (size, size), BG)
    d = ImageDraw.Draw(img)

    cx, cy, r = 256 * s, 268 * s, 176 * s

    # crust rim then filling
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CRUST)
    ri = r - 26 * s
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=FILLING)

    # cut a slice (wedge from center up-right), slightly separated look
    a0, a1 = math.radians(-80), math.radians(-25)
    wedge = [(cx, cy)]
    steps = 24
    for i in range(steps + 1):
        a = a0 + (a1 - a0) * i / steps
        wedge.append((cx + (r + 6 * s) * math.cos(a), cy + (r + 6 * s) * math.sin(a)))
    d.polygon(wedge, fill=CUT)

    # happy face on the pie
    er = 12 * s
    for ex in (cx - 60 * s, cx + 26 * s):
        d.ellipse([ex - er, cy + 10 * s - er, ex + er, cy + 10 * s + er], fill=INK)
    d.arc(
        [cx - 52 * s, cy + 22 * s, cx + 18 * s, cy + 74 * s],
        start=20, end=160, fill=INK, width=max(2, int(10 * s)),
    )
    # blush
    br = 14 * s
    for bx in (cx - 96 * s, cx + 62 * s):
        d.ellipse(
            [bx - br, cy + 44 * s - br, bx + br, cy + 44 * s + br],
            fill=(255, 205, 210, 220),
        )

    # steam curls above the pie
    for sx in (cx - 40 * s, cx + 40 * s):
        d.arc([sx - 16 * s, 44 * s, sx + 16 * s, 96 * s], start=90, end=270,
              fill=CRUST, width=max(2, int(12 * s)))

    return img.convert("RGB")


def main() -> None:
    for size in (192, 512):
        out = REPO_ROOT / f"icon-{size}.png"
        draw_icon(size).save(out)
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
