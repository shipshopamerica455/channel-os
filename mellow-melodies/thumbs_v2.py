#!/usr/bin/env python3
"""Thumbnails v2 — let the image breathe.

v1 centred the type and laid a heavy full-width scrim under it, which flattened
every plate to near-black and wasted the photography. The picture was doing no work.

v2 moves the type into the left third behind a horizontal gradient — dense at the
left edge, fully clear by 60% across — so the type still has solid pixels under it
while the right two thirds of the image stay bright and legible. The plates are also
graded lighter, because a thumbnail competes in a feed against bright ones and the
first thing lost at 200px wide is a dark image.

    python3 thumbs_v2.py
"""
import os
from PIL import Image, ImageDraw, ImageEnhance

from build_brand import font, INK, AMBER, CREAM
from build_final import plate, cover, FINAL

OUT = os.path.join(FINAL, "v2")


def hgrad_scrim(im, solid_to=0.30, clear_by=0.62, strength=0.92):
    """Dark at the left edge, gone by `clear_by` across. Eased, so there is no band."""
    W, H = im.size
    row = Image.new("L", (W, 1))
    px = row.load()
    a, b = int(W * solid_to), int(W * clear_by)
    for x in range(W):
        if x <= a:
            v = 1.0
        elif x >= b:
            v = 0.0
        else:
            t = (x - a) / (b - a)
            v = 1 - (t * t * (3 - 2 * t))          # smoothstep
        px[x, 0] = int(255 * v * strength)
    mask = row.resize((W, H))
    out = im.copy()
    out.paste(Image.new("RGB", (W, H), INK), (0, 0), mask)
    return out


def text_left(d, x, y, text, f, fill, tracking=0):
    if not tracking:
        d.text((x, y), text, font=f, fill=fill)
        return
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking


def thumbnail(key, duration, function, path_out, sub=None, bias=0.5, bright=1.0):
    W, H = 1280, 720
    im = cover(plate(key), W, H, bias)
    im = ImageEnhance.Brightness(im).enhance(bright)
    im = ImageEnhance.Color(im).enhance(1.06)       # a touch richer, not saturated
    im = hgrad_scrim(im)
    d = ImageDraw.Draw(im)

    d.rectangle([0, 0, 12, H], fill=AMBER)

    x = 62
    # Duration is the largest element — in this category it is the buying decision.
    # Auto-shrink rather than let a long value collide with the gradient's clear edge.
    size = 150
    f = font(size, "heavy")
    while d.textlength(duration.upper(), font=f) > 640 and size > 96:
        size -= 6
        f = font(size, "heavy")
    text_left(d, x, 250, duration.upper(), f, CREAM)

    d.rectangle([x, 250 + size + 26, x + 96, 250 + size + 32], fill=AMBER)
    text_left(d, x, 250 + size + 58, function.upper(), font(46, "demi bold"), AMBER, tracking=8)
    if sub:
        text_left(d, x, 250 + size + 124, sub, font(30, "regular"), (206, 214, 224))

    text_left(d, x, 88, "MELLOW MELODIES", font(24, "demi bold"), (156, 168, 184), tracking=7)

    im.save(os.path.join(OUT, path_out))
    print(f"{path_out}  ({key})")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"→ {OUT}\n")
    # Brightness is per-plate: the hall and the line start almost black and need
    # lifting, the skyline is already readable.
    thumbnail("skyline",  "2 HOURS",   "Deep Work",   "thumb-deepwork.png", "Calm baroque · 60 BPM",       bias=0.45, bright=1.35)
    thumbnail("skyline",  "6.5 HOURS", "NYSE Session", "thumb-nyse.png",    "Open to close, uninterrupted", bias=0.30, bright=1.25)
    thumbnail("desk_lib", "8 HOURS",   "Sleep",       "thumb-sleep.png",    "No ads · no interruptions",    bias=0.50, bright=1.45)
    thumbnail("hall",     "3 HOURS",   "The Overlap", "thumb-overlap.png",  "London · New York",            bias=0.36, bright=1.60)
    print("\nDone.")
