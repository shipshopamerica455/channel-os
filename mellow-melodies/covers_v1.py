#!/usr/bin/env python3
"""Cover thumbnails — the A/B challenger, built as an experiment rather than a redesign.

Every thumbnail using thumbs_v3.py sits between 0.5% and 2.3% CTR across ~28,000
impressions. The one that clicks at 6.7% is a pre-relaunch album cover — a composer
at a piano, gold serif type, no duration label. Four clicks, so: a lead, not a finding.

Two things differ between those images at once, and shipping a redesign that changes
both would answer nothing. So this generates three variants that separate them:

    A  cover art  + cover type      both changed
    B  cover art  + current type    isolates the ARTWORK
    C  current art + cover type     isolates the TYPE

against the live thumbnail as control. If B beats control, the painterly figure is
doing the work and the type system can stay. If C beats control, it is the reverse,
and the cheaper fix is to restyle type over plates the channel already has. If only
A wins, they only work together.

Feed all three into Studio's Test & compare on one video with impressions to spare.

    python3 covers_v1.py
"""
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from build_brand import font, AMBER, CREAM
from build_final import cover, FINAL
from thumbs_v3 import hgrad_scrim, shadowed, draw_badge, plate as thumb_plate

COVERS = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/brand/cover-plates"
OUT = os.path.join(FINAL, "v3")
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"


def _didot_faces():
    """Didot ships as a .ttc; locate the bold face once, fall back to regular."""
    faces = {}
    for i in range(8):
        try:
            f = ImageFont.truetype(DIDOT, 40, index=i)
            faces[f.getname()[1].lower()] = i
        except Exception:
            break
    return faces


DIDOT_FACES = _didot_faces()


def serif(size, weight="bold"):
    idx = DIDOT_FACES.get(weight, DIDOT_FACES.get("regular", 0))
    try:
        return ImageFont.truetype(DIDOT, size, index=idx)
    except Exception:
        return font(size, "demi bold")      # Didot missing — Avenir rather than crash


def cover_plate(name):
    return Image.open(os.path.join(COVERS, f"{name}.png")).convert("RGB")


def vgrad_scrim(im, top=0.46, bottom=0.30, strength=0.86):
    """Darken top and bottom bands only, leaving the lit subject in the middle alone.

    The v3 scrim is a horizontal wipe because its type lives in a left-hand panel.
    Cover type is centred over the picture, so the shading has to run the other way.

    The ramp is eased rather than linear. A straight ramp meets the untouched middle
    at a visible seam, and the generated plates already carry faint darker bands at
    top and bottom — two soft edges a few pixels apart read as a printing error.
    """
    W, H = im.size
    col = Image.new("L", (1, H))
    px = col.load()
    for y in range(H):
        t = max(0.0, 1.0 - y / (H * top))
        b = max(0.0, 1.0 - (H - y) / (H * bottom))
        v = min(1.0, max(t, b))
        px[0, y] = int(255 * (v * v * (3 - 2 * v)) * strength)   # smoothstep
    mask = col.resize((W, H))
    return Image.composite(Image.new("RGB", (W, H), (6, 9, 16)), im, mask)


def centred(im, y, text, f, fill, tracking=0, blur=9, spread=3):
    """Horizontally centred, shadowed text — shadowed() takes a left origin."""
    d = ImageDraw.Draw(im)
    w = sum(d.textlength(c, font=f) for c in text) + tracking * (len(text) - 1)
    shadowed(im, ((im.size[0] - w) / 2, y), text, f, fill, tracking=tracking,
             blur=blur, spread=spread)


def rule(d, cx, y, half=150, colour=AMBER):
    d.rectangle([cx - half, y, cx + half, y + 3], fill=colour)


def cover_type(im, title, sub, badge=None):
    """Album-cover treatment: gold serif title centred over the picture, no panel."""
    W, H = im.size
    im = vgrad_scrim(im)
    d = ImageDraw.Draw(im)
    cx = W // 2

    centred(im, 34, "MELLOW MELODIES", font(24, "demi bold"), (198, 174, 132), tracking=10)

    # All type stays in the upper third, clear of the subject. The face is the whole
    # reason for this artwork — the first draft ran the subtitle straight across it.
    size = 112
    f = serif(size)
    while d.textlength(title, font=f) > W * 0.84 and size > 64:
        size -= 6
        f = serif(size)
    centred(im, 84, title, f, (236, 199, 132))

    d = ImageDraw.Draw(im)
    rule(d, cx, 84 + size + 22)
    centred(im, 84 + size + 44, sub, serif(40, "regular"), CREAM, tracking=5)
    draw_badge(d, W, badge)
    return im


def variant_a(plate_name, title, sub, out, badge=None):
    im = cover(cover_plate(plate_name), 1280, 720, 0.5)
    im = ImageEnhance.Color(im).enhance(1.06)
    cover_type(im, title, sub, badge).save(os.path.join(OUT, out))
    print(f"{out}  A — cover art + cover type   ({plate_name})")


def variant_b(plate_name, duration, function, out, sub=None, badge=None):
    """Cover artwork carrying the CURRENT type system, unchanged from thumbs_v3."""
    im = cover(cover_plate(plate_name), 1280, 720, 0.5)
    im = ImageEnhance.Color(im).enhance(1.10)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = hgrad_scrim(im)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 12, 720], fill=AMBER)
    x, size = 62, 152
    f = font(size, "heavy")
    while d.textlength(duration.upper(), font=f) > 660 and size > 96:
        size -= 6
        f = font(size, "heavy")
    shadowed(im, (x, 244), duration.upper(), f, CREAM)
    ImageDraw.Draw(im).rectangle([x, 244 + size + 26, x + 100, 244 + size + 33], fill=AMBER)
    shadowed(im, (x, 244 + size + 60), function.upper(), font(46, "demi bold"), AMBER, tracking=8)
    if sub:
        shadowed(im, (x, 244 + size + 126), sub, font(30, "regular"), (222, 228, 236), blur=6, spread=2)
    shadowed(im, (x, 86), "MELLOW MELODIES", font(24, "demi bold"), (176, 188, 204),
             tracking=7, blur=6, spread=2)
    draw_badge(d, 1280, badge)
    im.save(os.path.join(OUT, out))
    print(f"{out}  B — cover art + CURRENT type ({plate_name})")


def variant_c(plate_name, title, sub, out, badge=None):
    """Current plate carrying the cover type — the cheap fix, if type is what matters."""
    im = cover(thumb_plate(plate_name), 1280, 720, 0.5)
    im = ImageEnhance.Color(im).enhance(1.06)
    cover_type(im, title, sub, badge).save(os.path.join(OUT, out))
    print(f"{out}  C — CURRENT art + cover type ({plate_name})")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"→ {OUT}\n")

    # Target: yYIO72gZBL0, "10 Hours of Calm Classical for Sleep, Volume Two".
    #
    # The original target was the rain video, chosen in August when it had ~3,400
    # impressions. It has taken five views in the six weeks since — about one a week —
    # so a test there would now need months to separate three variants. This one takes
    # 182 genuine views and 148 suggested impressions per 28 days, 62% of everything
    # real on the channel. It is the only video with enough live traffic to resolve.
    #
    # "Genuine" matters here: Studio's figures for this video include 989 hours from a
    # blogspot embed farm at impossible rates per view. The 182 is what remains after
    # EXT_URL is removed, and it is the number the test will actually run on.
    # Not the firelight plate, though it is the handsomest of the four: the hearth is
    # the brightest object in it, and the channel has already lost a video that way —
    # filed next to fireplace-ambience channels, 1.3% CTR, arrivals expecting crackle.
    # The moonlit plate keeps the figure and the instrument without the fire.
    variant_a("sleep-a-pianist-moonlight", "CALM CLASSICAL", "TEN HOURS FOR SLEEP",
              "ab-classical-A.png")
    variant_b("sleep-d-pianist-moonlight-right", "10 HOURS", "Sleep Music",
              "ab-classical-B.png", "Volume two · no ads")
    variant_c("sleepmusic-b-piano-keys-lamp", "CALM CLASSICAL", "TEN HOURS FOR SLEEP",
              "ab-classical-C.png")
    print("\nControl is the live thumbnail (thumb-classical-v2.png).")
    print("Upload all three to Test & compare on yYIO72gZBL0.")
