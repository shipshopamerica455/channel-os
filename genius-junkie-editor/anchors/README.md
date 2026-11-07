# anchors/ — what "on brand" actually looks like

**Read this folder before coding scenes or a thumbnail. Look at the images, not
just the filenames.**

Prose style guides don't stop drift. `HANDOFF-PRODUCTION.md` and
`feedback-thumbnail-geniusjunkie` both described the house thumbnail correctly,
and videos #16 and #17 still shipped off-brand — the drift was only caught when
the user put the uploads grid side by side and said *"looks very different from
the other thumbnails."* A described standard is not a standard you can check
against. These files are.

Anything marked **CANONICAL** is the reference. When in doubt, copy it.

---

## thumbnails/

`01-calendar-CANONICAL.png` — the locked skeleton. Every long-form thumbnail is
this layout with different content:

- hero photo at **full opacity** under a left-to-right scrim
  (`rgba(20,24,29,0.94) 0% → 0.60 48% → 0 74%`) — never dim the photo itself
- headline left/top, `FONT_DISPLAY` 900 at **116px**, `#ffdd00`, `stroke(6)`
- kicker **below** the headline, **white at 38px**, `stroke(4)` — never above it
  in small yellow caps
- **three green ✓ bullets** at `top: 470`
- yellow **TUTORIAL** tag rotated 3°, `left: 470, bottom: 24`
- **GENIUS JUNKIE** logo + wordmark, `left: 44, bottom: 22`
- proof art in a **white card, 6px `#e91e8c` border**, big drop shadow, at
  `right: 34, top: 74` — grey label line, ~364px-wide art, `#c2185b` line under

`02-teachers.png`, `03-scrapbook.png` — the two that drifted, rebuilt to match.
Useful as before/after evidence that the skeleton is what makes them a set.

`04-presentation.png` — most recent.

## scenes/

`01-proof-card-CANONICAL.png` — the standard long-form scene: a proof object on
one side, a kicker + note on the other, section chip top-left. The kicker is
`FONT_MONO` 700 24px in accent pink, the body `FONT_BODY` 30px `#e7ecf5`.

`02-demo-plus-two-notes.png` — a diagram carrying the argument with two stacked
notes beside it. Note the diagram is *doing* something (the white sliver only
appears in the no-bleed state) rather than decorating.

`03-list-slide.png` — a full-width list. **This one is here because it was wrong
first:** the reveals lagged the narration and two-thirds of the frame was empty.
It's the fixed version. If a slide looks emptier than this, it's too empty.

---

## The rules these encode

1. **Fill the frame.** A 1920×1080 frame with content only in the top-left third
   reads as a mistake. Both defects in the lookbook build were dead space.
2. **Reveals track the voice.** If the narration says it, it should already be on
   screen — not a second and a half later.
3. **The visual carries the argument.** A diagram that could be replaced by a
   caption isn't earning its place.
4. **Thumbnails are one skeleton, not a fresh design per video.** A viewer
   scanning the uploads grid should recognise the channel before reading a word.

## Adding to this folder

Add a frame when it's the *best* example of a pattern, not just the newest.
Prune anything superseded — a folder of twenty near-identical frames teaches
less than four sharp ones. Keep the **CANONICAL** marker on exactly one file per
subfolder.
