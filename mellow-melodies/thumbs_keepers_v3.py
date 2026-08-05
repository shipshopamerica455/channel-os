#!/usr/bin/env python3
"""v3 thumbnails for the 9 legacy keepers, named by video ID for unambiguous upload.

Plate choice is driven by the video's actual content, not by house style. The keepers
are morning/Bach material, so they get the morning plates — a midnight hearth under a
title reading "Morning with Bach" is worse than the flat tile it replaces.

The four 3-minute videos lead on the FUNCTION rather than the duration: "3 MINUTES" is
an argument against clicking, where the longer videos' runtime is the selling point.

    python3 thumbs_keepers_v3.py
"""
import os
from thumbs_v3 import thumbnail, OUT

# (video_id, plate, headline, function, subtitle)
KEEPERS = [
    ("3j35cN4zhFs", "deepwork-b-library-fire",   "6 HOURS",  "Deep Work",     "Calm baroque, uninterrupted"),
    ("RVYk2p9zeyo", "morning-a-desk-sunrise",    "2.5 HOURS", "Pre-Market",   "Before the bell"),
    ("3klOUZYoSMg", "sleep-c-lake-moon-cabin",   "38 MIN",   "Moonlit Piano", "Reflections, Vol. 1"),
    ("jvRzSZzJJAw", "morning-b-coffee-window",   "29 MIN",   "Morning Focus", "Baroque masterpieces"),
    ("_n4mJBxrPx0", "morning-c-garden-path",     "29 MIN",   "Morning Focus", "Energy and concentration"),
    ("v24hsuDOw4M", "morning-e-forest-path",     "CLARITY",  "Morning Walk",  "Classical for a clear head"),
    ("fN21SoxwCRo", "morning-f-fountain-courtyard", "ENERGY", "Uplifting",    "Baroque for positive energy"),
    ("vQrqicxLw3Q", "morning-d-spring-blossom",  "FOCUS",    "Springtime",    "Beautiful classical strings"),
    ("2_NRrjtMr4s", "morning-c-garden-path",     "MORNING",  "Royal Garden",  "Uplifting Bach"),
]

if __name__ == "__main__":
    out = os.path.join(OUT, "keepers")
    os.makedirs(out, exist_ok=True)
    for vid, plate, head, fn, sub in KEEPERS:
        thumbnail(plate, head, fn, os.path.join("keepers", f"{vid}.png"), sub)
    print(f"\n→ {out}")
