# How to Make SVG Files in Canva for Cricut

## Facts verified 2026-10-05

- **THE TRAP — Cricut publishes a list of things an SVG may NOT contain, and
  Canva produces several of them by default.** Cricut Design Space help,
  "Image uploads: unsupported items" — an `.svg` or `.dxf` cannot contain
  **pattern fills**, **clipping paths** ("multiple shapes layered together so
  that one shape masks or clips the other shapes"), **editable text**, or
  **linked images**. The error is *"Your file includes unsupported items."*
  Every Canva frame and every photo-in-a-shape is a clipping path.
- **SVGs are restricted to 5,000 paths.** More than that and the upload
  errors. Source: Cricut Design Space help.
- **What Design Space accepts:** `.svg`, `.jpg`, `.bmp`, `.png`, `.gif`,
  `.dxf`. The raster types upload **as a single layer**; `.svg` and `.dxf` are
  *"cut-ready images that upload as designed"* and separate into layers.
  So a raster element inside your SVG cannot become a cut path — there is
  nothing there to cut.
- **Canva's SVG download is PAID.** Canva Help Centre, "Choose the right
  download file type": *"Quality, file size export limit, scale, compression,
  CMYK color profile options, and transparent PNGs and SVGs are available to
  accounts with the Canva Pro, Canva for Teams, Canva Education, and Canva for
  Nonprofits plans."*
- **GOOD NEWS, and then the catch: Canva outlines text on SVG export.** That
  satisfies Cricut's no-editable-text rule automatically. But outlined script
  text is one closed path per letter, so where letters overlap the blade cuts
  through the joins. Cricut's own fix is **Weld**: *"The Weld tool allows you
  to join shapes to create a single customised image by removing any
  overlapping cut lines"*, and *"wherever cut paths have intersected, only the
  exterior cut path will remain."* Note: *once a project has been welded and
  saved, it cannot be unwelded.*
- **Licence, as a brief callback only** (it was the centre of the t-shirt
  video): Canva's Content Licence Agreement prohibits Pro content on "on
  demand" products, and permits free content for resale.

NOT CLAIMED: the price of Canva Pro, a Cricut machine, Cricut Access or any
material; which machine is best; or that any particular Canva element is or is
not a vector — the script teaches the TEST instead, because Canva does not
label them.

---

## S01 — HOOK (~130 words)

> Cricut publishes a list of things an S V G file is not allowed to contain,
> and Canva makes several of them by default.
>
> Their words, from the Design Space help pages: an S V G cannot contain
> pattern fills, clipping paths, editable text, or linked images. And a
> clipping path is their term for multiple shapes layered so that one masks the
> others — which is exactly what every Canva frame is, and every photo you have
> dropped into a shape.
>
> So you pay for Canva Pro to unlock the S V G download, you export, you upload,
> and Design Space says your file includes unsupported items. No clue which
> part. And the other half of the time it uploads perfectly and cuts a
> rectangle, because the thing you drew was never a vector.
>
> There is a free Cricut export card in the description. Let me build one that
> actually cuts.

## S02 — THE FREE CARD, AND THREE PRINCIPLES (~115 words)

> The free card is linked below — Cricut's unsupported list, the path limit,
> and the export settings on one page.
>
> Three principles.
>
> One: a cut file is made of outlines, not pictures. If the thing on your
> canvas is a photograph of a shape rather than the shape itself, there is
> nothing for the blade to follow.
>
> Two: Canva does not tell you which elements are vectors. It does not label
> them and there is no filter for it. You have to test.
>
> Three: everything clever is a liability. Frames, shadows, gradients, photo
> masks — every one of those is on Cricut's list or becomes a picture.
>
> Plain shapes cut. Clever does not.

## S03 — WHAT DESIGN SPACE ACTUALLY ACCEPTS (~155 words)

> Start with what the machine will take, because it changes what you make.
>
> Design Space accepts six file types: S V G, J P G, B M P, P N G, G I F and
> D X F. But they are not equal, and the help pages are specific about why.
>
> The raster ones — J P G, P N G, B M P, G I F — upload as a single layer. One
> flat image. You can trace an outline around it, but you are not cutting the
> shapes you drew, you are cutting around a picture of them.
>
> S V G and D X F are described as cut ready images that upload as designed,
> and a file built in layers separates back into layers after uploading.
>
> That is the whole difference. An S V G keeps your shapes as shapes. Everything
> else hands Cricut a photograph and asks it to guess.
>
> So S V G, and from Canva that means Pro — the S V G download is a paid
> feature, and we will come back to that.

## S04 — THE TEST CANVA WILL NOT GIVE YOU (~155 words)

> Here is the part nobody covers, and it is the one that saves the vinyl.
>
> Canva mixes true vector elements and raster ones in the same search results,
> the same as it mixes free and Pro, and it does not label them either way.
>
> So test it yourself, in Canva, before you build anything around it. Drop the
> element on the canvas and scale it up enormously — four or five times the page.
> A vector stays perfectly crisp at any size. A raster goes soft, and then
> blocky, and you will see it immediately.
>
> Generally: the flat single-colour shapes and line icons are vectors. Anything
> photographic, anything with a soft shadow baked into it, anything that looks
> painted or textured, is not.
>
> Two seconds per element. Do it before you spend twenty minutes composing with
> something that will never cut.

## S05 — BUILDING ONE THAT WILL CUT (~150 words)

> Now build, and build plainly.
>
> Start with a blank custom size — the size does not matter much because vectors
> scale, but work at the size you will actually cut so you can judge the detail.
>
> Use solid shapes and solid-colour icons. One flat colour per piece.
>
> Do not use a frame. A frame is a clipping path and clipping paths are on
> Cricut's unsupported list by name.
>
> Do not drop a photo into a shape, for the same reason.
>
> No drop shadows, no gradients, no glows, no transparency effects. Those either
> become a picture or they become dozens of extra paths, and we will come to why
> that matters.
>
> Delete the background entirely rather than making it white — a white rectangle
> behind everything is one more shape your machine will dutifully cut around.

<!-- AD BREAK 1 -->

## S06 — THE TRAP: WATCH IT FAIL, THEN FIX IT (~185 words)

> Let me show you the failure, because the error message tells you nothing.
>
> Here is a design. A circle with a photo dropped inside it, some lettering, a
> couple of stars. In Canva it looks great.
>
> Export it as an S V G. Upload it to Design Space. And there it is: your file
> includes unsupported items. That is the entire message. It does not say which
> item, it does not highlight anything, it just refuses.
>
> The culprit is the photo in the circle. That is a clipping path — one shape
> masking another — and Cricut names clipping paths in their unsupported list.
>
> So delete it. Replace the photo with the circle on its own, as a flat colour.
> Export again. Upload again. It goes straight in, and it comes in as layers —
> circle, lettering, stars, each one separately selectable.
>
> Same design, same machine, same thirty seconds of work. The only difference is
> that nothing in the file is pretending to be something else.
>
> When Design Space refuses a Canva file, look for a frame or a photo first. It
> is almost always that.

## S07 — THE EXPORT (~150 words)

> The export itself, and there is one thing to know before you click.
>
> Share, Download, and then the file type menu. S V G.
>
> If you are on a free plan it is there but it is locked, and this is one of the
> genuine reasons to pay. Canva's own help page lists it: transparent P N Gs and
> S V Gs are available to accounts with Canva Pro, Canva for Teams, Canva
> Education and Canva for Nonprofits.
>
> There is no workaround that keeps it a real vector. Exporting a P N G and
> tracing it in Design Space is not the same thing — that is the single flat
> layer problem again, and the traced edge is an approximation of your shape
> rather than your shape.
>
> One more thing at the export: if your design has several pages, Canva gives
> you a separate S V G per page. Upload them separately. Design Space has no
> concept of your Canva pages.

## S08 — THE FIVE THOUSAND PATH CEILING (~145 words)

> A limit that catches detailed work, and almost nobody mentions it.
>
> Cricut's help pages state that S V Gs are restricted to five thousand paths,
> and more than five thousand causes an upload error.
>
> A path is roughly one outline. A simple icon might be three. A word in a
> script font is one per letter. A detailed mandala, a leafy wreath, a
> distressed texture, a halftone pattern — those run to thousands very quickly,
> and a texture overlay on its own can blow the whole budget.
>
> You cannot see the count in Canva. What you can do is notice when a design is
> getting busy, and ask whether the detail is going to survive being cut anyway.
>
> It usually is not. A shape that is two millimetres across does not cut, it
> tears. The path limit and the physical limit tend to arrive together.

## S09 — TEXT, AND THE WELD YOU WILL FORGET (~160 words)

> Text, and here Canva does you a favour you did not ask for.
>
> Cricut's unsupported list includes editable text — an S V G is not allowed to
> contain live type, it has to be shapes. And Canva converts text to outlines
> automatically when it exports an S V G. So that one is handled.
>
> But outlining turns every letter into its own separate closed shape. And if
> you used a script font where the letters touch, every one of those overlaps is
> now a cut line running straight through the join.
>
> You will get your word in pieces with slices through it.
>
> The fix is Cricut's own tool, not Canva's. Select the letters in Design Space
> and Weld. In their words, the Weld tool joins shapes by removing any
> overlapping cut lines — wherever cut paths have intersected, only the exterior
> cut path remains.
>
> And note this before you do it: once a project has been welded and saved, it
> cannot be unwelded. Duplicate first.

<!-- AD BREAK 2 -->

## S10 — THE OTHER WAY: PRINT THEN CUT (~140 words)

> There is a second way to use Canva with a Cricut, and for a lot of people it
> is the better one.
>
> Print Then Cut does not need a vector at all. You print your design on your own
> printer, the machine reads registration marks, and it cuts around the printed
> artwork. Stickers, labels, planner pieces, gift tags.
>
> And for that job every single thing we have just ruled out comes back. Photos,
> gradients, shadows, textures — all fine, because they are being printed, not
> cut. You export a P N G, not an S V G, and the Pro requirement goes away.
>
> So the question before you design anything is which of the two you are doing.
> A cut file is outlines and flat colour. A Print Then Cut file is a picture with
> a cut line around it. They are different crafts and they look different on the
> canvas.

## S11 — LAYERS AND COLOURS (~145 words)

> One more thing that will confuse you the first time.
>
> When your S V G uploads cleanly, Design Space separates it into layers, and it
> does that by the colours in your file. Each distinct fill colour becomes its
> own layer, because each one is presumably getting cut from its own piece of
> material.
>
> Which means two things.
>
> If you want three pieces in three colours of vinyl, give them three different
> fills in Canva. Even if the colours are only for your own benefit and you will
> change them later.
>
> And if you used eleven slightly different shades because you were being subtle,
> you have just made eleven layers, and Design Space will cheerfully ask you to
> load eleven mats.
>
> Pick your colours deliberately. In a cut file, colour is not decoration. It is
> instructions.

## S12 — KEEPING THE FILE (~130 words)

> One habit, and it is the same one as always.
>
> Keep the Canva design, the exported S V G, and a plain text note of where every
> element came from and whether it was free.
>
> Cut files get sold, and they get shared, and they travel further than almost
> anything else you will make. An S V G passed around a Facebook group six months
> from now is still your file with your name on the listing.
>
> And the Canva licence question is the same as it always is: Pro content may not
> go on things you sell. Filter your element search to free, every time, and you
> never have to think about it again.
>
> Three lines per design. Write it while you are placing the elements.

## S13 — THE CHECKS (~110 words)

> Before you export.
>
> No frames and no photos dropped into shapes — those are clipping paths. Every
> element passed the scale-up test and is actually a vector. Flat solid colours,
> one per intended piece of material. No shadows, gradients or textures. The
> background is deleted, not white. The design is not so detailed that it will
> tear even if it uploads. And every element came from a search filtered to free.
>
> Seven things. The first one is the one Design Space will actually stop you
> for, and the second is the one that wastes a sheet of vinyl without stopping
> you at all.

## S14 — CLOSE (~60 words)

> The Cricut export card is free and linked below, and if the job you actually
> want is sticker sheets, the sticker and illustration kit is a Canva sticker
> sheet already set up with cut lines and safe margins for Print Then Cut.
>
> Go and scale an element up to five hundred percent before you trust it.

---

## Product

Points at the **existing `sticker-illustration-kit`** (verified live, 200).

**HONEST FIT, and it is a narrow one — the script says so explicitly.** The kit
is an editable Canva sticker sheet with cut lines and safe margins plus four
reference PDFs. It contains **NO SVG files**, so it does not serve the
SVG-cutting job this video is mostly about. It serves the OTHER job the video
covers — **Print Then Cut sticker sheets** — and the close says exactly that:
"if the job you actually want is sticker sheets". It never says "SVGs for your
Cricut".

**NOTE FOR THE SLATE: this is the THIRD consecutive video pointing at this
pack** (t-shirt POD, sublimation, Cricut). The precedent for more than one
front door is `party-printables-kit` across wedding stationery and thank you
cards, and it is sound — but three in a row says the catalogue is short of
packs, not that this one is versatile. A real SVG/cut-file pack is the obvious
gap, and it is the one thing that would convert this audience the same week.

**Free rung — NEW:** a one-page *Canva → Cricut Export Card* — Cricut's
unsupported-items list quoted verbatim, the five-thousand-path ceiling, the six
accepted file types and which upload as a single layer, the scale-up vector
test, the SVG-is-Pro note, the weld rule and its one-way warning, the
colour-equals-layers rule, and the seven pre-export checks.
