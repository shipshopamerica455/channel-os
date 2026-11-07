# How to Make Seamless Patterns in Canva

## Facts verified 2026-10-05

- **THE TRAP — Canva's canvas edge is a CROP, not a wrap.** An element that
  runs off the edge is simply cut there; nothing continues on the opposite
  side. So a pattern that looks finished in Canva shows a hard seam the moment
  it tiles, and Canva gives you no way to see that seam before you export.
- **THE METHOD — Position → Advanced, exact X and Y.** Canva Help Centre,
  "Move elements in your design": X and Y values measure the distance in
  pixels from the top-left corner of the canvas, and you set them under
  **Position → Advanced**. That is the only way to place the opposite-edge
  duplicate exactly; eyeballing it is what produces the seam.
- **Spoonflower's published file spec** (a real POD fabric/wallpaper
  marketplace, named as an example):
  - *"Your files should be a JPG or PNG, saved at your preferred print
    dimensions and 150 DPI, and under 40 MB."*
  - *"Spoonflower converts all files to 150 DPI when they are uploaded to the
    site."* So the physical repeat size is what you choose; the DPI is not
    yours to decide.
  - Their own worked example: a 9 × 12 inch print is **1350 × 1800 px**.
  - *"Spoonflower prints using sRGB color mode"* — not CMYK.
  - And on seams, in their words: *"Be sure any background colors in your file
    extend to the edge of the file, otherwise the design will look broken up
    into separate squares as opposed to a seamless repeating layout."*
- **Licence, as a brief callback only** (it was the centre of the t-shirt
  video): Canva's Content Licence Agreement prohibits Pro content on "on
  demand" products and permits free content for resale. A pattern sold as a
  digital paper pack or printed on fabric is squarely in that territory.

NOT CLAIMED: what Spoonflower or any marketplace pays, what a listing costs,
what royalty rate to expect, or which marketplace is best. None was checked
against a seller-terms page in this session. Other marketplaces differ and the
script says so — it teaches the arithmetic and sends you to your own
marketplace's spec page.

---

## S01 — HOOK (~130 words)

> The canvas edge in Canva is a crop, not a wrap. Anything you push past the
> edge is cut off there, and nothing appears on the other side to continue it.
>
> Which means you can build a pattern that looks completely finished on your
> screen, export it, tile it, and watch a hard grid of seams appear — straight
> lines through your design every tile width, where the motifs stop dead at the
> boundary.
>
> And Canva will not show you that seam. There is no offset preview, no tile
> preview, no wrap mode. The design looks perfect right up until it is on
> fabric.
>
> The fix is exact arithmetic, and Canva does give you the tool for it:
> Position, Advanced, and typed X and Y values. There is a free seamless repeat
> card in the description. Let me build a tile that actually repeats.

## S02 — THE FREE CARD, AND THREE PRINCIPLES (~115 words)

> The free card is linked below — the offset arithmetic, the marketplace spec,
> and the seam test on one page.
>
> Three principles.
>
> One: every element that touches an edge needs a twin on the opposite edge, at
> exactly one canvas width or height away. Not roughly. Exactly.
>
> Two: the background has to run all the way to the edge on all four sides.
> Spoonflower say this in their own guidance — if it does not, the design
> breaks up into separate squares instead of repeating.
>
> Three: you cannot judge a seam inside Canva. The only honest test is to
> export it and tile it.
>
> Arithmetic, then proof. Not eyes.

## S03 — THE TILE SIZE (~155 words)

> Start with the tile, and start square — it makes every offset the same number
> and saves you a class of mistakes.
>
> The size question is really a physical one. Spoonflower, naming them as an
> example because other marketplaces differ, say files should be saved at your
> preferred print dimensions at a hundred and fifty D P I, and under forty
> megabytes. They also say they convert everything to a hundred and fifty D P I
> on upload — so the resolution is not yours to decide. The physical size is.
>
> So the arithmetic is inches times a hundred and fifty. Their own worked
> example is a nine by twelve inch print at thirteen fifty by eighteen hundred
> pixels.
>
> For a square tile, pick how big you want one repeat to be in the real world.
> An eight inch repeat is twelve hundred pixels square. A twelve inch repeat is
> eighteen hundred.
>
> Custom size, pixels, type it in. Check your own marketplace's spec page.

## S04 — THE BACKGROUND, AND WHY IT GOES TO THE EDGE (~150 words)

> The background first, and this is the one Spoonflower actually warn about.
>
> Their words: be sure any background colours in your file extend to the edge of
> the file, otherwise the design will look broken up into separate squares as
> opposed to a seamless repeating layout.
>
> So: a rectangle, dragged so it covers the whole canvas and overhangs on every
> side. Not snapped neatly to the edges — overhanging, so there is no chance of
> a one pixel hairline of white where the tiles meet.
>
> And resist a gradient here. A gradient has a light end and a dark end, and when
> the tile repeats, the dark end sits straight against the light end of the next
> copy. That is a seam you cannot fix with offsets, because it is the background
> itself that does not match its own opposite edge.
>
> Flat colour, or a texture that is itself seamless. Nothing directional.

## S05 — THE MOTIFS, AND THE LICENCE (~150 words)

> Now the motifs, and the usual licence check, because a pattern is about as
> sellable as a file gets.
>
> Canva's Content Licence Agreement prohibits Pro content on on demand products
> and permits free content for resale. A pattern sold as a digital paper pack,
> or printed on fabric, is exactly that territory. So Elements, the filter icon,
> price set to Free, every single search.
>
> For the pattern itself: start by scattering motifs across the middle of the
> tile, nowhere near the edges. Vary the size, vary the rotation, and leave more
> space than feels right — patterns always look busier when they tile than they
> do as a single square.
>
> Group nothing yet. Every motif has to stay individually selectable, because in
> a moment we are going to read exact coordinates off some of them and type
> those numbers back in.

<!-- AD BREAK 1 -->

## S06 — THE TRAP: THE EDGE IS A CROP (~185 words)

> Now the part that makes it seamless, and it is pure arithmetic.
>
> Take a motif and move it so it hangs off the right edge. On screen it is
> simply cut in half. That cut half has to reappear on the left edge, or the
> tile will never meet itself.
>
> So: select it, Position, Advanced, and read the X value. Say the tile is twelve
> hundred pixels wide and this motif sits at X of eleven hundred and forty.
> Duplicate it, and set the duplicate's X to eleven hundred and forty minus
> twelve hundred — which is minus sixty. Negative. It sits mostly off the canvas
> to the left, with exactly the missing piece showing.
>
> Leave Y alone. Both copies must share it exactly.
>
> Same rule vertically: Y minus the canvas height for anything crossing the top
> or bottom.
>
> And a motif in a corner needs four copies — the original, one at X minus
> width, one at Y minus height, and one with both. Miss the fourth and you get a
> seam at every corner point, which is the most noticeable kind.
>
> Typed numbers. Never dragged.

## S07 — THE SEAM TEST (~145 words)

> You cannot check this in Canva. There is no tile preview, and your eye is not
> going to catch a two pixel misalignment on a square you have been staring at
> for an hour.
>
> So export and tile it.
>
> Download as P N G. Then make a second Canva design at exactly twice the tile
> size — if your tile is twelve hundred square, make it twenty four hundred
> square — and drop the P N G in four times, at X and Y of zero and zero, zero
> and twelve hundred, twelve hundred and zero, and twelve hundred and twelve
> hundred. Typed, again.
>
> Now look at the two lines where they meet. Any motif that crosses a join
> should continue perfectly. Any stripe of background colour, any sliced leaf,
> any shift in tone — that is a seam, and it will print.
>
> Fix it in the original, export again, re-test.

## S08 — SCALE, AND THE THING THAT SURPRISES EVERYONE (~145 words)

> Scale is where most first patterns go wrong, and it has nothing to do with
> seams.
>
> A tile that looks balanced on your screen is being viewed at maybe fifteen
> centimetres across. Printed at an eight inch repeat on a metre of fabric, you
> will see it twelve or more times, and every bit of busyness multiplies.
>
> So the rule: make it sparser than feels right, and make the motifs bigger than
> feels right. Density that looks slightly empty as a single tile usually looks
> correct as cloth.
>
> And offer the same tile at more than one repeat size if your marketplace lets
> you. The identical artwork at a two inch repeat and at a twelve inch repeat
> reads as two completely different products — one is a quilting cotton, the
> other is a wallpaper.
>
> One file. Two listings.

## S09 — THE EXPORT (~150 words)

> The export, and there are three settings that matter.
>
> One: P N G or J P G. Spoonflower accept both. P N G is the safer habit — no
> compression artefacts, and artefacts tend to show up exactly at the edges
> where you least want them.
>
> Two: colour mode. Spoonflower print in s R G B, not C M Y K, and Canva works
> in R G B anyway — so for once Canva's limitation is the right answer and you
> have nothing to change.
>
> Three: the file size ceiling. Under forty megabytes. A twelve hundred pixel
> square tile is nowhere near that, but a large repeat with a photographic
> texture in it can get close.
>
> Tick the size up to two times only if your pixel dimensions come out below
> what your repeat size needs. More pixels than a hundred and fifty D P I
> achieves nothing here — they throw them away.

<!-- AD BREAK 2 -->

## S10 — COLOURWAYS: ONE TILE, FIVE PRODUCTS (~140 words)

> Here is the thing that turns a pattern into a pattern business, and it costs
> you about four minutes.
>
> Once a tile is genuinely seamless, the seams do not care what colour anything
> is. So duplicate the page, select the background, change it. Select the motifs,
> recolour them. The geometry is untouched, which means the tile is still
> seamless — you have not moved anything.
>
> Five colourways from one correct tile. A neutral, a dark, a bright, a pastel,
> and one seasonal.
>
> This is also why the arithmetic is worth doing properly the first time. Get
> one tile right and every variation inherits it. Get it slightly wrong and you
> have just made five broken products instead of one.
>
> Do the maths once. Recolour forever.

## S11 — WHERE THE SAME FILE GOES (~145 words)

> And the reason patterns are worth the fuss: one seamless tile is not one
> product.
>
> It is fabric by the metre, and wallpaper, and wrapping paper. It is a digital
> paper pack for scrapbookers, which needs nothing but the tile itself at a
> workable size. It is a background for packaging, for product photography, for
> a shop banner. It goes on a mug, a tote, a notebook cover.
>
> The reason it travels that far is precisely the seamlessness — a file that
> meets itself can be scaled to any physical object without anyone having to
> think about where it ends.
>
> Which is also the argument for testing it properly. A pattern with a seam
> fails everywhere at once, and usually not until someone has printed three
> metres of it.

## S12 — KEEPING THE FILE (~130 words)

> One habit, and it is the same one as always.
>
> Keep the Canva design, the exported tile, and a plain text note of where every
> motif came from and whether it was free.
>
> Patterns get resold, relicensed and bundled more than almost anything else you
> will make. A digital paper pack from two years ago is still out there with your
> name on it, and the one question anybody will ever ask is whether you had the
> right to sell the artwork in it.
>
> Write down the tile dimensions too. Six months from now, when you want a sixth
> colourway, the thing you will not remember is whether the canvas was twelve
> hundred or eighteen hundred.
>
> Three lines per pattern.

## S13 — THE CHECKS (~110 words)

> Before you list it.
>
> The background covers the whole canvas and overhangs every side. Every
> edge-crossing motif has an exact twin at X minus width or Y minus height, typed
> not dragged. Every corner motif has all four copies. You have tiled it two by
> two and looked at both joins. The pixel dimensions match the physical repeat
> you want at your marketplace's D P I. It is under their file size ceiling. And
> every motif came from a search filtered to Free.
>
> Seven things. The fourth is the only one that actually proves the first three.

## S14 — CLOSE (~60 words)

> The seamless repeat card is free and linked below, and if you want the
> arithmetic already done, the seamless pattern kit is a Canva tile set up with
> the offset structure in place, a two by two proof sheet, and the marketplace
> spec.
>
> Go and tile one before you trust it.

---

## Product

**NEW PACK — `seamless-pattern-kit`.** This is the first pack built for the
print-on-demand audience the last three videos created, and it exists because
the catalogue did not have one: t-shirt POD, sublimation and Cricut all had to
point at `sticker-illustration-kit`, and by the Cricut video the fit had worn
through (that kit has no SVG files and no pattern tiles).

What it contains:
- An editable Canva tile, square, with the offset structure already built — the
  guides, a worked edge-crossing motif with its exact-offset twin, and a corner
  motif with all four copies, so the buyer can see the arithmetic rather than
  take it on trust.
- A 2 × 2 proof sheet at exactly twice the tile size, with the four drop
  positions pre-set, so the seam test is one paste away.
- Reference PDFs: the offset arithmetic worked through, the Spoonflower spec
  with the inches × 150 table, the seam-test method, a scale/repeat-size guide,
  and the licence note.

**Free rung — NEW:** a one-page *Canva Seamless Repeat Card* — the edge-is-a-
crop rule, the Position → Advanced offset arithmetic including the four-corner
case, the 2 × 2 seam test, the Spoonflower spec quoted (150 DPI, sRGB, 40 MB,
background to the edge), and the seven pre-listing checks.
