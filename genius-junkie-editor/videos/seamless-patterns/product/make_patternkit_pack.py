#!/usr/bin/env python3
"""Seamless Pattern Kit — the reference set that ships with the Canva tile.

The first pack built for the print-on-demand audience the t-shirt, sublimation
and Cricut videos created. Those three all had to point at the sticker kit, and
by the Cricut video the fit had worn through.

Outputs (all US Letter):
  pattern-READ-ME.pdf          what is in the kit, how to use the tile, licence
  pattern-offset-maths.pdf     the edge-is-a-crop rule, worked, incl. corners
  pattern-marketplace-spec.pdf Spoonflower's published numbers + the inch table
  pattern-seam-test.pdf        the 2x2 proof method, step by step
  pattern-scale-guide.pdf      repeat size vs how it reads, and colourways

Every third-party number is quoted from Spoonflower's own support pages,
verified 2026-10-05. Nothing about payouts, fees or royalties is claimed.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

PAPER = (0.984, 0.980, 0.973)
INK   = (0.078, 0.094, 0.114)
TEAL  = (0.184, 0.490, 0.471)
AMBER = (0.851, 0.604, 0.169)
GREY  = (0.659, 0.690, 0.682)
PINK  = (0.914, 0.118, 0.549)
BODY  = (0.28, 0.30, 0.31)
W, H = letter
M = 0.7 * inch


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def page(c, title, kicker=None):
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - M
    if kicker:
        c.setFillColorRGB(*TEAL)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M, y + 4, kicker.upper())
        y -= 6
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, y - 20, title)
    c.setFillColorRGB(*TEAL)
    c.rect(M, y - 34, 62, 3, stroke=0, fill=1)
    return y - 58


def footer(c):
    c.setFillColorRGB(0.62, 0.64, 0.63)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(W / 2, M - 16, "Genius Junkie · geniusjunkie.net")


def body(c, y, text, size=11, font="Helvetica", col=BODY, lead=15):
    c.setFillColorRGB(*col)
    c.setFont(font, size)
    for ln in wrap(text, font, size, W - 2 * M):
        c.drawString(M, y, ln); y -= lead
    return y


def head(c, y, t):
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(M, y, t)
    return y - 18


def bullets(c, y, items, lead=16):
    for t in items:
        c.setFillColorRGB(*TEAL)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M, y, "•")
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 11)
        for i, ln in enumerate(wrap(t, "Helvetica", 11, W - 2 * M - 16)):
            c.drawString(M + 16, y, ln); y -= lead if i else lead
        y -= 4
    return y


def tile_diagram(c, x, y, s, label, corner=False):
    """A tile with an edge-crossing motif and its exact-offset twin."""
    c.setStrokeColorRGB(*GREY); c.setLineWidth(1)
    c.rect(x, y, s, s, stroke=1, fill=0)
    c.setFillColorRGB(0.93, 0.95, 0.94)
    c.rect(x, y, s, s, stroke=0, fill=1)
    c.setStrokeColorRGB(*GREY)
    c.rect(x, y, s, s, stroke=1, fill=0)
    r = s * 0.11
    # the original, hanging off the right edge
    c.setFillColorRGB(*AMBER)
    c.circle(x + s - r * 0.45, y + s * 0.62, r, stroke=0, fill=1)
    # the twin at X - width
    c.setFillColorRGB(*PINK)
    c.circle(x - r * 0.45, y + s * 0.62, r, stroke=0, fill=1)
    if corner:
        c.setFillColorRGB(*AMBER)
        c.circle(x + s - r * 0.45, y - r * 0.45, r, stroke=0, fill=1)
        c.setFillColorRGB(*PINK)
        c.circle(x - r * 0.45, y - r * 0.45, r, stroke=0, fill=1)
        c.circle(x - r * 0.45, y + s - r * 0.45, r, stroke=0, fill=1)
        c.circle(x + s - r * 0.45, y + s - r * 0.45, r, stroke=0, fill=1)
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(x + s / 2, y - 14, label)


def readme(c):
    y = page(c, "Seamless Pattern Kit", "read me first")
    y = body(c, y, "A pattern tile is either seamless or it is not — there is no 'nearly'. This kit "
                   "exists so the arithmetic is already done for you, and so you can SEE the "
                   "structure rather than take it on trust.")
    y -= 10
    y = head(c, y, "WHAT IS IN THE KIT")
    y = bullets(c, y, [
        "The Canva tile — square, with the offset structure already built. One edge-crossing motif "
        "is in place with its exact-offset twin, and one corner motif has all four copies.",
        "The 2 x 2 proof sheet — a second Canva design at exactly twice the tile size, with the "
        "four drop positions pre-set. Paste your exported tile in four times and the seam test is done.",
        "This reference set: the offset arithmetic, the marketplace spec, the seam-test method, and "
        "the scale and colourway guide.",
    ])
    y -= 6
    y = head(c, y, "HOW TO USE IT")
    y = bullets(c, y, [
        "Duplicate the tile page before you change anything, so you always have the worked example.",
        "Replace the motifs with your own, keeping the structure: anything touching an edge needs its twin.",
        "Export, drop it into the proof sheet four times, and look at the two joins.",
        "Only then recolour. Colourways inherit the geometry, so a correct tile makes five correct products.",
    ])
    y -= 6
    y = head(c, y, "THE LICENCE PART")
    y = body(c, y, "Canva's Content Licence Agreement prohibits Pro content on 'on demand' products and "
                   "permits free content for resale. A pattern sold as a digital paper pack or printed "
                   "on fabric is squarely in that territory, so filter every element search to Free. The "
                   "artwork in this kit is original and carries no Canva licence problem.")
    footer(c); c.showPage()


def offset_maths(c):
    y = page(c, "The offset arithmetic", "the one that makes it seamless")
    y = body(c, y, "Canva's canvas edge is a CROP, not a wrap. An element pushed past the edge is cut "
                   "there and nothing appears on the opposite side. So every element that touches an "
                   "edge needs a twin, placed by typed coordinates — never dragged.")
    y -= 8
    y = head(c, y, "WHERE THE NUMBERS LIVE")
    y = body(c, y, "Select the element, then Position > Advanced. X and Y are the distance in pixels "
                   "from the TOP-LEFT corner of the canvas. (Canva Help Centre, 'Move elements in your "
                   "design'.)")
    y -= 10
    y = head(c, y, "THE RULE")
    c.setFillColorRGB(*INK); c.setFont("Courier-Bold", 13)
    for ln in ["crosses the RIGHT edge  ->  twin at  X - canvas width",
               "crosses the LEFT edge   ->  twin at  X + canvas width",
               "crosses the BOTTOM      ->  twin at  Y - canvas height",
               "crosses the TOP         ->  twin at  Y + canvas height"]:
        c.drawString(M + 10, y, ln); y -= 18
    y -= 6
    y = body(c, y, "The other coordinate must stay IDENTICAL. If you change both, the twin is in the "
                   "wrong place and the seam moves rather than disappearing.", col=PINK,
             font="Helvetica-Bold")
    y -= 14
    y = head(c, y, "WORKED EXAMPLE — 1200 px SQUARE TILE")
    c.setFillColorRGB(*INK); c.setFont("Courier", 11.5)
    for ln in ["motif sits at  X = 1140,  Y = 320",
               "duplicate it,  set X = 1140 - 1200  =  -60",
               "leave         Y = 320   exactly as it was"]:
        c.drawString(M + 10, y, ln); y -= 16
    y -= 10
    y = head(c, y, "AND THE CORNER CASE — FOUR COPIES, NOT TWO")
    y = body(c, y, "A motif overlapping a corner appears in all four corners of the repeat. It needs the "
                   "original, one at X - width, one at Y - height, and one with BOTH offsets applied. "
                   "Miss the fourth and you get a seam at every corner point, which is the most "
                   "noticeable kind there is.")
    y -= 20
    tile_diagram(c, M + 20, y - 150, 150, "edge motif + twin")
    tile_diagram(c, M + 250, y - 150, 150, "corner motif + three", corner=True)
    footer(c); c.showPage()


def marketplace_spec(c):
    y = page(c, "The marketplace spec", "spoonflower's published numbers")
    y = body(c, y, "Named as an EXAMPLE. Other marketplaces differ — check your own spec page. These "
                   "are Spoonflower's own words, verified 5 October 2026.")
    y -= 10
    y = bullets(c, y, [
        "\"Your files should be a JPG or PNG, saved at your preferred print dimensions and 150 DPI, "
        "and under 40 MB.\"",
        "\"Spoonflower converts all files to 150 DPI when they are uploaded to the site.\" So the "
        "physical repeat size is your decision; the resolution is not.",
        "\"Spoonflower prints using sRGB color mode\" — not CMYK. Canva works in RGB anyway, so there "
        "is nothing to change.",
        "\"Be sure any background colors in your file extend to the edge of the file, otherwise the "
        "design will look broken up into separate squares as opposed to a seamless repeating layout.\"",
    ])
    y -= 8
    y = head(c, y, "INCHES x 150 = PIXELS")
    rows = [("2 in repeat", "300 x 300 px"), ("4 in", "600 x 600"), ("6 in", "900 x 900"),
            ("8 in", "1200 x 1200"), ("12 in", "1800 x 1800"), ("18 in", "2700 x 2700")]
    for a, b in rows:
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 11.5)
        c.drawString(M + 14, y, a)
        c.setFillColorRGB(*TEAL); c.setFont("Courier-Bold", 12)
        c.drawString(M + 170, y, b)
        y -= 17
    y -= 8
    y = body(c, y, "Spoonflower's own worked example for a non-square print: 9 x 12 inches is "
                   "1350 x 1800 px.", font="Helvetica-Oblique")
    y -= 16
    y = head(c, y, "NOT CLAIMED HERE")
    y = body(c, y, "Nothing about payouts, royalty rates, listing costs or which marketplace is best. "
                   "None of that was checked against a seller-terms page, so none of it is stated.")
    footer(c); c.showPage()


def seam_test(c):
    y = page(c, "The seam test", "the only honest check")
    y = body(c, y, "You cannot judge a seam inside Canva. There is no tile preview, no offset preview "
                   "and no wrap mode — and your eye will not catch a two-pixel misalignment on a square "
                   "you have been staring at for an hour.")
    y -= 10
    y = head(c, y, "THE 2 x 2 PROOF")
    y = bullets(c, y, [
        "Export the tile as a PNG.",
        "Open the proof sheet in this kit — it is already exactly twice the tile size.",
        "Drop the PNG in four times and set the positions by typing, not dragging:",
    ])
    c.setFillColorRGB(*INK); c.setFont("Courier-Bold", 12)
    for ln in ["X = 0     Y = 0", "X = 0     Y = tile", "X = tile  Y = 0", "X = tile  Y = tile"]:
        c.drawString(M + 26, y, ln); y -= 16
    y -= 8
    y = bullets(c, y, [
        "Look at the two lines where the copies meet — the vertical join and the horizontal one.",
        "Any motif crossing a join should continue perfectly. A stripe of background colour, a sliced "
        "leaf, or a shift in tone is a seam, and it will print.",
        "Fix it in the ORIGINAL tile, export again, re-test. Never patch the proof sheet.",
    ])
    y -= 6
    y = head(c, y, "THE THREE SEAMS, AND WHAT CAUSES EACH")
    for a, b in [("A hairline of white at a join",
                  "the background does not overhang the canvas edge"),
                 ("A motif sliced in half",
                  "it crosses an edge and has no twin, or the twin's other coordinate was changed"),
                 ("A gradual light-to-dark band",
                  "a gradient background — its dark end meets the next tile's light end")]:
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 11)
        c.drawString(M + 10, y, a); y -= 14
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
        c.drawString(M + 22, y, b); y -= 18
    footer(c); c.showPage()


def scale_guide(c):
    y = page(c, "Scale and colourways", "where first patterns go wrong")
    y = body(c, y, "Most first patterns are seamless AND wrong, because scale has nothing to do with "
                   "seams. A tile viewed at 15 cm on a screen is seen a dozen times over on a metre of "
                   "cloth, and every bit of busyness multiplies.")
    y -= 10
    y = head(c, y, "THE RULE")
    y = body(c, y, "Sparser than feels right. Motifs bigger than feels right. Density that looks "
                   "slightly empty as a single tile usually reads correctly as fabric.",
             font="Helvetica-Bold", col=INK)
    y -= 14
    y = head(c, y, "REPEAT SIZE CHANGES THE PRODUCT")
    for a, b in [("2–4 in repeat", "reads as a small print — quilting cotton, linings, gift wrap"),
                 ("6–8 in", "the general-purpose middle — apparel, cushions, tea towels"),
                 ("12–18 in", "a feature print — wallpaper, curtains, large panels")]:
        c.setFillColorRGB(*TEAL); c.setFont("Helvetica-Bold", 11.5)
        c.drawString(M + 10, y, a)
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 11)
        c.drawString(M + 130, y, b); y -= 18
    y -= 8
    y = body(c, y, "The identical artwork at two repeat sizes reads as two different products. One file, "
                   "two listings — if your marketplace allows it.", font="Helvetica-Oblique")
    y -= 16
    y = head(c, y, "COLOURWAYS INHERIT THE GEOMETRY")
    y = body(c, y, "Once a tile is genuinely seamless, the seams do not care what colour anything is. "
                   "Duplicate the page, change the background, recolour the motifs — you have not MOVED "
                   "anything, so it is still seamless.")
    y -= 8
    y = bullets(c, y, [
        "A neutral, a dark, a bright, a pastel, and one seasonal is a sensible five.",
        "This is the argument for doing the arithmetic properly once: a correct tile makes five correct "
        "products, and a slightly wrong one makes five broken ones.",
    ])
    footer(c); c.showPage()


def build():
    specs = [("pattern-READ-ME.pdf", readme),
             ("pattern-offset-maths.pdf", offset_maths),
             ("pattern-marketplace-spec.pdf", marketplace_spec),
             ("pattern-seam-test.pdf", seam_test),
             ("pattern-scale-guide.pdf", scale_guide)]
    for name, fn in specs:
        path = os.path.join(OUT, name)
        c = pdfcanvas.Canvas(path, pagesize=letter)
        c.setTitle(name.replace("-", " ").replace(".pdf", "") + " — Genius Junkie")
        fn(c)
        c.save()
        print("wrote", name)


if __name__ == "__main__":
    build()
