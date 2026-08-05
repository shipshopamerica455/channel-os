# Mellow Melodies — Image Prompts

Generate these, hand me the files, and I'll composite the type and export upload-ready
sizes. **Don't let the model render any text** — image models garble lettering, and a
misspelled channel name on a banner is unrecoverable. All type gets drawn in code by
[build_brand.py](build_brand.py).

Run them through Flow with [gen-brand-bg.mjs](gen-brand-bg.mjs), or paste into any
image model.

---

## The shared style block

Prepend this to every prompt below.

> Cinematic photograph, shallow depth of field, nocturnal. Deep near-black navy
> (#0E1420) dominates the frame, lit by a single warm amber light source (#E0A340).
> Muted, restrained, expensive. Calm and still — nothing urgent, nothing dramatic.
> High quality, realistic, not illustrated, not a 3D render.
>
> NO text, letters, numbers, words, signage, watermarks or logos anywhere in the image.
> No screens showing charts, candlesticks, graphs, tickers or trading terminals. No
> faces looking at camera, no posed people, no stock-photo styling. No neon, no teal-
> and-orange grade, no lens flare.

**Why no charts.** The audience is buying relief from a screen full of candlesticks. A
green candle in the corner of a video sold on emotional regulation works against the
product. This holds for every asset, including the trading-session videos.

---

## 1. Channel banner background — `banner-bg.png`

**16:9.** Only the centred **1546×423** strip is visible on phones, so that horizontal
band through the middle must stay dark and quiet — the channel name sits there.

> A city seen from a high window in the last hour before dawn. Deep blue-black sky,
> a scatter of small warm window lights far below, low mist between the buildings.
> Shot from inside a dark room so the lower and upper edges of the frame fall into
> heavy shadow.
>
> CRITICAL COMPOSITION: the central horizontal third of the frame must be dark, plain
> and almost empty — deep shadow, minimal detail — because large text will be placed
> across it. Visual interest belongs at the top and bottom edges only.

**Alternate — `banner-bg-alt.png`:**

> A grand concert hall at night, empty, seen from the rear of the stalls. Rows of
> seats falling away into darkness, a single warm amber work-light burning on the far
> stage. Dust in the beam. Vast, silent, still. The centre of the frame is deep shadow;
> the only detail sits along the top and bottom edges.

That second one bridges the classical heritage the 1,117 existing subscribers signed up
for, so it's the safer of the two if the pivot feels abrupt.

---

## 2. Logo mark — `logo-concept-*.png`

**1:1.** The code-drawn mark already works and holds at 48px, so treat these as
challengers rather than replacements. Full-bleed dark ground, no white background —
YouTube circle-crops it.

> **a — steady line.** A single horizontal band of warm amber light stretched across a
> deep near-black field, perfectly level and even, softly blurred at both ends. Minimal,
> symmetrical, centred. Nothing else in the frame. Full-bleed dark background to the
> very edges.

> **b — struck string.** An extreme macro of a single piano string in deep shadow, lit
> by one warm amber highlight running along its length. Abstract, almost unreadable as
> an object. Centred and symmetrical, full-bleed dark background.

> **c — arc.** A slow warm amber arc of light curving through darkness, like a long
> exposure of a single moving point. Simple enough to read at thumbnail size. Centred,
> full-bleed near-black background.

Judge every one of these circle-cropped at **48px** before falling in love with it. That
is the size it lives at in a subscription feed, and detail below ~88px collapses.

---

## 3. Thumbnail backgrounds

**16:9.** Duration is the largest element on the finished tile and sits centre, so keep
the middle dark and put texture at the edges. One per content pillar, reused across
uploads so the channel reads as a set.

**`thumb-bg-deepwork.png`** — Tue/Thu functional videos

> A dark wooden desk lit by one warm amber lamp just out of frame. A closed notebook
> and a pen, deliberately out of focus. No screen, no monitor, no keyboard. Early hours,
> curtains drawn. The centre of the frame is empty desk surface in low light.

**`thumb-bg-session.png`** — the market-session videos

> Rain running down a tall window at night, a warm amber interior light reflected and
> smeared in the water. The city beyond is soft, dark and unfocused. Quiet and enclosed.
> The centre of the frame is the darkest, plainest area.

**`thumb-bg-sleep.png`** — Sunday long-form

> A still lake at night under low cloud, a single warm point of light on the far shore
> reflected in the water. No moon disc, no stars, no drama. Almost monochrome deep
> blue-black. The centre of the frame is flat, calm water in shadow.

---

## 4. Video backgrounds (Veo first frames)

**16:9.** These become the actual video visuals — generate the still, then animate it
with Veo image-to-video and loop it long. Per [AUTOMATION.md](AUTOMATION.md), a static
image held for six hours is the exact profile YouTube's inauthentic-content policy
screens for, so these must move.

Use the same three scenes as the thumbnails so tile and video match, but **without** the
"keep the centre empty" constraint — nothing is overlaid on these, so let them be
properly composed.

Motion prompts for the Veo pass, all deliberately near-still:

- *"Rain continues to run down the glass. The reflected light shimmers very slightly. The camera does not move."*
- *"Dust drifts slowly through the lamp light. Almost imperceptible drift. The camera holds completely still."*
- *"The water moves almost imperceptibly. The reflected light ripples slowly. The camera holds completely still."*

Restraint is the whole point — this plays for hours behind someone's work. Any camera
move that's noticeable once is unbearable by the fortieth repetition.

---

## What I'll do with them

Drop the files anywhere in the MELLOW MELODIES folder and tell me. I'll composite the
type over them, check the banner against the 1546×423 safe area and the logo at 48px,
and export: `banner.png` 2560×1440, `avatar.png` 800×800, and the thumbnail set at
1280×720.
