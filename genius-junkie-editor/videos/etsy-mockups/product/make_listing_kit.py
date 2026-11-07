#!/usr/bin/env python3
"""Etsy Listing Image Kit — the printable reference set that ships with the
editable Canva template.

Outputs (A4 unless noted):
  listing-safe-band-guide.pdf   the 2000x2000 canvas with the 5:4 band drawn to scale
  listing-10-slot-plan.pdf      what each of the ten slots is for, in order
  listing-info-cards.pdf        fill-in copy for photos 4-7
  listing-checklist.pdf         the six checks, printable and tickable
  listing-specs.pdf             Etsy image + video specs on one page
  listing-READ-ME.pdf           how to use the Canva template, and the licence
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

PAPER = (0.980, 0.969, 0.949)   # #faf7f2
INK = (0.169, 0.149, 0.133)     # #2b2622
CLAY = (0.761, 0.408, 0.247)    # #c2683f
SAND = (0.886, 0.831, 0.753)    # #e2d4c0
SAGE = (0.553, 0.608, 0.514)    # #8d9b83
DIM = (0.486, 0.443, 0.408)     # #7c7168
BAND = (0.914, 0.118, 0.549)    # Genius Junkie pink
W, H = A4
M = 0.85 * inch


def page(c, title, kicker=None):
    """Common page furniture. Returns the y cursor under the header."""
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - M
    if kicker:
        c.setFillColorRGB(*SAGE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M, y + 6, kicker.upper())
        y -= 6
    c.setFillColorRGB(*CLAY)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, y - 18, title)
    c.setFillColorRGB(*CLAY)
    c.rect(M, y - 32, 66, 3, stroke=0, fill=1)
    return y - 62


def footer(c):
    c.setFillColorRGB(0.6, 0.57, 0.55)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(W / 2, M - 22, "Genius Junkie · geniusjunkie.net")


def bullets(c, y, lines, indent=12, size=10.5, lead=15):
    c.setFont("Helvetica", size)
    c.setFillColorRGB(0.34, 0.31, 0.29)
    for ln in lines:
        c.drawString(M + indent, y, ln)
        y -= lead
    return y


def heading(c, y, text, size=12.5):
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", size)
    c.drawString(M, y, text)
    return y - 18


# ----------------------------------------------------------- safe band ------
def safe_band_guide(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "The 5:4 safe band", "listing image kit")

    c.setFont("Helvetica", 10.5)
    c.setFillColorRGB(0.34, 0.31, 0.29)
    for ln in [
        "You upload a 2000 × 2000 square. In Etsy's search results — where the buying",
        "decision happens — that square is cropped to 5:4 (570 × 456 px): the middle 80%",
        "of the height. Everything essential has to live inside the band below.",
    ]:
        c.drawString(M, y, ln)
        y -= 15
    y -= 14

    # the square, drawn to scale
    side = W - 2 * M - 1.9 * inch
    sx, sy = M, y - side
    c.setFillColorRGB(1, 1, 1)
    c.rect(sx, sy, side, side, stroke=0, fill=1)
    c.setStrokeColorRGB(*DIM)
    c.setLineWidth(0.8)
    c.rect(sx, sy, side, side, stroke=1, fill=0)

    # the 10% strips that get thrown away
    strip = side * 0.10
    c.setFillColorRGB(*BAND)
    c.setFillAlpha(0.22)
    c.rect(sx, sy + side - strip, side, strip, stroke=0, fill=1)
    c.rect(sx, sy, side, strip, stroke=0, fill=1)
    c.setFillAlpha(1)

    # the band itself
    c.setStrokeColorRGB(*CLAY)
    c.setLineWidth(2)
    c.rect(sx, sy + strip, side, side - 2 * strip, stroke=1, fill=0)

    # a product sitting correctly inside it
    aw = side * 0.30
    c.setFillColorRGB(*CLAY)
    c.roundRect(sx + side * 0.17, sy + side * 0.30, aw, side * 0.36, aw / 2.4, stroke=0, fill=1)
    c.setFillColorRGB(*SAND)
    c.circle(sx + side * 0.66, sy + side * 0.47, side * 0.11, stroke=0, fill=1)

    c.setFillColorRGB(*BAND)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(sx + 8, sy + side - strip / 2 - 3, "CROPPED AWAY IN SEARCH · 200 px")
    c.drawString(sx + 8, sy + strip / 2 - 3, "CROPPED AWAY IN SEARCH · 200 px")
    c.setFillColorRGB(*CLAY)
    c.drawString(sx + 8, sy + side / 2 - 3, "5:4 SAFE BAND — 1600 px of the 2000")

    # the numbers, to the right
    nx = sx + side + 18
    ny = sy + side - 6
    for lab, val in [
        ("Canvas", "2000 × 2000 px"),
        ("Guide 1", "10% from the top (200 px)"),
        ("Guide 2", "10% from the bottom (200 px)"),
        ("Search crop", "570 × 456 px (5:4)"),
        ("Safe height", "1600 px"),
        ("Export", "JPEG, ~90% quality"),
    ]:
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(nx, ny, lab)
        c.setFillColorRGB(*DIM)
        c.setFont("Helvetica", 8.5)
        c.drawString(nx, ny - 11, val)
        ny -= 32

    y = sy - 26
    y = heading(c, y, "Outside the band goes decoration only")
    bullets(c, y, [
        "background, a soft shadow, a sliver of prop — nothing you would miss",
        "never the product, never text, never your logo",
        "delete the guides before you export",
    ])
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------- 10-slot plan ----
def slot_plan(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "The ten slots, in order", "listing image kit")

    c.setFont("Helvetica", 10.5)
    c.setFillColorRGB(0.34, 0.31, 0.29)
    c.drawString(M, y, "Etsy shows the first few as thumbnails and almost nobody swipes past four.")
    y -= 15
    c.drawString(M, y, "Order matters more than count — but use all ten, they cost nothing.")
    y -= 26

    rows = [
        ("1", "HERO", "the product filling the frame, plain light background, no text"),
        ("2", "MOCKUP", "the outcome — framed on a wall, used on a desk, held in a hand"),
        ("3", "SCALE", "against a hand, a mug or furniture, with the real dimensions on it"),
        ("4", "CARD — INCLUDED", "exactly what they receive, listed plainly"),
        ("5", "CARD — SIZES", "sizes or variations available"),
        ("6", "CARD — DELIVERY", "instant download, or shipped in 2–3 days"),
        ("7", "CARD — HOW TO USE", "printing, care or usage instructions"),
        ("8", "DETAIL", "texture, stitching, the actual pixels of a print"),
        ("9", "DETAIL", "a second close-up from a different part of the product"),
        ("10", "LIFESTYLE", "your best in-situ shot — the product being lived with"),
        ("▶", "VIDEO", "5–15 s, no sound needed — a slow pan is enough"),
    ]
    for n, lab, desc in rows:
        c.setFillColorRGB(*SAND)
        c.roundRect(M, y - 4, 26, 18, 5, stroke=0, fill=1)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(M + 13, y + 1, n)
        c.setFillColorRGB(*CLAY)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(M + 36, y + 1, lab)
        c.setFillColorRGB(0.34, 0.31, 0.29)
        c.setFont("Helvetica", 9.5)
        c.drawString(M + 165, y + 1, desc)
        y -= 26

    y -= 8
    y = heading(c, y, "The rule under all of it")
    bullets(c, y, [
        "a buyer arrives with four questions: what is it, what does it look like in real",
        "life, how big is it, and what exactly do I get.",
        "the ten slots answer those, in that order, before anyone reads a word.",
    ])
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------- info cards ------
def info_cards(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "Copy for photos 4–7", "listing image kit")

    c.setFont("Helvetica", 10.5)
    c.setFillColorRGB(0.34, 0.31, 0.29)
    c.drawString(M, y, "Fill these in once, then reuse the wording across every listing. Plain")
    y -= 15
    c.drawString(M, y, "sentences, not marketing — each card is a message you never have to answer.")
    y -= 26

    cards = [
        ("PHOTO 4 — WHAT'S INCLUDED", [
            "• ____ designs / colourways",
            "• ____ file(s) per design, ____ format",
            "• ____ DPI · ____ × ____ px",
        ]),
        ("PHOTO 5 — SIZES & VARIATIONS", [
            "• ratios: ______________________",
            "• sizes: _______________________",
            "• anything that needs its own file: ______",
        ]),
        ("PHOTO 6 — HOW IT ARRIVES", [
            "• instant download / shipped in ____ days",
            "• nothing is posted / tracked shipping included",
            "• where to find it after purchase: ______",
        ]),
        ("PHOTO 7 — HOW TO USE IT", [
            "• print at 100%, do not scale up",
            "• paper: ______________________",
            "• care / usage: ________________",
        ]),
    ]
    for title, lines in cards:
        c.setStrokeColorRGB(*SAND)
        c.setLineWidth(1.4)
        c.roundRect(M, y - 62, W - 2 * M, 74, 8, stroke=1, fill=0)
        c.setFillColorRGB(*CLAY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(M + 14, y - 4, title)
        c.setFillColorRGB(0.34, 0.31, 0.29)
        c.setFont("Helvetica", 9.5)
        ly = y - 22
        for ln in lines:
            c.drawString(M + 14, ly, ln)
            ly -= 14
        y -= 92

    y = heading(c, y, "Keep all four identical")
    bullets(c, y, [
        "same background, same font, same accent colour as your hero",
        "so the set reads as one shop, not four different sellers",
    ])
    footer(c)
    c.showPage()
    c.save()


# ----------------------------------------------------------- checklist ------
def checklist(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "Before you publish", "listing image kit")

    checks = [
        ("Hero built inside the 5:4 safe band", "nothing essential in the top or bottom 10%"),
        ("At least five photos — ideally all ten", "under five measurably underperforms"),
        ("A mockup that matches what they receive", "one file → one framed print, not a gallery wall"),
        ("A scale shot with real dimensions", "a hand, a mug, or above furniture"),
        ("Information cards sharing one style", "same background, font and accent"),
        ("Exported JPEG, 2000 px min on the short side", "~90% quality — sharp but light on mobile"),
    ]
    y -= 6
    for i, (t, sub) in enumerate(checks, 1):
        c.setStrokeColorRGB(*DIM)
        c.setLineWidth(1.2)
        c.rect(M, y - 10, 16, 16, stroke=1, fill=0)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(M + 28, y, f"{i}. {t}")
        c.setFillColorRGB(0.45, 0.42, 0.40)
        c.setFont("Helvetica", 9.5)
        c.drawString(M + 28, y - 15, sub)
        y -= 44

    y -= 10
    c.setFillColorRGB(*SAGE)
    c.setLineWidth(2)
    c.setStrokeColorRGB(*SAGE)
    c.roundRect(M, y - 46, W - 2 * M, 54, 10, stroke=1, fill=0)
    c.setFillColorRGB(*SAGE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M + 18, y - 14, "Six ticks and the listing is doing its job")
    c.setFillColorRGB(0.34, 0.31, 0.29)
    c.setFont("Helvetica", 10)
    c.drawString(M + 18, y - 32, "before anyone reads a word of your description.")

    y -= 78
    y = heading(c, y, "The four mistakes that cost clicks")
    bullets(c, y, [
        "fewer than five photos — you have ten slots and they are free",
        "text sprayed across the hero — it gets cropped and reads as an advert",
        "mockups that overclaim — where bad reviews come from",
        "inconsistent styling across the shop — every listing looks like a new seller",
    ])
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------------------- specs ------
def specs(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "Etsy image specs", "listing image kit")

    rows = [
        ("Minimum size", "2000 px on the shortest side"),
        ("Safe sizes", "2000 × 2000 (1:1) or 2700 × 2025 (4:3)"),
        ("Search crop", "5:4 — 570 × 456 px, taken from the middle"),
        ("Slots", "10 images + 1 video per listing"),
        ("Formats", "JPG · PNG · GIF"),
        ("Video", "5–15 seconds, no sound needed"),
        ("Export", "JPEG at ~90% quality"),
        ("Below 2000 px", "Etsy's zoom will not engage"),
    ]
    for lab, val in rows:
        c.setFillColorRGB(*CLAY)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M, y, lab)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", 11)
        c.drawString(M + 165, y, val)
        c.setStrokeColorRGB(0.88, 0.86, 0.83)
        c.setLineWidth(0.7)
        c.line(M, y - 9, W - M, y - 9)
        y -= 30

    y -= 14
    y = heading(c, y, "On file size")
    bullets(c, y, [
        "reported caps vary across sources — do not design to a number.",
        "JPEG at ~90% keeps a 2000 px image comfortably under a megabyte,",
        "which is sharp enough to look good and light enough to load fast on a",
        "phone, where most of your buyers are.",
    ])
    footer(c)
    c.showPage()
    c.save()


# -------------------------------------------------------------- read me -----
def readme(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "Read me first", "etsy listing image kit")

    blocks = [
        ("What's in this kit", [
            "The editable Canva template — ten pages, one per listing slot, with",
            "   the 5:4 safe band already marked as guides",
            "The five reference PDFs in this folder (safe band, slot plan,",
            "   card copy, checklist, specs)",
        ]),
        ("How to use the Canva template", [
            "Open the template link — it copies into your own Canva account.",
            "Page 1 is the hero. Replace the placeholder art with yours, keeping",
            "   everything inside the pink band.",
            "Pages 2–10 follow the slot plan. Swap the art and the words.",
            "Delete the guides layer, then Share → Download → JPEG.",
        ]),
        ("For the next product", [
            "Duplicate the whole design, swap the artwork and the words, and you",
            "   have ten listing images in about ten minutes.",
            "Keep the card design identical across every listing — that is what",
            "   makes a shop read as a brand rather than a collection.",
        ]),
        ("If you sell physical things", [
            "Shoot next to a window, light from the side, ceiling light OFF.",
            "A sheet of white card opposite the window bounces light back in.",
            "In Canva: crop to 2000 × 2000 inside the band, then Adjust — lift",
            "   brightness a little, drop saturation a touch.",
        ]),
        ("Licence", [
            "Use this kit for your own shop's listings, on unlimited products,",
            "   including products you sell commercially.",
            "You may not resell, share or redistribute the template or these",
            "   PDFs themselves, and you may not sell the kit as your own.",
        ]),
    ]
    for title, lines in blocks:
        y = heading(c, y, title)
        y = bullets(c, y, ["• " + ln if not ln.startswith("   ") else ln for ln in lines])
        y -= 12

    footer(c)
    c.showPage()
    c.save()


if __name__ == "__main__":
    made = [
        ("listing-safe-band-guide.pdf", safe_band_guide),
        ("listing-10-slot-plan.pdf", slot_plan),
        ("listing-info-cards.pdf", info_cards),
        ("listing-checklist.pdf", checklist),
        ("listing-specs.pdf", specs),
        ("listing-READ-ME.pdf", readme),
    ]
    for name, fn in made:
        fn(os.path.join(OUT, name))
    print(f"wrote {len(made)} PDFs")
