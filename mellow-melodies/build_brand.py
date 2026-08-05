#!/usr/bin/env python3
"""Channel art for the Mellow Melodies rebrand: logo, banner, thumbnail template.

Positioning is functional focus music for traders and high-stakes work, so the art
has to stop reading as spa/wellness. The old mark was a lotus figure in spa gold;
that is exactly the wrong signal for an audience that is at a desk under pressure.

Amber is deliberately carried over from the old logo. 1,117 people already
subscribed to a gold-and-dark channel — keeping the accent makes this read as the
same channel maturing rather than a stranger appearing in their subscriptions.

Everything carrying type is drawn in code. Image models garble rendered text, and a
misspelled channel name on a banner is unrecoverable.

    python3 build_brand.py          # writes into <MELLOW MELODIES>/brand/
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/brand"

# ── palette ──────────────────────────────────────────────────────────────────
INK       = (14, 20, 32)      # near-black navy — every ground
INK_LINE  = (26, 34, 48)      # faint rules
INK_SOFT  = (20, 28, 42)      # panel wash
AMBER     = (224, 163, 64)    # the accent, evolved from the old logo gold
AMBER_DP  = (186, 124, 38)    # deeper amber, gradients only
CREAM     = (242, 237, 228)   # warm off-white — primary type
SLATE     = (122, 137, 156)   # muted secondary type
SLATE_DK  = (78, 91, 108)

AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
ARIAL_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def _probe_avenir():
    """Avenir Next is a .ttc; find the regular/demi/bold face indices once."""
    faces = {}
    for i in range(12):
        try:
            f = ImageFont.truetype(AVENIR, 40, index=i)
            faces[f.getname()[1].lower()] = i
        except Exception:
            break
    return faces


FACES = _probe_avenir()


def font(size, weight="regular"):
    idx = FACES.get(weight)
    if idx is None:
        idx = FACES.get("regular")
    if idx is None:                       # Avenir unavailable — Arial still ships
        return ImageFont.truetype(ARIAL_B, size)
    return ImageFont.truetype(AVENIR, size, index=idx)


def centre(d, xy, text, f, fill, tracking=0):
    """Centred text. `tracking` letterspaces by drawing glyph by glyph."""
    x, y = xy
    if not tracking:
        l, t, r, b = d.textbbox((0, 0), text, font=f)
        d.text((x - (r - l) / 2 - l, y - (b - t) / 2 - t), text, font=f, fill=fill)
        return
    widths = [d.textlength(c, font=f) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    _, t, _, b = d.textbbox((0, 0), text, font=f)
    cx = x - total / 2
    for c, w in zip(text, widths):
        d.text((cx, y - (b - t) / 2 - t), c, font=f, fill=fill)
        cx += w + tracking


# ── 1. Logo mark ─────────────────────────────────────────────────────────────
# Nine rounded bars whose tops form a PLATEAU, not an arc. A peaky waveform reads
# as volatility, which is precisely what this audience is paying to not feel; a
# flat top reads as sustained and steady, which is the actual product promise.
# Full-bleed ground so YouTube's circle crop never exposes a corner.
BARS = [0.34, 0.62, 0.86, 0.94, 0.94, 0.94, 0.86, 0.62, 0.34]


def logo(size=800, path="logo.png", bars=BARS, glow=True):
    S = size * 4                                   # supersample, then downscale
    im = Image.new("RGB", (S, S), INK)
    d = ImageDraw.Draw(im)

    if glow:
        # faint warm centre, echoing the old gold logo without reintroducing it
        g = Image.new("RGB", (S, S), INK)
        gd = ImageDraw.Draw(g)
        gd.ellipse([S * 0.18, S * 0.18, S * 0.82, S * 0.82], fill=(38, 40, 44))
        g = g.filter(ImageFilter.GaussianBlur(S * 0.09))
        im = Image.blend(im, g, 0.85)
        d = ImageDraw.Draw(im)

    bw, gap = S * 0.0475, S * 0.0275
    total = len(bars) * bw + (len(bars) - 1) * gap
    x = (S - total) / 2
    cy, maxh = S / 2, S * 0.35
    for i, h in enumerate(bars):
        bh = maxh * h
        colour = AMBER if 1 < i < len(bars) - 2 else AMBER_DP
        d.rounded_rectangle([x, cy - bh / 2, x + bw, cy + bh / 2],
                            radius=bw / 2, fill=colour)
        x += bw + gap

    im = im.resize((size, size), Image.LANCZOS)
    im.save(os.path.join(OUT, path))
    print(f"{path} {size}x{size}")
    return im


def logo_smallsize_check():
    """Circle-crop the mark at the sizes YouTube actually renders it."""
    base = Image.open(os.path.join(OUT, "logo.png"))
    sizes = [176, 88, 48]
    pad = 40
    W = sum(sizes) + pad * (len(sizes) + 1)
    im = Image.new("RGB", (W, 176 + pad * 2), (235, 235, 238))
    x = pad
    for s in sizes:
        c = base.resize((s, s), Image.LANCZOS)
        mask = Image.new("L", (s * 4, s * 4), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, s * 4, s * 4], fill=255)
        c.putalpha(mask.resize((s, s), Image.LANCZOS))
        im.paste(c, (x, pad + (176 - s) // 2), c)
        x += s + pad
    im.save(os.path.join(OUT, "logo-smallsize-check.png"))
    print("logo-smallsize-check.png")


# ── 2. Channel banner ────────────────────────────────────────────────────────
# 2560x1440 canvas. Only the centred 1546x423 safe area is visible on every
# device, so every word lives inside it.
def banner():
    W, H = 2560, 1440
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)

    # A very low, very even waveform across the full canvas — the same "steady"
    # idea as the logo, at ambient strength. Deliberately monotonous.
    import math
    mid = H // 2
    for band, (amp, col, step) in enumerate([
        (150, INK_LINE, 7), (96, (30, 40, 56), 11),
    ]):
        pts = []
        for x in range(0, W + step, step):
            y = mid + amp * math.sin(x / 190.0 + band * 1.7) * 0.5
            pts.append((x, y))
        d.line(pts, fill=col, width=3)

    cx, cy = W // 2, H // 2
    centre(d, (cx, cy - 96), "MELLOW MELODIES", font(112, "demi bold"), CREAM, tracking=14)
    d.rectangle([cx - 90, cy - 20, cx + 90, cy - 15], fill=AMBER)

    centre(d, (cx, cy + 40), "Long-form focus music for work that demands full attention",
           font(46, "regular"), SLATE)
    centre(d, (cx, cy + 126), "DEEP WORK   ·   MARKET SESSIONS   ·   SLEEP",
           font(30, "demi bold"), AMBER, tracking=6)
    centre(d, (cx, cy + 190), "New sessions Tuesday · Thursday · Sunday",
           font(30, "regular"), SLATE_DK)

    im.save(os.path.join(OUT, "banner.png"))
    print("banner.png 2560x1440")

    # what phones/TVs actually crop to
    prev = im.copy()
    pd = ImageDraw.Draw(prev)
    pd.rectangle([(W - 1546) // 2, (H - 423) // 2,
                  (W + 1546) // 2, (H + 423) // 2], outline=(220, 80, 80), width=5)
    prev.save(os.path.join(OUT, "banner-safearea-preview.png"))
    print("banner-safearea-preview.png")


# ── 3. Thumbnail template ────────────────────────────────────────────────────
# Duration is the largest element because in this category it IS the buying
# decision — people choose by whether it covers their session, not by mood.
def thumbnail(duration, function, path, sub=None):
    W, H = 1280, 720
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)

    import math
    for band, (amp, col) in enumerate([(210, INK_LINE), (140, (28, 37, 52))]):
        pts = [(x, H / 2 + amp * math.sin(x / 130.0 + band * 1.9) * 0.5)
               for x in range(0, W + 6, 6)]
        d.line(pts, fill=col, width=4)

    d.rectangle([0, 0, 14, H], fill=AMBER)

    cx = W // 2 + 6
    centre(d, (cx, 300), duration.upper(), font(168, "heavy"), CREAM, tracking=2)
    centre(d, (cx, 430), function.upper(), font(58, "demi bold"), AMBER, tracking=12)
    if sub:
        centre(d, (cx, 520), sub, font(34, "regular"), SLATE)
    centre(d, (cx, 648), "MELLOW MELODIES", font(26, "demi bold"), SLATE_DK, tracking=8)

    im.save(os.path.join(OUT, path))
    print(f"{path} 1280x720")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"→ {OUT}\n")
    logo(800, "logo.png")
    logo(800, "logo-flat.png", glow=False)
    logo_smallsize_check()
    banner()
    thumbnail("6.5 HOURS", "NYSE Session", "thumb-01-nyse.png", "Open to close, uninterrupted")
    thumbnail("2 HOURS", "Deep Work", "thumb-02-deepwork.png", "Calm baroque · 60 BPM")
    thumbnail("8 HOURS", "Sleep", "thumb-03-sleep.png", "No ads · no interruptions")
    print("\nAll assets written.")
