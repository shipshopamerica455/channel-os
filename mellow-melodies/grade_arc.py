#!/usr/bin/env python3
"""Derive a day arc from ONE plate by re-lighting it, not by generating six images.

Asking Flow for "the same window at six times of day" produces six different rooms —
it has no image-to-image mode, so nothing carries between prompts. Grading one
photograph instead makes the framing identical by construction: it is literally the
same pixels, re-lit. Which is the actual idea — you sit in one place and the light moves.

What a grade can do: temperature, exposure, contrast, saturation, and a vertical
gradient so the sky can brighten while the room stays dark. What it cannot do: switch
tower windows on or restructure cloud. So the lamp is lifted separately from the sky,
which is what sells "evening" without touching the geometry.

    python3 grade_arc.py --plate loops/arc/1-premarket.png
"""
import argparse, os
from PIL import Image, ImageEnhance

CHANNEL = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES"

# (name, brightness, contrast, saturation, sky tint RGB, sky strength, warm-lamp lift)
# Ordered through a trading day. Sky tint is applied top-weighted, so the horizon shifts
# while the desk in the lower third stays where it was.
STAGES = [
    ("1-premarket", 0.62, 1.05, 0.85, (18, 32, 68), 0.42, 0.28),
    ("2-open",      0.80, 1.10, 1.05, (96, 62, 30), 0.34, 0.18),
    ("3-morning",   1.06, 1.02, 0.98, (74, 96, 130), 0.24, 0.06),
    ("4-midday",    1.18, 0.92, 0.82, (128, 136, 148), 0.30, 0.00),
    ("5-afternoon", 0.98, 1.08, 1.06, (120, 84, 44), 0.26, 0.10),
    ("6-close",     0.66, 1.06, 0.92, (28, 34, 72), 0.44, 0.30),
]


def sky_gradient(size, colour, strength):
    """A tint that is strongest at the top and gone by the horizon line."""
    w, h = size
    col = Image.new("L", (1, h))
    px = col.load()
    for y in range(h):
        t = y / h
        # full strength at the top, faded out by 62% down — below that is room, not sky
        v = max(0.0, 1.0 - (t / 0.62)) ** 1.4 if t < 0.62 else 0.0
        px[0, y] = int(255 * v * strength)
    return Image.new("RGB", size, colour), col.resize(size)


def warm_lift(im, amount):
    """Push the already-bright warm pixels warmer — the lamp glows without touching the rest."""
    if amount <= 0:
        return im
    r, g, b = im.split()
    hot = r.point(lambda v: 255 if v > 150 else 0)
    warm = Image.merge("RGB", (
        r.point(lambda v: min(255, int(v * (1 + amount * 0.35)))),
        g.point(lambda v: min(255, int(v * (1 + amount * 0.16)))),
        b,
    ))
    return Image.composite(warm, im, hot)


def grade(plate, name, bright, contrast, sat, tint, tint_str, lamp, outdir):
    im = Image.open(plate).convert("RGB")
    sky, mask = sky_gradient(im.size, tint, tint_str)
    im = Image.composite(Image.blend(im, sky, 0.55), im, mask)
    im = ImageEnhance.Brightness(im).enhance(bright)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(sat)
    im = warm_lift(im, lamp)
    out = os.path.join(outdir, f"{name}.png")
    im.save(out)
    print(f"  {name}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", required=True, help="the single source photograph")
    ap.add_argument("--out", default="loops/arc-graded")
    a = ap.parse_args()

    plate = a.plate if os.path.isabs(a.plate) else os.path.join(CHANNEL, a.plate)
    outdir = a.out if os.path.isabs(a.out) else os.path.join(CHANNEL, a.out)
    os.makedirs(outdir, exist_ok=True)

    print(f"source: {os.path.basename(plate)}\n")
    for s in STAGES:
        grade(plate, *s, outdir)
    print(f"\n→ {outdir}")
