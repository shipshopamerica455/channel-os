#!/usr/bin/env python3
"""Composite the generated backgrounds with code-drawn type → upload-ready assets.

The generated plates supply atmosphere; every word is still drawn here, because
image models garble lettering and a misspelled channel name on a banner is
unrecoverable. Sources are 3:2, so everything is cover-cropped to 16:9 or 1:1.

Each plate also gets graded toward the palette (#0E1420 navy / #E0A340 amber) and a
scrim under the type zone. The plates were prompted with a dark, empty centre, but a
scrim makes the type legible regardless of what any future plate looks like — the
banner must not break the next time a background is swapped.

    python3 build_final.py
"""
import os
from PIL import Image, ImageDraw, ImageEnhance

from build_brand import (font, centre, logo, OUT,
                         INK, AMBER, AMBER_DP, CREAM, SLATE, SLATE_DK)

SRC = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/LOGO REBRAND ASSETS"
FINAL = os.path.join(OUT, "final")

PLATES = {
    "hall":     "add32068-2483-43b7-ae71-d2877eaa0cc5.png",  # empty concert hall, one stage light
    "skyline":  "d39eb5f5-80ee-4feb-9f30-5af25ea25aaf.png",  # city before dawn from a window
    "desk_mod": "5e6b7146-4283-4f55-93ed-00184024f0f2.png",  # modern desk, lamp, city beyond
    "desk_lib": "200e805e-4bc9-401c-85cb-6080046e2078.png",  # library desk, brass lamp
    "line":     "d4a1a3cb-605a-4c8d-aaa0-19b076af009d.png",  # amber steady line, navy ground
    "line_blk": "ae6f5b2d-f77a-40c0-b67d-2644dbbf07b5.png",  # amber steady line, black ground
    "string":   "22388b81-22ec-497b-a92f-522f33a27851.png",  # piano string macro
}


def plate(key):
    return Image.open(os.path.join(SRC, PLATES[key])).convert("RGB")


def cover(im, W, H, bias=0.5):
    """Scale to cover WxH and crop. `bias` picks the vertical slice (0=top, 1=bottom)."""
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = round((im.height - H) * bias)
    return im.crop((x, y, x + W, y + H))


def grade(im, darken=0.72, tint=0.16):
    """Pull the plate toward the brand navy so every asset reads as one set."""
    im = ImageEnhance.Brightness(im).enhance(darken)
    im = ImageEnhance.Color(im).enhance(0.88)
    wash = Image.new("RGB", im.size, INK)
    return Image.blend(im, wash, tint)


def scrim(im, top, bottom, strength=0.80, feather=0.35):
    """Darken a horizontal band so type always reads. Feathered, so there is no seam."""
    h = im.height
    band = max(bottom - top, 1)
    fade = max(int(band * feather), 1)
    col = Image.new("L", (1, h), 0)
    px = col.load()
    for y in range(h):
        if top <= y <= bottom:
            v = 1.0
        elif top - fade <= y < top:
            v = (y - (top - fade)) / fade
        elif bottom < y <= bottom + fade:
            v = 1 - (y - bottom) / fade
        else:
            v = 0.0
        px[0, y] = int(255 * v * strength)
    mask = col.resize(im.size)
    out = im.copy()
    out.paste(Image.new("RGB", im.size, INK), (0, 0), mask)
    return out


# ── banner ───────────────────────────────────────────────────────────────────
def banner(key="hall", name="banner.png", bias=0.5):
    W, H = 2560, 1440
    im = grade(cover(plate(key), W, H, bias), darken=0.80, tint=0.20)
    # Safe area is the centred 1546x423; scrim a little wider than the type block.
    im = scrim(im, H // 2 - 250, H // 2 + 250, strength=0.72)
    d = ImageDraw.Draw(im)

    cx, cy = W // 2, H // 2
    centre(d, (cx, cy - 96), "MELLOW MELODIES", font(112, "demi bold"), CREAM, tracking=14)
    d.rectangle([cx - 90, cy - 20, cx + 90, cy - 15], fill=AMBER)
    centre(d, (cx, cy + 40), "Long-form focus music for work that demands full attention",
           font(46, "regular"), (198, 205, 214))
    centre(d, (cx, cy + 126), "DEEP WORK   ·   MARKET SESSIONS   ·   SLEEP",
           font(30, "demi bold"), AMBER, tracking=6)
    centre(d, (cx, cy + 190), "New sessions Tuesday · Thursday · Sunday",
           font(30, "regular"), (150, 162, 178))

    im.save(os.path.join(FINAL, name))
    print(f"{name} 2560x1440  ({key})")

    prev = im.copy()
    ImageDraw.Draw(prev).rectangle(
        [(W - 1546) // 2, (H - 423) // 2, (W + 1546) // 2, (H + 423) // 2],
        outline=(220, 80, 80), width=5)
    prev.save(os.path.join(FINAL, name.replace(".png", "-safearea.png")))


# ── avatar ───────────────────────────────────────────────────────────────────
def avatar_from_line(size=800, name="avatar-line.png"):
    """The generated 'steady line' as an avatar, with the plateau bars rising from it.

    A bare line is a strong 16:9 image but a weak avatar — cropped to a circle at 48px
    it reads as a hyphen. Standing the bars on it keeps the generated glow while
    leaving something with actual mass at feed size.
    """
    S = size * 4
    im = cover(plate("line"), S, S)
    im = ImageEnhance.Brightness(im).enhance(0.92)

    d = ImageDraw.Draw(im)
    bars = [0.34, 0.62, 0.86, 0.94, 0.94, 0.94, 0.86, 0.62, 0.34]
    bw, gap = S * 0.0475, S * 0.0275
    total = len(bars) * bw + (len(bars) - 1) * gap
    x, cy, maxh = (S - total) / 2, S / 2, S * 0.35
    for i, h in enumerate(bars):
        bh = maxh * h
        col = (255, 214, 150) if 1 < i < len(bars) - 2 else AMBER
        d.rounded_rectangle([x, cy - bh / 2, x + bw, cy + bh / 2], radius=bw / 2, fill=col)
        x += bw + gap

    im = im.resize((size, size), Image.LANCZOS)
    im.save(os.path.join(FINAL, name))
    print(f"{name} {size}x{size}")


def avatar_compare():
    """Both candidates at the sizes YouTube actually renders, circle-cropped.

    48px is the one that decides it — that is the size in a subscription feed, and
    anything that collapses there is not a viable avatar however good it looks at 800.
    """
    cands = [("code-drawn bars", os.path.join(OUT, "logo.png")),
             ("generated line + bars", os.path.join(FINAL, "avatar-line.png"))]
    sizes = [176, 88, 48]
    pad, row = 46, 236
    W = sum(sizes) + pad * (len(sizes) + 1) + 300
    im = Image.new("RGB", (W, row * len(cands) + pad), (236, 237, 240))
    d = ImageDraw.Draw(im)
    for r, (label, path) in enumerate(cands):
        base = Image.open(path).convert("RGB")
        y0 = pad + r * row
        d.text((pad, y0 + 88), label, font=font(30, "demi bold"), fill=(40, 44, 52))
        x = pad + 300
        for s in sizes:
            c = base.resize((s, s), Image.LANCZOS)
            m = Image.new("L", (s * 4, s * 4), 0)
            ImageDraw.Draw(m).ellipse([0, 0, s * 4, s * 4], fill=255)
            c.putalpha(m.resize((s, s), Image.LANCZOS))
            im.paste(c, (x, y0 + (176 - s) // 2), c)
            d.text((x, y0 + 190), f"{s}px", font=font(22, "regular"), fill=(120, 126, 136))
            x += s + pad
    im.save(os.path.join(FINAL, "avatar-compare.png"))
    print("avatar-compare.png")


# ── thumbnails ───────────────────────────────────────────────────────────────
def thumbnail(key, duration, function, path, sub=None, bias=0.5):
    W, H = 1280, 720
    im = grade(cover(plate(key), W, H, bias), darken=0.66, tint=0.22)
    # Runs to 690, not 560 — the channel wordmark sits at 648, and left on raw plate a
    # bright background detail between letterspaced glyphs can read as punctuation.
    im = scrim(im, 170, 690, strength=0.78)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 14, H], fill=AMBER)

    cx = W // 2 + 6
    centre(d, (cx, 300), duration.upper(), font(168, "heavy"), CREAM, tracking=2)
    centre(d, (cx, 430), function.upper(), font(58, "demi bold"), AMBER, tracking=12)
    if sub:
        centre(d, (cx, 520), sub, font(34, "regular"), (186, 195, 206))
    centre(d, (cx, 648), "MELLOW MELODIES", font(26, "demi bold"), (140, 152, 168), tracking=8)

    im.save(os.path.join(FINAL, path))
    print(f"{path} 1280x720  ({key})")


if __name__ == "__main__":
    os.makedirs(FINAL, exist_ok=True)
    print(f"→ {FINAL}\n")

    banner("hall", "banner.png", bias=0.42)
    banner("skyline", "banner-alt-skyline.png", bias=0.55)

    logo(800, "logo.png")                      # ensure the code-drawn mark exists
    avatar_from_line()
    avatar_compare()

    # Plate assignment is deliberate: BOTH desk plates have a glass of whisky on them.
    # That is fine for the Sunday decompression pillar — putting the day down — and
    # wrong for a video sold on clear decisions under pressure. So the desk goes to
    # sleep only, and the functional videos get the abstract line and the skyline.
    thumbnail("line", "2 Hours", "Deep Work", "thumb-deepwork.png",
              "Calm baroque · 60 BPM")
    thumbnail("skyline", "6.5 Hours", "NYSE Session", "thumb-nyse.png",
              "Open to close, uninterrupted", bias=0.45)
    thumbnail("desk_lib", "8 Hours", "Sleep", "thumb-sleep.png",
              "No ads · no interruptions", bias=0.50)
    thumbnail("hall", "3 Hours", "The Overlap", "thumb-overlap.png",
              "London · New York", bias=0.42)

    print("\nUpload-ready.")
