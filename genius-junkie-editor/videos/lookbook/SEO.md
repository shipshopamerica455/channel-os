# SEO — Lookbook (video 19)

## Titles (3 options)

**MAIN (A · search-intent) — RECOMMENDED**
How to Make a Lookbook in Canva 2026 — Print-Ready A4 (Bleed + Colour)

**B (qualifier)**
Canva Lookbook Tutorial — Spreads, Bleed and the Export Settings

**C (pain-point)**
Your Canva Lookbook Will Print Duller Than Your Screen

*Recommendation: A. "canva lookbook" is the query and the Dec-2024 version still
pulls 456 in twenty-eight days on a channel where 76% of traffic is search, so
the phrase has to lead and "2026" is what makes someone pick the new one over
the old one sitting beside it. The parenthetical is the differentiator — every
other lookbook tutorial shows you how to place photos on a page; none of them
mention that the file will print duller than the screen. B is the flat complete
version; switch to it only if A under-performs and retention shows people
leaving before the colour section. C is the best Short title and a poor video
title: nobody searches for a problem they have not had yet.*

## Description

(see `description.txt` — published verbatim)

## Pinned comment

> The whole video in one paragraph, if you skip the rest:
>
> **Screens make colour with light. Printers make it with ink. They cannot
> reach the same colours** — and Canva puts the setting that handles it behind
> the paywall. Canva's own help page says PDF Print offers a *"color profile
> (RGB or CMYK) selection option"*, and the **same page** lists **CMYK colour
> profile options** among the features restricted to Pro, Teams, Education and
> Nonprofit. So PDF Print works on free. The CMYK choice inside it does not.
>
> Your print file therefore leaves in RGB, and the print shop's software decides
> what your brand colours become. Neon orange, electric blue and lime collapse.
> Deep teal, burgundy and charcoal barely move.
>
> Three honest options on a free account:
> · export RGB and **tell the printer in writing**, then ask for a proof
> · design in colours that survive — get a printed swatch before a run of fifty
> · pay for one month of Pro, export, cancel
>
> The second trap **is** free: tick **Crop marks and bleed** and run your
> background past the edge of the canvas. A guillotine is accurate to about a
> millimetre, and a millimetre of drift leaves a white stripe.
>
> Full kit (template + colour guide + print-shop brief):
> https://geniusjunkie.net/lookbook-kit/

## Tags

canva lookbook, how to make a lookbook in canva, lookbook template canva, canva
print settings, cmyk canva, rgb vs cmyk, canva bleed crop marks, pdf print
canva, fashion lookbook design, product catalogue canva, canva tutorial 2026,
print ready pdf canva, lookbook layout, canva pro cmyk, design for print,
catalogue template

## Thumbnail

`GJThumb20` — the channel house skeleton (see `feedback-thumbnail-geniusjunkie`):
the printed lookbook photo at full brightness under the left-to-right scrim,
"PRINTS DULLER" in yellow with a black stroke, "LOOKBOOK · CANVA" in white
beneath, three green ticks (the colour setting behind Pro / the free checkbox
that saves it / what to send the print shop), the yellow TUTORIAL tag and the
GENIUS JUNKIE badge. The proof sits in the white pink-bordered card: four
colours on screen against what ink actually reaches, captioned **CMYK IS
PRO-ONLY**. The claim is shown, not stated.

## Ad breaks (MANUAL — set these in Studio)

Automatic mid-rolls OFF. Two manual breaks, both on a designed 1.4 s silence
with a hard cut (verified silent by `gj master`):

- **3:17.4** — after the spread is built, before the colour trap
- **6:02.3** — after both exports, before the digital-version play

Break 2 was moved later during the build: at the first pass it landed at 5:24
(64% in), which left the last third without a break. Reassigning it to after
S09 put it at 71%, in line with the other videos on the slate.

## Shorts

**promo-look-colour** (30 s) — the gamut bars, then Canva's own wording and the
Pro lock. The stronger of the two: it is a number-free claim the viewer can
check against their own printed work.

**promo-look-bleed** (30 s) — the same page twice, without bleed and with. The
white stripe only appears in the first half. The useful-craft one, and the only
part of the video that costs nothing to act on.

## Facts, and where they came from

- Both colour-profile quotes are from **canva.com/help/download-file-types**,
  linked in the description so a buyer can check them.
- The script is careful about the distinction: **PDF Print is not paywalled**,
  the CMYK selection inside it is. Canva's page does not say the former, so the
  video does not either.
- The CMYK column on the colour sheet is a printed **approximation**, not a
  profile conversion — it shows the direction of the shift, and the sheet says
  so. Do not let it be read as a colour-managed proof.
- Trim arithmetic on the bleed map is **computed** from `PAGE_W_MM`/`PAGE_H_MM`
  in `product/make_lookbook_pack.py`, so the diagram cannot drift from the
  millimetres printed beside it.

## Release

Long-form **9M9z_fbDVFQ**, private draft, public **25 Sep 2026 17:00 UTC**.

**FOUR Shorts** (the new house standard — see the gj-auto skill):

| slug | id | slot | source |
|---|---|---|---|
| colour | `N_aNtDxRGPw` | 26 Sep 12:00 | S06 trap |
| dpi | `NkIJ_CT5-JQ` | 26 Sep 19:00 | S08, 289.5–312.0 |
| bleed | `L-zPPYq-3Cs` | 27 Sep 12:00 | S03 trap |
| proof | `WUWB3HpQ6eI` | 27 Sep 19:00 | S11, 416.4–431.3 |

Two from the S06/S03 traps, two from different sections so the set does not
repeat itself in the feed. Every description opens with
`▶️ FULL TUTORIAL: https://youtu.be/9M9z_fbDVFQ`.

`PromoLookDpi` does NOT use lookKit's `ZoomCheck` — that component is built for
16:9 and its 2.4px blur on 10px bars is invisible at phone scale, which killed
the only point the Short makes. It has a local `SharpVsSoft` with bigger tiles,
a face and fine rules, and a 9px blur. Check any reused kit component at phone
scale before trusting it in a Short.

Supersedes 5RfXvZpB2tM (retitled `DELETE THIS -`, private, unscheduled — user
deletes). Fourth cut: adds `colour-swatches-print.png`, which was generated but
never placed in a scene, leaving the video on 4 cutaways instead of 5.

> Third cut. Fixes the GamutBars white card collapsing to its padding — `GamutBars`
> rendered `position: absolute` inside an auto-height parent, so it contributed no
> height and the dark row labels (neon orange, electric blue, …) landed on the dark
> backdrop instead of on white. Same bug hit the colour Short. The bleed Short was
> missing its progress bar (`VertProgress dur=` should be `durationInFrames=`).
> Mid-rolls are UNCHANGED: 3:17.4 and 6:02.3, automatic OFF.

> Replaced **2et074OMY0I** (same title/description/thumbnail, corrected picture in the first
> ~2 minutes). YouTube cannot replace a video's file, so the old draft was deleted 1 Sep.
> Mid-roll positions are unchanged: 3:17.4 and 6:02.3, automatic breaks OFF.

- **ZY49lHGCVR4** — promo-look-colour, 26 Sep 12:00 UTC
- **uD885gHVROs** — promo-look-bleed, 27 Sep 12:00 UTC

Canva template: **DAHTsfpkvPw** (3508 x 2480 px = A4 landscape at 300 dpi) —
canva.link/<lookbook.canvaTemplate>. Hero image bleeding off three edges, two stacked
blocks, the type rule, product name / description / price, and the deletable
5 mm safe-margin note. Thank-you page and shop card live.

Built **by hand in the Canva editor**, not through the MCP: the API reported a
successful clear-and-rebuild commit that never persisted (second confirmed case,
both `resize-design` outputs — see `feedback-canva-commit-verify`). Two editor
gotchas worth keeping: the **Delete key does nothing** on a selected element via
automation — use right-click → Delete; and **cmd+D does not duplicate**, but
right-click → Duplicate does.

## Funnel note

Unlike the wallpaper row this one has real buyer intent: anyone making a
lookbook has products to sell and a print budget. The kit is the strongest
£4.99 product since the pitch deck, and the print-shop brief is the sheet most
likely to be worth the money on its own.

The outro points at the wall-art row, which shares the print-and-sell audience.

## What to watch

456/28d on the Dec-2024 version with no 2026 sequel. If the colour section
holds retention, **"what you can legally sell from Canva"** and **"designing for
print in Canva"** are both their own videos — this row keeps bumping into both,
and the licence question already came up on the wallpaper row.

## Pin comment

```
Say this one precisely, because half the internet gets it backwards: **PDF Print is free. The CMYK selection inside it is not.**

From Canva's download page, PDF Print gives you "300 dpi, with bleed, crop marks, and color profile (RGB or CMYK) selection option" — but CMYK colour profile options sit on the Pro-gated list alongside transparent PNGs and SVGs.

So on a free account you get the 300 DPI export. You do not get to choose CMYK inside it.
```
