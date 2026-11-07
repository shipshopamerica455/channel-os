# genius-junkie-editor

Claude Code editing pipeline for the **Genius Junkie** tutorial channel.
Modeled on hassancs91/claude-youtube-editor, rebuilt around what this channel
actually is: real screen recordings (Canva, CapCut, AI tools), not talking-head
+ fake screencasts. Fully local — Whisper transcription, ffmpeg renders, Pillow
thumbnails. £0 per video.

## Quick start

```bash
# 1. drop a recording in
mkdir -p videos/my-tutorial && cp ~/Desktop/recording.mp4 videos/my-tutorial/source.mp4

# 2. run everything
python3 tools/run_all.py videos/my-tutorial

# 3. package + upload (via Claude Code skills)
#    /gj-package   → titles, chapters, description, thumbnails
#    /gj-publish   → verified upload, private draft, channel-guarded
```

Or just tell Claude Code: *"edit videos/my-tutorial"* — the `/gj-edit` skill
runs the pipeline and does the judgment work (bad-take kills, zoom review) that
scripts can't.

## What each stage does

| Stage | Output | What it does |
|---|---|---|
| `transcribe.py` | `transcript.json` | word-level timestamps, local Whisper |
| `plan_cuts.py` | `cuts.json` | silences + filler words + `kills.json` bad takes |
| `apply_cuts.py` | `master.mp4` | frame-accurate splice, rebased transcript |
| `motion_map.py` | `activity.json` | frame-diff map of where the screen changes |
| `plan_zooms.py` | `zooms.json` | shot list: punch in on the action, wide to re-orient |
| `apply_zooms.py` | `zoomed.mp4` | eased zooms, single encode pass |
| `captions.py` | `captioned.mp4` | word-timed captions, live word in brand yellow |
| `polish.py` | `final.mp4` | 2-pass −14 LUFS, optional denoise/music/bumpers |
| `make_thumbs.py` | `thumbnail-{A,B,C}.png` | 3 variants off high-activity frames |
| `chapters.py` | `description.txt` | chapters + SEO description |
| `shorts.py` | `shorts/*.mp4` | 9:16 clips, crop follows the on-screen action |
| `verify.py` | — | A/V drift, stale captions, dead starts |

Skills in `.claude/skills/`: `gj-edit`, `gj-cut`, `gj-zoom`, `gj-captions`,
`gj-package`, `gj-shorts`, `gj-publish`.

Uploader: `../remotion-shorts/upload-geniusjunkie.mjs` (own OAuth token,
hard-locked to the Genius Junkie channel ID).

Brand knobs all live in `brand.json`.
