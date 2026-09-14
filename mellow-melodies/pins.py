#!/usr/bin/env python3
"""Pinterest pins for the published catalogue.

    python3 pins.py            # build pins + manifest
    python3 pins.py --limit 5  # just a few, to look at first

Pinterest is a search engine that happens to look like a mood board, which suits this
catalogue: pins persist for years, and "sleep music" and "study playlist" are real
queries there. It is also the one external channel worth trying on evidence — external
referrals watch 46.5 min/view against 9.2 for YouTube's own suggested feed, though that
rate rests on only 14 views and should be treated as a hint, not a number.

Two things the existing art cannot do, so this builds around them:

  · Everything on this channel is 16:9. Pinterest ranks 2:3 vertical and buries
    landscape. Cropping an 8-hour-sleep plate to 2:3 throws away the composition, so
    the image sits in the upper two-thirds and the title takes a brand-coloured block
    beneath it — the standard pin shape, and it reads at feed size.

  · A pin is a search result. The description carries the query terms someone would
    actually type, not the YouTube title, which is written for a different feed.

Images land in brand/pins/ and a manifest at brand/pins/pins.csv. Note that Pinterest's
bulk-upload CSV needs a PUBLIC image URL — it cannot read local files — so either upload
these by hand (about half an hour for thirty) or host the folder first and fill in the
media_url column. The manifest doubles as the checklist either way.
"""
import csv
import json
import re
import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageEnhance

from build_brand import font, INK, AMBER, CREAM
from build_final import cover
from covers_v1 import serif

CH = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES"
OUT = os.path.join(CH, "brand", "pins")
W, H = 1000, 1500
IMG_H = 940                      # image occupies the top ~63%

# Which plate suits which playlist. Cover plates first — a painterly musician reads far
# better on a mood board than a photographic empty room.
PLATES = {
    "sleep": [("cover-plates", "sleep-a-pianist-moonlight"),
              ("cover-plates", "sleep-b-cellist-window"),
              ("cover-plates", "sleep-c-pianist-firelight"),
              ("thumb-plates", "sleepmusic-a-piano-moonlight"),
              ("thumb-plates", "sleepmusic-c-cello-window")],
    "deepwork": [("thumb-plates", "deepwork-b-library-fire"),
                 ("thumb-plates", "deepwork-a-desk-glow"),
                 ("thumb-plates", "deepwork-c-cafe-window")],
    "charts": [("thumb-plates", "deepwork-a-desk-glow"),
               ("thumb-plates", "deepwork-b-library-fire")],
    "sessions": [("thumb-plates", "market-a-skyline-goldblue"),
                 ("thumb-plates", "market-b-window-desk-city")],
}

# Pinterest queries this catalogue can plausibly rank for, by playlist. Deliberately
# plain: nobody searches Pinterest for "low-cortisol focus music".
KEYWORDS = {
    "sleep": ["sleep music", "music for sleeping", "relaxing piano", "sleep playlist",
              "insomnia help", "calm music", "night routine"],
    "deepwork": ["study music", "focus music", "deep work", "concentration music",
                 "study playlist", "productivity"],
    "charts": ["study music", "focus music", "background music for work",
               "concentration playlist"],
    "sessions": ["focus music", "work playlist", "background music", "study session"],
}
BOARDS = {"sleep": "Sleep Music", "deepwork": "Study & Focus Music",
          "charts": "Study & Focus Music", "sessions": "Music for Working"}


def plate(group, name):
    return Image.open(os.path.join(CH, "brand", group, f"{name}.png")).convert("RGB")


def hours_label(minutes):
    """Runtime as the listing states it — 11h58m is sold as 12 hours, not 11."""
    h = minutes / 60
    if h < 1:
        return f"{minutes} MINUTES"
    return f"{round(h)} HOURS" if abs(h - round(h)) < 0.1 else f"{h:.1f} HOURS"


GENERIC = {"sleep music", "focus music", "study music", "deep work", "monk mode",
           "sleep", "focus", "music"}


def pin_headline(title):
    """The distinctive half of the title, with the runtime stripped.

    The badge above already states the hours, so "12 Hours of Sleep Music" reduces to
    "Sleep Music" — which is the board name, not a headline. When the part before the
    em dash collapses to something generic like that, the specific promise is in the
    half after it ("Piano and Rain Through the Whole Night"), so use that instead.
    """
    parts = [p.strip() for p in str(title).split(" — ")]
    strip_hours = lambda t: re.sub(
        r"^\s*\d+(?:\.\d+)?\s*(?:hours?|minutes?)\s+of\s+", "", t, flags=re.I).strip()

    head = strip_hours(parts[0])
    if head.lower().rstrip(",.") in GENERIC and len(parts) > 1:
        alt = strip_hours(parts[1])
        # Drop trailing sales furniture the image already says.
        alt = re.sub(r"[,\s]*\bno ads\b\.?$", "", alt, flags=re.I).strip(" ,.")
        if alt:
            head = alt
    return head[:1].upper() + head[1:] if head else head


def build_pin(slot, s, group, name, out_path):
    im = Image.new("RGB", (W, H), INK)
    art = cover(plate(group, name), W, IMG_H, 0.5)
    art = ImageEnhance.Color(art).enhance(1.06)
    im.paste(art, (0, 0))

    d = ImageDraw.Draw(im)
    # Fade the image into the text block so the join is not a hard line.
    for i in range(120):
        y = IMG_H - 120 + i
        d.line([(0, y), (W, y)], fill=tuple(
            int(a + (b - a) * (i / 120)) for a, b in zip((0, 0, 0), INK)), width=1)

    y = IMG_H + 54
    dur = hours_label(s.get("minutes", 0))
    f = font(52, "heavy")
    w = d.textlength(dur, font=f)
    d.text(((W - w) / 2, y), dur, font=f, fill=CREAM)
    y += 78
    d.rectangle([W // 2 - 70, y, W // 2 + 70, y + 4], fill=AMBER)
    y += 40

    head = pin_headline(s.get("title", ""))
    size = 62
    fs = serif(size)
    lines = textwrap.wrap(head, width=22) or [head]
    while (len(lines) > 3 or max(d.textlength(l, font=fs) for l in lines) > W - 120) and size > 34:
        size -= 3
        fs = serif(size)
        lines = textwrap.wrap(head, width=int(22 * 62 / size)) or [head]
    for line in lines[:3]:
        lw = d.textlength(line, font=fs)
        d.text(((W - lw) / 2, y), line, font=fs, fill=(236, 199, 132))
        y += size + 12

    tag = "NO ADS  ·  ORIGINAL MUSIC"
    ft = font(26, "demi bold")
    tw = sum(d.textlength(ch, font=ft) for ch in tag) + 6 * (len(tag) - 1)
    x = (W - tw) / 2
    for ch in tag:
        d.text((x, H - 92), ch, font=ft, fill=(150, 163, 182))
        x += d.textlength(ch, font=ft) + 6

    im.save(out_path, quality=92)


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    os.makedirs(OUT, exist_ok=True)
    cal = json.load(open(os.path.join(os.path.dirname(__file__), "calendar.json")))
    rows, made, counters = [], 0, {}

    for slot, s in cal.items():
        if slot.startswith("_") or not isinstance(s, dict):
            continue
        vid = s.get("published")
        if not vid or vid == "pending":
            continue
        pl = s.get("playlist", "sleep")
        opts = PLATES.get(pl) or PLATES["sleep"]
        i = counters.get(pl, 0)
        counters[pl] = i + 1
        group, name = opts[i % len(opts)]

        fn = f"pin-{slot}.jpg"
        try:
            build_pin(slot, s, group, name, os.path.join(OUT, fn))
        except FileNotFoundError:
            print(f"  {slot}: plate {group}/{name} missing — skipped")
            continue

        # Two different strings on purpose. The Pinterest title keeps the runtime,
        # because "10 hours of sleep music" is a query people type; the image drops it,
        # because the badge above the headline already says it. They were silently
        # different before, which made a pin impossible to find in the manifest by the
        # only thing visible on it — so the image's own words get their own column.
        head = str(s.get("title", "")).split(" — ")[0]
        on_image = pin_headline(s.get("title", ""))
        kw = KEYWORDS.get(pl, KEYWORDS["sleep"])
        desc = (f"{head}. Uninterrupted original music, no ads and no talking — "
                f"put it on and leave it running. {', '.join(kw[:5])}.")
        rows.append({
            "slot": slot,
            "text_on_image": on_image,
            "title": head[:100],
            "board": BOARDS.get(pl, "Sleep Music"),
            "description": desc[:500],
            "link": f"https://youtu.be/{vid}",
            "image_file": fn,
            "media_url": "",          # fill in once the folder is hosted, for bulk CSV
            "keywords": ", ".join(kw),
        })
        made += 1
        print(f"  {fn}  {BOARDS.get(pl,'')}  ({group}/{name})")
        if limit and made >= limit:
            break

    with open(os.path.join(OUT, "pins.csv"), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)

    boards = sorted({r["board"] for r in rows})
    print(f"\n{made} pins → {OUT}")
    print(f"manifest: {os.path.join(OUT, 'pins.csv')}")
    print(f"boards to create first: {', '.join(boards)}")


if __name__ == "__main__":
    main()
