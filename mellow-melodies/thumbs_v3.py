#!/usr/bin/env python3
"""Thumbnails v3 — high-contrast plates, type that can survive them.

v2 fixed the layout but was still built on the video plates, which are prompted
"muted, restrained… deep near-black navy dominates". Correct for something playing
behind six hours of work; dead on arrival as a 200px tile.

v3 uses purpose-generated plates (gen-thumb-plates.mjs) built on warm amber practical
light against deep blue night. They arrive bright and saturated, so the job flips:
instead of lifting a dark image, the type now has to hold up against a busy, luminous
one. Hence a soft shadow behind every glyph rather than relying on the scrim alone —
the scrim can then stay light enough to keep the picture alive.

    python3 thumbs_v3.py
"""
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

from build_brand import font, INK, AMBER, CREAM
from build_final import cover, FINAL

PLATES = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/brand/thumb-plates"
OUT = os.path.join(FINAL, "v3")


def plate(name):
    return Image.open(os.path.join(PLATES, f"{name}.png")).convert("RGB")


def hgrad_scrim(im, solid_to=0.26, clear_by=0.58, strength=0.86):
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
            v = 1 - (t * t * (3 - 2 * t))
        px[x, 0] = int(255 * v * strength)
    out = im.copy()
    out.paste(Image.new("RGB", (W, H), INK), (0, 0), row.resize((W, H)))
    return out


def shadowed(im, xy, text, f, fill, tracking=0, blur=9, spread=3):
    """Draw text with a soft dark halo so it holds over a bright, busy plate."""
    layer = Image.new("L", im.size, 0)
    ld = ImageDraw.Draw(layer)

    def _draw(d, x0, y0, col):
        x = x0
        if not tracking:
            d.text((x, y0), text, font=f, fill=col)
            return
        for ch in text:
            d.text((x, y0), ch, font=f, fill=col)
            x += d.textlength(ch, font=f) + tracking

    x, y = xy
    for dx in range(-spread, spread + 1, spread or 1):
        for dy in range(-spread, spread + 1, spread or 1):
            _draw(ld, x + dx, y + dy, 190)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.new("RGB", im.size, (2, 4, 8)), (0, 0), layer)
    _draw(ImageDraw.Draw(im), x, y, fill)


# Corner badge — one glance tells a returning viewer which series a tile belongs to.
# Colour does the work; the word is confirmation. Kept small and top-right so it never
# competes with the duration, which is still the buying decision.
BADGES = {
    "london":  ((214, 138, 46),  "LONDON"),
    "nyse":    ((58, 108, 196),  "NYSE"),
    "study":   ((132, 84, 176),  "STUDY"),
    "coding":  ((46, 158, 108),  "CODING"),
    "sleep":   ((70, 92, 140),   "SLEEP"),
    "focus":   ((196, 92, 60),   "FOCUS"),
}


def draw_badge(d, W, key):
    if key not in BADGES:
        return
    col, label = BADGES[key]
    f = font(30, "heavy")
    tw = d.textlength(label, font=f)
    pad_x, h = 22, 46
    x1, y1 = W - 40, 36
    x0 = x1 - (tw + pad_x * 2)
    d.rounded_rectangle([x0, y1, x1, y1 + h], radius=8, fill=col)
    d.text((x0 + pad_x, y1 + 7), label, font=f, fill=(255, 255, 255))


def thumbnail(plate_name, duration, function, path_out, sub=None, bias=0.5, badge=None):
    W, H = 1280, 720
    im = cover(plate(plate_name), W, H, bias)
    im = ImageEnhance.Color(im).enhance(1.10)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = hgrad_scrim(im)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 12, H], fill=AMBER)

    x = 62
    size = 152
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

    draw_badge(d, W, badge)
    im.save(os.path.join(OUT, path_out))
    print(f"{path_out}  ({plate_name})")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"→ {OUT}\n")
    thumbnail("deepwork-a-desk-glow",     "2 HOURS",   "Deep Work",    "thumb-deepwork.png",  "Calm baroque · 60 BPM")
    thumbnail("deepwork-b-library-fire",  "2 HOURS",   "Chart Analysis", "thumb-charts.png",  "Clear decisions, calm head")
    thumbnail("market-a-skyline-goldblue","6.5 HOURS", "NYSE Session", "thumb-nyse.png",      "Open to close, uninterrupted")
    thumbnail("market-b-window-desk-city","3 HOURS",   "The Overlap",  "thumb-overlap.png",   "London · New York")
    # Instrument in frame, deliberately. The fireplace plate got the 8h video filed
    # next to fireplace-ambience channels — 92% suggested traffic from them, 1.3% CTR,
    # and viewers arriving expecting crackle rather than baroque.
    thumbnail("sleepmusic-a-piano-moonlight", "8 HOURS",  "Sleep Music", "thumb-sleep.png",     "Original piano · no ads")
    thumbnail("sleepmusic-c-cello-window",    "10 HOURS", "Sleep Music", "thumb-sleep-10h.png", "Original strings · no ads")

    # September slate. Weighted to length after 1 Jun–27 Aug analytics: the 8h sleep
    # compilation turned 44 views into 26.7 hours watched, while every event-titled
    # trader video (FOMC, opening range, earnings) drew under 20 views and no search
    # traffic at all. Long and plainly-named is what the suggested feed picks up.
    #
    # Every one of these uses a sleepmusic-* or deepwork-* plate with the instrument in
    # frame, for the reason noted above: the hearth plate got its video shelved next to
    # fireplace-ambience channels and the arrivals were expecting crackle.
    thumbnail("sleepmusic-b-piano-keys-lamp", "10 HOURS", "Rain & Piano",  "thumb-rain-10h.png",     "Volume two · no ads")
    thumbnail("deepwork-b-library-fire",      "2 HOURS",  "Chart Analysis","thumb-charts4.png",      "Volume four · calm baroque")
    thumbnail("sleepmusic-a-piano-moonlight", "8 HOURS",  "Nocturnes",     "thumb-nocturnes.png",    "Original piano · no ads")
    thumbnail("sleepmusic-c-cello-window",    "10 HOURS", "Ocean & Piano", "thumb-ocean.png",        "Original piano · no ads")
    thumbnail("deepwork-a-desk-glow",         "3 HOURS",  "Study Music",   "thumb-study-3h.png",     "Calm baroque · 60 BPM")
    thumbnail("sleepmusic-c-cello-window",    "9 HOURS",  "Quiet Cello",   "thumb-cello-9h.png",     "Slow strings · no ads")
    thumbnail("sleepmusic-b-piano-keys-lamp", "10 HOURS", "Sleep Music",   "thumb-classical-v2.png", "Volume two · no ads")
    thumbnail("deepwork-c-cafe-window",       "4 HOURS",  "Monk Mode",     "thumb-monkmode2.png",    "Volume two · no distractions")
    thumbnail("sleep-b-cabin-snow",           "8 HOURS",  "Winter Piano",  "thumb-winter-8h.png",    "Snowfall · no ads")
    thumbnail("sleepmusic-a-piano-moonlight", "12 HOURS", "Sleep Music",   "thumb-sleep-12h.png",    "Piano and rain · no ads")
    thumbnail("deepwork-b-library-fire",      "6 HOURS",  "Deep Work",     "thumb-baroque-6h.png",   "Uninterrupted · no ads")
    thumbnail("sleepmusic-c-cello-window",    "9 HOURS",  "Quiet Strings", "thumb-strings-9h.png",   "Sleep and deep rest")

    # October slate. September's 7-sleep/5-focus split settled the lane question on ~580
    # views: sleep returned 11.3 min/view against focus's 3.8, so October is 10 and 2.
    # Every sleep tile puts the instrument in frame, for the reason above — the hearth
    # plate got its video shelved beside fireplace-ambience channels.
    thumbnail("sleepmusic-a-piano-moonlight", "10 HOURS", "Nocturnes",     "thumb-nocturnes2.png",   "Moonlight piano · no ads")
    thumbnail("deepwork-b-library-fire",      "3 HOURS",  "Study Music",   "thumb-study-3h2.png",    "Volume two · calm baroque")
    thumbnail("sleepmusic-c-cello-window",    "10 HOURS", "Ocean & Piano", "thumb-ocean-10h.png",    "Slow waves · no ads")
    thumbnail("sleepmusic-c-cello-window",    "9 HOURS",  "Slow Cello",    "thumb-cello-9h2.png",    "Quiet strings · no ads")
    thumbnail("sleepmusic-b-piano-keys-lamp", "8 HOURS",  "Rain & Piano",  "thumb-rain-8h.png",      "Volume three · no ads")
    thumbnail("sleepmusic-a-piano-moonlight", "10 HOURS", "Sleep Music",   "thumb-classical-3.png",  "Volume three · no ads")
    thumbnail("sleepmusic-b-piano-keys-lamp", "8 HOURS",  "Quiet Piano",   "thumb-piano-8h.png",     "Soft nocturnes · no ads")
    thumbnail("deepwork-a-desk-glow",         "6 HOURS",  "Deep Work",     "thumb-baroque-6h2.png",  "Volume two · uninterrupted")
    thumbnail("sleep-b-cabin-snow",           "10 HOURS", "Winter Piano",  "thumb-winter-10h.png",   "Snowfall · no ads")
    thumbnail("sleepmusic-c-cello-window",    "9 HOURS",  "Quiet Strings", "thumb-strings-9h2.png",  "Deep rest · no ads")
    thumbnail("sleepmusic-a-piano-moonlight", "8 HOURS",  "Forest Night",  "thumb-forest-8h.png",    "Calm piano · no ads")
    thumbnail("sleepmusic-b-piano-keys-lamp", "10 HOURS", "Sleep Music",   "thumb-sleep-10h-v2.png", "Piano under a quiet sky")
    print("\nDone.")
