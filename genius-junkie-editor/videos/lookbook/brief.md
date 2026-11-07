# Brief — SLATE 2 COMPLETE — all ten rows shipped. Regenerate SLATE-EVIDENCE.md before ranking slate 3.

_Generated 2026-09-01 by `gj brief`._

## The job
Write `script.md` for this video. When it's done run `gj build lookbook`.

## Hard numbers
- Voice: Kokoro `bm_fable` — measured **3.7 words/sec**.
- Target runtime **8.7 min** ⇒ **~1859 words** of VO total.
- Must clear **8:00** so two mid-rolls are allowed. Under-writing is the #1 cause of a re-record.
- 13–15 sections. Two DESIGNED AD BREAKS: after the section ending ~40% in, and ~72% in.

## Required shape (each `## SNN — TITLE (~N words)` then a `>` quoted block)
1. **S01 HOOK** (~110 w) — the cost of getting it wrong, then "here's what we're building".
2. **S02** — the 2–3 principles that make the rest make sense.
3. **S03–S05** — setup and the main build. S05 is full say-it-show-it.
   → **AD BREAK 1** after S05.
4. **S06** — the payoff/"the trick I promised". This is the section the Shorts come from.
5. **S07–S09** — the rules, the polish, the export.
   → **AD BREAK 2** after S09.
6. **S10–S11** — the system/scale play.
7. **S12** checklist · **S13** the £4.99 pack CTA · **S14** outro + end screen.

## Before you code a single scene — LOOK at anchors/
Open `anchors/` and actually look at the images. The CANONICAL thumbnail and
scene frames are the standard; prose did not stop videos #16 and #17 shipping
off-brand, side-by-side comparison did. Copy the skeleton, change the content.

## QA is section-aware now — use it
`gj qa lookbook` samples three frames INSIDE every section and tiles them nine
to a sheet, each labelled `S07 · 4:11`. READ the sheets before rendering.
Look for: dead space (content only in one corner), and reveals that lag the
narration. Those are the two defects this pipeline actually produces.
`--per-section N` for density, `--uniform` for the old even sampling.

## Style laws (non-negotiable — see HANDOFF-PRODUCTION.md)
- Say-it-show-it: every instruction must be visible on screen as it's spoken.
- A visual change every 3–6 s. No still frame longer than 6 s.
- Numbers written phonetically ("twelve point five two") — local TTS mangles digits.
- Bright by default; dark only as a deliberate beat.
- Name the real trap. Every video needs one fact competitors get wrong.

## Fact-check before writing
Run these and cite what you find in a "Facts verified" block at the top of script.md:
- [ ] <the platform's current limits/specs>
- [ ] <the pricing or fee that changed>
- [ ] <the rule people get wrong>

## Cutaway budget (HARD RULE)
4–6 Flow photo cutaways placed on **emotional** lines, never over an instruction.
Add them to `video.json` → `images[]` with a prompt each, then `gj images lookbook`.

## Product
Every video ships a £4.99 pack: an editable Canva template + generated PDFs.
Sketch what's in it at the bottom of script.md so `make_*_pack.py` can be written.
