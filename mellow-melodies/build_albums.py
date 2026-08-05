#!/usr/bin/env python3
"""Package the generated tracks into sellable albums for the Ko-fi shop.

The raw takes are already on disk as WAVs — the same material the videos are built
from. This turns them into something someone will pay for: tagged 320k MP3s and the
original WAVs, named properly, with a licence note and a readme, zipped per album.

Margin is the point. A £8 album on Ko-fi nets around £7.60; the equivalent effort in
Amazon affiliate commission is roughly forty headphone referrals. Same description
space, same audience.

    python3 build_albums.py            # build everything
    python3 build_albums.py --list     # show the plan without writing
"""
import os, shutil, subprocess, sys, zipfile

CH = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES"
BEDS = os.path.join(CH, "beds")
OUT = os.path.join(CH, "albums")

# Track titles are invented here because the generator's own titles were not kept when
# the takes were saved. They are thematic per album so a track listing reads as a
# deliberate record rather than a numbered dump.
ALBUMS = [
    {
        "slug": "deep-work-vol-1",
        "title": "Deep Work, Volume One",
        "price": "£8",
        "blurb": "Six tracks of slow baroque-influenced focus music, written to be left "
                 "running through a long working session. No vocals, no dynamic swells, "
                 "nothing that pulls your eyes off the screen.",
        "sources": ["w2tue-parts", "a-parts"],
        "count": 12,
        "names": ["Opening Range", "Linear Thinking", "The Quiet Terminal", "Sixty BPM",
                  "Chart Light", "Session Hold", "Slow Ledger", "Clean Signal",
                  "The Long Position", "Steady State", "Closing Bell", "After Hours"],
    },
    {
        "slug": "night-sessions",
        "title": "Night Sessions",
        "price": "£8",
        "blurb": "Slow solo piano for sleep and the end of a long day. Sparse, unhurried, "
                 "and deliberately without anything designed to wake you.",
        "sources": ["w2sun-parts", "w3sun-parts"],
        "count": 12,
        "names": ["Moonlit Reflection", "Low Cloud", "Still Water", "Embers",
                  "The Last Hour", "Snow at the Window", "Quiet Harbour", "Dim Lamp",
                  "Small Hours", "Drift", "Nightfall", "Rest"],
    },
    {
        "slug": "low-cortisol",
        "title": "Low Cortisol",
        "price": "£6",
        "blurb": "Sustained low strings for the moment after a bad decision. No crescendo, "
                 "nothing to strain toward — written to bring a raised heart rate down "
                 "rather than to energise.",
        "sources": ["w2thu-parts", "w4thu-parts"],
        "count": 8,
        "names": ["Reset", "Breath", "Ground", "Unwind",
                  "Slow Pulse", "Even Keel", "Let It Go", "Stand Down"],
    },
]

LICENCE = """MELLOW MELODIES — LICENCE

Thank you for buying this album. It directly funds new music and keeps the 24/7
stream running.

WHAT YOU MAY DO
  · Listen, anywhere, forever. The files are yours.
  · Use as background music in your own videos, streams and podcasts, with credit
    to Mellow Melodies.

WHAT YOU MAY NOT DO
  · Resell or redistribute the files.
  · Upload them as your own release to streaming platforms.

All music is original and produced by Mellow Melodies.
https://www.youtube.com/@mellowmelodies
"""


def tracks_in(folder):
    d = os.path.join(BEDS, folder)
    if not os.path.isdir(d):
        return []
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".wav"))


def build(album, dry=False):
    picked, seen = [], set()
    for src in album["sources"]:
        for t in tracks_in(src):
            if len(picked) >= album["count"]:
                break
            # skip near-duplicate takes from the same generation (…-a / …-b pairs)
            stem = os.path.basename(t).rsplit("-", 1)[0]
            if stem in seen:
                continue
            seen.add(stem); picked.append(t)
    if len(picked) < album["count"]:
        print(f"  ! only {len(picked)} tracks available for {album['title']}")

    print(f"\n{album['title']}  ({album['price']}) — {len(picked)} tracks")
    if dry:
        for i, t in enumerate(picked):
            print(f"   {i+1:2d}. {album['names'][i]}")
        return

    root = os.path.join(OUT, album["slug"])
    mp3d, wavd = os.path.join(root, "MP3"), os.path.join(root, "WAV")
    os.makedirs(mp3d, exist_ok=True); os.makedirs(wavd, exist_ok=True)

    for i, t in enumerate(picked):
        name = album["names"][i]
        num = f"{i+1:02d}"
        mp3 = os.path.join(mp3d, f"{num} {name}.mp3")
        if not os.path.exists(mp3):
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", t,
                "-c:a", "libmp3lame", "-b:a", "320k",
                "-metadata", f"title={name}",
                "-metadata", "artist=Mellow Melodies",
                "-metadata", f"album={album['title']}",
                "-metadata", f"track={i+1}",
                "-metadata", "genre=Ambient",
                mp3], check=True)
        wav = os.path.join(wavd, f"{num} {name}.wav")
        if not os.path.exists(wav):
            shutil.copy2(t, wav)
        print(f"   {num} {name}")

    with open(os.path.join(root, "LICENCE.txt"), "w") as f:
        f.write(LICENCE)
    with open(os.path.join(root, "README.txt"), "w") as f:
        f.write(f"{album['title']}\nMellow Melodies\n\n{album['blurb']}\n\n"
                f"{len(picked)} tracks · 320kbps MP3 and original WAV\n\n"
                "See LICENCE.txt for usage terms.\n")

    zpath = os.path.join(OUT, f"{album['slug']}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=1) as z:
        for base, _, files in os.walk(root):
            for fn in files:
                p = os.path.join(base, fn)
                z.write(p, os.path.relpath(p, root))
    mb = os.path.getsize(zpath) / 1048576
    print(f"   → {album['slug']}.zip  ({mb:.0f} MB)")


if __name__ == "__main__":
    dry = "--list" in sys.argv
    if not dry:
        os.makedirs(OUT, exist_ok=True)
    for a in ALBUMS:
        build(a, dry)
    if not dry:
        print(f"\n→ {OUT}")
