#!/usr/bin/env python3
"""Square album covers for the Ko-fi shop.

Square, because that is what every shop grid and music player expects — the 16:9
video thumbnails would be letterboxed and look like an afterthought. Same plates and
palette as the channel so the shop reads as part of it rather than a separate thing.

    python3 build_covers.py
"""
import os
from PIL import Image, ImageDraw, ImageEnhance

from build_brand import font, centre, INK, AMBER, CREAM
from build_final import FINAL

# thumb-plates are a separate set from build_final's UUID plates, so load them by path
PLATE_DIR = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/brand/thumb-plates"


def plate(name):
    return Image.open(os.path.join(PLATE_DIR, f"{name}.png")).convert("RGB")

OUT = os.path.join(FINAL, "covers")
SIZE = 1400

COVERS = [
    ("deep-work-vol-1", "deepwork-a-desk-glow", "DEEP WORK", "VOLUME ONE", "12 TRACKS"),
    ("night-sessions",  "sleepmusic-a-piano-moonlight", "NIGHT", "SESSIONS", "12 TRACKS"),
    ("low-cortisol",    "market-b-window-desk-city", "LOW", "CORTISOL", "8 TRACKS"),
]


def cover(slug, plate_key, line1, line2, tracks):
    im = plate(plate_key)
    # centre-crop to square before resizing, so nothing is stretched
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
    im = im.resize((SIZE, SIZE), Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(0.72)
    im = ImageEnhance.Color(im).enhance(1.05)

    # bottom-weighted scrim: the art stays visible up top, the type sits on solid ink
    grad = Image.new("L", (1, SIZE))
    px = grad.load()
    for y in range(SIZE):
        t = y / SIZE
        px[0, y] = int(235 * max(0.0, (t - 0.34) / 0.66) ** 1.25)
    im.paste(Image.new("RGB", (SIZE, SIZE), INK), (0, 0), grad.resize((SIZE, SIZE)))

    d = ImageDraw.Draw(im)
    cx = SIZE // 2
    centre(d, (cx, SIZE - 430), "MELLOW MELODIES", font(34, "demi bold"), (150, 162, 178), tracking=10)
    centre(d, (cx, SIZE - 330), line1, font(112, "heavy"), CREAM, tracking=4)
    centre(d, (cx, SIZE - 210), line2, font(112, "heavy"), CREAM, tracking=4)
    d.rectangle([cx - 70, SIZE - 130, cx + 70, SIZE - 124], fill=AMBER)
    centre(d, (cx, SIZE - 78), tracks, font(32, "demi bold"), AMBER, tracking=8)

    p = os.path.join(OUT, f"{slug}.png")
    im.save(p)
    print(f"  {slug}.png  {SIZE}x{SIZE}")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for c in COVERS:
        cover(*c)
    print(f"\n→ {OUT}")
