# genius-junkie-editor

Editing pipeline for the **Genius Junkie** YouTube channel
(`UCz8eVGSEicfswKIe4XAp7Kw`) — Canva / CapCut / AI-design tutorials built on
screen recordings. Raw recording in, uploadable video out. Everything runs
locally: Whisper for transcription (no API cost), ffmpeg for every render,
Pillow for thumbnails.

## The pipeline

```
videos/<slug>/source.mp4                 the raw screen recording
  → transcribe.py   transcript.json      word-level timestamps (local Whisper)
  → plan_cuts.py    cuts.json            silences + fillers + kills.json  ← REVIEW
  → apply_cuts.py   master.mp4           + transcript.cut.json (rebased)
  → motion_map.py   activity.json        where the screen is changing
  → plan_zooms.py   zooms.json           shot list                        ← REVIEW
  → apply_zooms.py  zoomed.mp4           eased punch-ins, single encode
  → captions.py     captioned.mp4        word-timed brand captions
  → polish.py       final.mp4            2-pass loudnorm, music, bumpers
  → verify.py                            A/V drift, stale transcript, dead start
```

One command: `python3 tools/run_all.py videos/<slug>` — stages skip when their
output exists; `--from <stage>` restarts mid-way; `--force` redoes.

## Skills

`/gj-edit` end-to-end · `/gj-cut` · `/gj-zoom` · `/gj-captions` ·
`/gj-package` titles/chapters/thumbs · `/gj-shorts` · `/gj-publish`

## House rules

- **Plan files are the interface.** cuts.json / zooms.json / chapters.json /
  shorts.json are data to be reviewed and hand-edited; renders are disposable.
  Never hand-edit an .mp4 outside the pipeline — transcript.cut.json must always
  match master.mp4 or captions and Shorts drift.
- **Brand lives in brand.json only.** Colors (Genius Junkie pink `#e91e8c`,
  yellow `#ffdd00`, ink `#0f172a`), caption style, cut/zoom defaults, loudness
  targets. Change it there so every video matches.
- **Cheap stages first.** Transcribe + plan cost nothing to redo; renders cost
  minutes. Review the plan files before rendering, fix bad takes via kills.json.
- **`anchors/` is the style contract you can SEE.** Look at the images before
  coding scenes or a thumbnail — prose didn't stop #16 and #17 drifting
  off-brand. Anything marked CANONICAL is the reference; copy it.
- **`gj qa <slug>` samples per SECTION, not evenly** — three frames inside each
  section, nine to a sheet, tiles labelled `S07 · 4:11`. Read the sheets before
  rendering and look for the two defects this pipeline actually produces: dead
  space, and reveals lagging the narration. `--per-section N` / `--uniform`.
- **Every generated cutaway must be placed.** `video.json` lists the Flow
  prompts and the scenes are written separately, so nothing used to compare
  them — three videos shipped with unplaced images, and the photo album went out
  with THREE cutaways against a house rule of four to six. `gj qa` and
  `gj render` now run `checkCutaways` and warn by name; `gj cutaways <slug>`
  runs it standalone. Do not write five prompts and place four.
- **Third-party pricing is a fact, not a flourish.** Any claim about what a
  platform charges (Etsy/KDP/TPT/Stripe fees, Canva Pro pricing, print costs)
  must be checked against the platform's own fee page in the same session the
  script is written, and written as a floor not a total — "the £0.20 listing
  fee" not "£0.20 and nothing else". A viewer caught the wall-art script
  claiming a sale costs 20¢ and nothing else when it is nearer 17%; that is the
  kind of error that costs a tutorial channel its credibility.
- **A re-upload replaces a file YouTube will not let you swap** — so it always
  means: upload the fix as a NEW private draft with **no publishAt**, then get
  the old one deleted. Before handing over, **retitle the superseded video to
  `DELETE THIS - <original title>`** via the API. Do not ask the user to tell
  two identical drafts apart by ID, thumbnail or schedule status — they are
  identical by design, and it cost two false starts on the lookbook. The
  rename is one API call and removes the ambiguity completely. Never delete
  the old video yourself; that is the user's call. Mid-roll positions do NOT
  survive and are not reachable via the API — say so explicitly every time.
- **Name the trap in the first 30 seconds, and again at S06.** Channel AVD is
  ~1:16 on ~8:30 videos, so a trap first revealed at 3:09 and a CTA at 8:08 are
  seen by almost nobody. S01 carries the claim and the free-asset line as if no
  one watches another second; S06 keeps the full demonstration and remains the
  Shorts source. This trades a little AVD for reach of the offer, which is the
  right trade at a £3.23 RPM where one £4.99 sale ≈ 1,545 views of ad money.
- **The free rung is NEW, never carved out of the paid pack.** The free asset
  exists to create appetite for the £4.99 pack — a one-page checklist, a
  decision sheet, a settings card that references the pack. Do NOT strip an
  artefact out of an existing pack to use as the lead magnet: the pack is the
  only revenue that converts the same week, and the list is a 12–18 month
  compounding play. Build alongside it, not out of it.
- **Shorts slots are ALLOCATED, never assumed.** Four Shorts at one slot a day
  cannot fit a 2-day long-form cadence — consecutive videos collide on days +3
  and +4 every single time, and two releases had to be unpicked by hand before
  anyone noticed. `publish` now asks YouTube what is occupied
  (`remotion-shorts/gj-scheduled-slots.mjs`) and walks a ladder of 12:00 / 19:00
  until it finds free slots, refusing rather than double-booking.
  **Never trust packaging.json for occupancy** — it records what the pipeline
  intended, so anything moved by hand leaves it stale. If you must reconcile
  local files to reality, match by video TITLE, not by slot: "is this slot
  live?" is true even when a different video owns it, which silently leaves the
  wrong entry in place.

- **Music is opt-in, and it stops at the ad breaks.** `gj music <slug>` renders
  a procedural bed (`pipeline/audio/`, lifted from the aiTrends 2D studio
  plugin — numpy/scipy, no API, no licence) and `master` mixes it only if
  `bed.wav` exists, so nothing changes for a video until you ask. The bed sits
  ~22 dB under the voice, lifts only for S06 (the trap), and is gapped across
  both designed ad windows — `master` applies the mute and the loudnorm AFTER
  the mix and then re-verifies with `silencedetect`, because YouTube refuses
  manual mid-rolls where the audio is not silent. A published video cannot have
  its file swapped, so this only ever applies to the next render.

- **Credentials never live in source here.** This folder sits beside a PUBLIC
  git remote, and the Ghost admin key — full write access to the live site —
  was hardcoded in three files until 7 Nov 2026. It now comes from
  `pipeline/lib/ghost-key.mjs`, which reads `GHOST_ADMIN_KEY` out of the
  gitignored `remotion-shorts/.env` — the one copy on disk, the same one
  `gj-health-check.mjs` reads — and throws if it is missing. Import
  `ghostToken()`; never paste a key, and never add a fallback literal, because
  a wrong-but-present key fails as a 401 halfway through a publish. The
  paid-kit path prefix works the same way, via `kitBase()`, and so do the Canva
  template share links — **they are the product** — via `canvaLinks()` and
  gitignored `pipeline/canva-links.json`. Page sources use `CANVA_LINK`,
  `KIT_BASE` and `STRIPE_LINK` placeholders that `commerce()` fills at publish
  time; a kit with two templates uses `CANVA_LINK_DESKTOP` / `_LETTER`, and the
  resolver replaces the longest placeholder first on purpose.

- **Titles:** always 3 options (A search-intent, B qualifier, C pain-point) with
  a recommendation. Search-led, not curiosity-led — this is a tutorial channel.
- **Uploads:** via `../remotion-shorts/upload-geniusjunkie.mjs`, private draft
  by default, channel-guarded to Genius Junkie. Ask before scheduling/public.
- Whisper models: `small.en` default; `base.en` for >30-min recordings;
  `medium.en` only if the audio is rough.
- Temp/experiment files go in the session scratchpad, not in videos/.
