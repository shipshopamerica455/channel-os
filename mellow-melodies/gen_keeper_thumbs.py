#!/usr/bin/env python3
"""New thumbnails for the 9 long-form keepers, in the rebranded system.

The existing tiles are ornate gold-framed AI Bach portraits with serif lettering.
Two problems with leaving them: they now clash with the new banner and mark, so the
channel reads as two brands stacked; and that specific look — a costumed AI composer
in a gilt frame, repeated across every tile — is the visual signature reviewers
associate with mass-produced content.

Filenames carry the video ID so each one is unambiguous to upload.

    python3 gen_keeper_thumbs.py
"""
import os
from build_final import thumbnail, FINAL

# (video_id, plate, duration, function, subtitle, crop bias)
# Duration leads on anything an hour or over — that is the buying decision. Below an
# hour it is a weak hook, so those tiles lead on the function instead.
KEEPERS = [
    ("3j35cN4zhFs", "line",     "6 Hours",    "Deep Work",    "Calm baroque · uninterrupted", 0.50),
    ("RVYk2p9zeyo", "skyline",  "2.5 Hours",  "Pre-Market",   "Before the bell",              0.45),
    ("3klOUZYoSMg", "desk_lib", "38 Minutes", "Sleep",        "Moonlit piano · Vol. 1",       0.50),
    ("jvRzSZzJJAw", "hall",     "28 Minutes", "Morning Focus", "Baroque masterpieces",        0.42),
    ("_n4mJBxrPx0", "skyline",  "28 Minutes", "Morning Focus", "Baroque for concentration",   0.55),
    ("v24hsuDOw4M", "line",     "Clarity",    "Short Session", "Classical for a clear head",  0.50),
    ("fN21SoxwCRo", "line",     "Energy",     "Short Session", "Uplifting baroque",           0.50),
    ("vQrqicxLw3Q", "line",     "Focus",      "Short Session", "Beautiful classical strings", 0.50),
    ("2_NRrjtMr4s", "line",     "Morning",    "Short Session", "Uplifting Bach",              0.50),
]

if __name__ == "__main__":
    out = os.path.join(FINAL, "keepers")
    os.makedirs(out, exist_ok=True)
    for vid, plate, dur, fn, sub, bias in KEEPERS:
        thumbnail(plate, dur, fn, os.path.join("keepers", f"{vid}.png"), sub, bias=bias)
    print(f"\n→ {out}")
