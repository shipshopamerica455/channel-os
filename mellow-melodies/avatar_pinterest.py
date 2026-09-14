#!/usr/bin/env python3
"""Pinterest avatar from the existing channel mark.

    python3 avatar_pinterest.py

Not a new logo. The nine-bar plateau already carries the rebrand, and the pins are
built on the same ink and amber, so inventing a second mark for one platform would
just weaken both.

What does need changing is scale. logo.png sets the bars in the middle ~60% of an
800px square, which is right for YouTube, where the avatar renders large on the channel
page. Pinterest shows it at roughly 32-48px beside every pin in the feed, and at that
size the current framing is a small amber smudge inside a large dark circle — most of
the tile spent on empty ground.

So this crops to the mark's own bounding box and re-sets it to fill ~82% of the
diameter. The ceiling is ~88%: a circle crop keeps only the inscribed circle, and with
the bars' 1.85 aspect the bounding box corners hit the edge beyond that. 82% leaves
visible breathing room without wasting the tile.

Outputs avatar-pinterest.png (280x280, what Pinterest asks for) and a size check
rendering it at the sizes Pinterest actually draws.
"""
import os

from PIL import Image, ImageDraw

from build_brand import INK

BRAND = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/brand"
OUT = os.path.join(BRAND, "final")
FILL = 0.82                      # mark width as a fraction of the circle diameter


def mark_bbox(im):
    """Bounding box of the bars, ignoring the ground and its faint centre glow."""
    px = im.convert("RGB").load()
    w, h = im.size
    xs, ys = [], []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            # amber is strongly red-dominant; the ink ground and glow are not
            if r > 90 and r - b > 40:
                xs.append(x)
                ys.append(y)
    if not xs:
        raise SystemExit("no amber pixels found in logo.png — has the mark changed?")
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def build(size=280):
    src = Image.open(os.path.join(BRAND, "logo.png")).convert("RGB")
    box = mark_bbox(src)
    mark = src.crop(box)

    # Rebuild the ground rather than scaling the original's glow, which would smear.
    im = Image.new("RGB", (size * 4, size * 4), INK)
    S = size * 4
    target_w = int(S * FILL)
    target_h = max(1, round(mark.height * target_w / mark.width))
    if target_h > S * FILL:                       # never let a tall mark overflow
        target_h = int(S * FILL)
        target_w = max(1, round(mark.width * target_h / mark.height))
    mark = mark.resize((target_w, target_h), Image.LANCZOS)
    im.paste(mark, ((S - target_w) // 2, (S - target_h) // 2))

    im = im.resize((size, size), Image.LANCZOS)
    path = os.path.join(OUT, "avatar-pinterest.png")
    im.save(path)
    return im, path


def size_check(av):
    """Draw it circle-cropped at the sizes Pinterest renders, on Pinterest's white."""
    sizes = [120, 60, 48, 32]
    pad, gap = 30, 26
    W = pad * 2 + sum(sizes) + gap * (len(sizes) - 1)
    H = pad * 2 + max(sizes) + 22
    sheet = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    x = pad
    for s in sizes:
        tile = av.resize((s * 4, s * 4), Image.LANCZOS)
        mask = Image.new("L", (s * 4, s * 4), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, s * 4 - 1, s * 4 - 1], fill=255)
        tile = tile.resize((s, s), Image.LANCZOS)
        mask = mask.resize((s, s), Image.LANCZOS)
        y = pad + (max(sizes) - s) // 2
        sheet.paste(tile, (x, y), mask)
        d.text((x, pad + max(sizes) + 6), f"{s}px", fill=(90, 90, 90))
        x += s + gap
    path = os.path.join(OUT, "avatar-pinterest-sizecheck.png")
    sheet.save(path)
    return path


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    av, p = build()
    print(f"{p}  (280x280)")
    print(f"{size_check(av)}  — 120px profile header, 60/48px feed, 32px comment")
