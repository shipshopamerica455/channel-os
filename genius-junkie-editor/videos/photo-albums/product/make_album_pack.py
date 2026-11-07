#!/usr/bin/env python3
"""Photo Album Kit — the reference sheets that ship with the editable Canva
photo album template (8 x 6 in landscape, 20 inside pages + cover).

Every binding and page-count fact is quoted from Canva's own photo books page
and the source is printed on the sheet so a buyer can check it. The gutter and
safe-zone arithmetic is COMPUTED from the page size, so the diagrams cannot
drift from the millimetres printed beside them.

Verified 2026-09-01 — canva.com/photo-books.

Outputs (all US Letter):
  01-gutter-and-safe-zone-map.pdf  the spread drawn to scale, with the fold
  02-page-planner.pdf              twenty pages as sections, fill-in
  03-photo-check.pdf               resolution, and what gloss does to shadows
  04-print-shop-brief.pdf          fill-in email that asks the layflat question
  05-binding-guide.pdf             layflat vs PUR, quoted, and what it costs you
  06-spread-recipes.pdf            six layouts that keep faces clear of the fold
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

PAPER = (0.984, 0.980, 0.973)
INK = (0.078, 0.094, 0.114)
BLUE = (0.176, 0.404, 0.663)
AMBER = (0.851, 0.604, 0.169)
GREY = (0.659, 0.690, 0.682)
PINK = (0.914, 0.118, 0.549)
GREEN = (0.133, 0.773, 0.369)
BODY = (0.28, 0.30, 0.31)
BOX = (0.898, 0.925, 0.945)
PHOTO = (0.851, 0.784, 0.706)
W, H = letter
M = 0.7 * inch

# ----------------------------------------------------------------- page ----
# The Canva photo book, in millimetres. Every diagram below derives from these,
# so the drawing and the numbers printed next to it cannot disagree.
PAGE_W_MM, PAGE_H_MM = 203.2, 152.4      # 8 x 6 in
SPREAD_W_MM = PAGE_W_MM * 2              # 406.4
BLEED_MM = 3.0
SAFE_MM = 12.7                           # 1/2 in from the outside edges
GUTTER_MM = 19.05                        # 3/4 in EITHER SIDE of the fold
MIN_PAGES, MAX_PAGES = 20, 98            # Canva's stated range

CANVA_SRC = "canva.com/photo-books, verified 1 September 2026"


def page(c, title, kicker=None):
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - M
    if kicker:
        c.setFillColorRGB(*BLUE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M, y + 4, kicker.upper())
        y -= 6
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, y - 20, title)
    c.setFillColorRGB(*BLUE)
    c.rect(M, y - 34, 62, 3, stroke=0, fill=1)
    return y - 58


def footer(c):
    c.setFillColorRGB(0.62, 0.64, 0.63)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(W / 2, M - 16, "Genius Junkie · geniusjunkie.net")


def body(c, y, lines, size=10.5, lead=15, indent=0, col=BODY):
    c.setFont("Helvetica", size)
    c.setFillColorRGB(*col)
    for ln in lines:
        c.drawString(M + indent, y, ln)
        y -= lead
    return y


def heading(c, y, text, size=12.5):
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", size)
    c.drawString(M, y, text)
    return y - 18


def wrap(text, width_pt, size, font="Helvetica"):
    out, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if stringWidth(trial, font, size) <= width_pt:
            line = trial
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def para(c, y, text, size=10.5, lead=15, col=BODY, width=None):
    return body(c, y, wrap(text, width or (W - 2 * M), size), size=size, lead=lead, col=col)


def callout(c, y, title, lines, col=PINK, width=None):
    w = width or (W - 2 * M)
    wrapped = []
    for ln in lines:
        wrapped.extend(wrap(ln, w - 28, 9.5))
    h = 34 + 13 * len(wrapped)
    c.setStrokeColorRGB(*col)
    c.setLineWidth(2)
    c.roundRect(M, y - h, w, h + 6, 9, stroke=1, fill=0)
    c.setFillColorRGB(*col)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 14, y - 16, title)
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 9.5)
    yy = y - 33
    for ln in wrapped:
        c.drawString(M + 14, yy, ln)
        yy -= 13
    return y - h - 18


def table(c, y, cols, rows, widths, head_col=BLUE):
    x = M
    c.setFillColorRGB(*head_col)
    c.setFont("Helvetica-Bold", 9)
    for col, wdt in zip(cols, widths):
        c.drawString(x, y, col.upper())
        x += wdt
    y -= 6
    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(0.7)
    c.line(M, y, M + sum(widths), y)
    y -= 14
    for row in rows:
        x = M
        for cell, wdt, i in zip(row, widths, range(len(row))):
            c.setFillColorRGB(*(INK if i == 0 else BODY))
            c.setFont("Helvetica-Bold" if i == 0 else "Helvetica", 10)
            c.drawString(x, y, str(cell))
            x += wdt
        y -= 16
    return y - 6


def rule_line(c, y, col=GREY):
    c.setStrokeColorRGB(*col)
    c.setLineWidth(0.7)
    c.line(M, y, W - M, y)
    return y - 16


# ------------------------------------------------- 1 · gutter & safe zone ---
def pdf_gutter():
    c = pdfcanvas.Canvas(os.path.join(OUT, "01-gutter-and-safe-zone-map.pdf"), pagesize=letter)
    y = page(c, "The gutter and safe-zone map", "photo album kit · sheet 1")
    y = para(c, y, "One spread, drawn to scale. Everything in this kit is a consequence of the "
                   "shaded band down the middle: that is not a line on your design, it is the "
                   "place where the paper turns into the spine.")
    y -= 10

    # the spread, drawn to scale from the millimetres above
    avail = W - 2 * M
    scale = avail / (SPREAD_W_MM * mm)
    sw = SPREAD_W_MM * mm * scale
    sh = PAGE_H_MM * mm * scale
    x0, y0 = M, y - sh
    half = x0 + sw / 2

    c.setFillColorRGB(*PHOTO)
    c.rect(x0, y0, sw, sh, stroke=0, fill=1)
    # the gutter band
    gw = GUTTER_MM * mm * scale
    c.setFillColorRGB(0.98, 0.85, 0.93)
    c.rect(half - gw, y0, gw * 2, sh, stroke=0, fill=1)
    c.setStrokeColorRGB(*PINK)
    c.setLineWidth(1.2)
    c.setDash(4, 3)
    c.line(half - gw, y0, half - gw, y0 + sh)
    c.line(half + gw, y0, half + gw, y0 + sh)
    # the safe zone
    sm = SAFE_MM * mm * scale
    c.setStrokeColorRGB(*GREEN)
    c.rect(x0 + sm, y0 + sm, sw - 2 * sm, sh - 2 * sm, stroke=1, fill=0)
    c.setDash()
    # the fold itself
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.6)
    c.line(half, y0, half, y0 + sh)
    # frame
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.0)
    c.rect(x0, y0, sw, sh, stroke=1, fill=0)

    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColorRGB(*PINK)
    c.drawCentredString(half, y0 - 14, f"KEEP OUT — {GUTTER_MM:.2f} mm (3/4 in) EITHER SIDE OF THE FOLD")
    c.setFillColorRGB(*GREEN)
    c.drawString(x0 + sm + 4, y0 + sh + 8, f"SAFE ZONE — {SAFE_MM:.1f} mm (1/2 in) FROM EVERY OUTSIDE EDGE")
    y = y0 - 34

    y = table(c, y, ["measurement", "millimetres", "inches"], [
        ("Page", f"{PAGE_W_MM:.1f} x {PAGE_H_MM:.1f}", "8 x 6"),
        ("Spread (two pages)", f"{SPREAD_W_MM:.1f} x {PAGE_H_MM:.1f}", "16 x 6"),
        ("Bleed, all round", f"{BLEED_MM:.1f}", "0.12"),
        ("Safe margin", f"{SAFE_MM:.1f}", "0.50"),
        ("Gutter keep-out, each side", f"{GUTTER_MM:.2f}", "0.75"),
        ("Total gutter keep-out", f"{GUTTER_MM * 2:.2f}", "1.50"),
    ], [2.6 * inch, 1.9 * inch, 1.4 * inch])

    y = callout(c, y, "What may and may not cross the fold", [
        "NO — a face. It is bent, and it catches a shadow along the fold.",
        "NO — text. A word broken by a fold is a word nobody reads.",
        "NO — a horizon line. A bent horizon looks broken; a bent sky does not.",
        "YES — sky, water, blurred backgrounds, texture. Nobody can tell where a cloud was meant to be.",
    ])
    footer(c)
    c.save()


# ------------------------------------------------------- 2 · page planner ---
def pdf_planner():
    c = pdfcanvas.Canvas(os.path.join(OUT, "02-page-planner.pdf"), pagesize=letter)
    y = page(c, "The twenty-page planner", "photo album kit · sheet 2")
    y = para(c, y, f"Canva's photo books take from {MIN_PAGES} to {MAX_PAGES} inside pages. "
                   f"{MIN_PAGES} is a floor, not a suggestion — so fill this in BEFORE you place "
                   "a single photo. Six sections across twenty pages is about three pages each, "
                   "and then every page has a job.")
    y -= 6
    y = callout(c, y, "Do this on paper first", [
        "Write the sections, not the photos. Arrival. The first evening. The long walk.",
        "The bad weather day. The people. The last morning.",
        "Then you are choosing which story earns an extra spread, instead of hunting for",
        "eight more photos to pad out the end. Same page count, completely different book.",
    ], col=BLUE)

    y = heading(c, y, "Your twenty pages")
    rows = 6
    colw = (W - 2 * M)
    for i in range(rows):
        yy = y - i * 46
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.7)
        c.roundRect(M, yy - 34, colw, 38, 5, stroke=1, fill=0)
        c.setFillColorRGB(*BLUE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(M + 10, yy - 12, f"SECTION {i + 1}")
        c.setFillColorRGB(*GREY)
        c.setFont("Helvetica", 8.5)
        c.drawString(M + 10, yy - 27, "name")
        c.drawString(M + 3.1 * inch, yy - 27, "pages")
        c.drawString(M + 4.5 * inch, yy - 27, "the one photo it is built around")
        c.setStrokeColorRGB(0.85, 0.86, 0.85)
        c.line(M + 44, yy - 24, M + 3.0 * inch, yy - 24)
        c.line(M + 3.45 * inch, yy - 24, M + 4.4 * inch, yy - 24)
        c.line(M + 6.1 * inch, yy - 24, W - M - 10, yy - 24)
    y = y - rows * 46 - 10

    y = rule_line(c, y)
    y = body(c, y, [
        "Total must reach 20.   Pages used: ______        Still to place: ______",
    ], size=11)
    y -= 6
    y = para(c, y, "Remember the cover is separate — it is not one of the twenty. And the inside "
                   "face of the front cover prints blank on hardcover, so your dedication goes on "
                   "inside page one.", size=9.5, lead=13)
    footer(c)
    c.save()


# -------------------------------------------------------- 3 · photo check ---
def pdf_photos():
    c = pdfcanvas.Canvas(os.path.join(OUT, "03-photo-check.pdf"), pagesize=letter)
    y = page(c, "Checking the photos", "photo album kit · sheet 3")
    y = para(c, y, "Two things go wrong between your screen and 148 gsm gloss paper: resolution, "
                   "and shadows. Both are cheap to check and impossible to fix after printing.")
    y -= 8

    y = heading(c, y, "1 · Resolution")
    y = para(c, y, "A phone photo is fine at the size it appears on the page. The trouble starts "
                   "when a small photo is blown up to fill a whole page. Print wants 300 dots per "
                   "inch — a picture that looks acceptable on a laptop can land soft on gloss.")
    y = table(c, y, ["if the photo fills", "you need at least", "a 12 MP phone photo"], [
        ("A quarter page (4 x 3 in)", "1200 x 900 px", "fine"),
        ("Half a page (8 x 3 in)", "2400 x 900 px", "fine"),
        ("A full page (8 x 6 in)", "2400 x 1800 px", "usually fine"),
        ("A full spread (16 x 6 in)", "4800 x 1800 px", "check it"),
    ], [2.9 * inch, 2.1 * inch, 1.9 * inch])
    y = callout(c, y, "Believe the warning", [
        "Canva flags low-resolution images with a small warning on the image. It is right.",
        "If you see it on a full-page photo, use a different photo or make it smaller.",
    ], col=AMBER)

    y = heading(c, y, "2 · Gloss deepens contrast")
    y = para(c, y, "Canva's inside pages are printed on 148 gsm gloss stock. Gloss deepens "
                   "contrast, so photos that are already dark print darker and the detail in the "
                   "shadows disappears. If a picture is moody on screen, lift the shadows "
                   "slightly before you place it.")
    y = body(c, y, [
        "[  ] Every full-page photo checked for the low-resolution flag",
        "[  ] Every dark photo has had its shadows lifted",
        "[  ] No photo has been enlarged past its original size",
        "[  ] Faces are clear of the gutter keep-out on every spread",
    ], size=11, lead=18)
    footer(c)
    c.save()


# ---------------------------------------------------- 4 · print-shop brief ---
def pdf_brief():
    c = pdfcanvas.Canvas(os.path.join(OUT, "04-print-shop-brief.pdf"), pagesize=letter)
    y = page(c, "The print-shop brief", "photo album kit · sheet 4")
    y = para(c, y, "If you are printing anywhere other than Canva, send this before you send the "
                   "file. The first question is the one that changes your layout, so ask it "
                   "while you can still act on the answer.")
    y -= 6
    y = callout(c, y, "The question that changes everything", [
        "\"Is this binding layflat, or perfect bound / PUR?\"",
        "LAYFLAT — the pages open to a genuinely flat plane. You can relax the gutter",
        "keep-out and design proper full-spread images.",
        "PERFECT BOUND or PUR — the centre of every spread curves into the spine. Keep",
        "faces, text and horizons out of the gutter band on sheet 1.",
    ])

    y = heading(c, y, "Copy this into an email")
    box_h = 268
    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(0.9)
    c.roundRect(M, y - box_h, W - 2 * M, box_h, 8, stroke=1, fill=0)
    tx = M + 14
    yy = y - 22
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10)
    lines = [
        "Hello,",
        "",
        "I would like a quote for a photo book:",
        "",
        f"   Finished size        {PAGE_W_MM:.0f} x {PAGE_H_MM:.0f} mm (8 x 6 in), landscape",
        "   Inside pages         ______   (must be an even number)",
        "   Cover                softcover / hardcover",
        "   Quantity             ______",
        f"   Bleed supplied       {BLEED_MM:.0f} mm all round, with crop marks",
        "   File                 print-ready PDF, RGB unless you tell me otherwise",
        "",
        "Three questions before I send artwork:",
        "",
        "   1. Is the binding layflat, or perfect bound / PUR?",
        "   2. What gutter allowance do you want for this page count?",
        "   3. Can I have a proof before the full run?",
        "",
        "Thank you,",
        "______________________",
    ]
    for ln in lines:
        c.drawString(tx, yy, ln)
        yy -= 13.5
    y = y - box_h - 20
    y = para(c, y, "Question two matters more than people expect: the thicker the book, the more "
                   "the inner pages are pulled into the spine, so a printer may ask for a wider "
                   "gutter on a 90-page book than on a 20-page one.", size=9.5, lead=13)
    footer(c)
    c.save()


# ------------------------------------------------------ 5 · binding guide ---
def pdf_binding():
    c = pdfcanvas.Canvas(os.path.join(OUT, "05-binding-guide.pdf"), pagesize=letter)
    y = page(c, "Layflat, PUR, and what Canva offers", "photo album kit · sheet 5")
    y = para(c, y, "This is the fact the whole kit is built around, in Canva's own words so you "
                   "can check it yourself.")
    y -= 6

    y = callout(c, y, "From Canva's photo books page", [
        "\"No, we don't offer layflat binding at this time. We do, however, offer PUR",
        "binding using a strong bookbinding adhesive.\"",
        "",
        "\"Design for a front cover, back cover and from 20 to 98 inside pages.\"",
        "",
        "\"Inside faces of the covers and endpapers (hardcover only) will be left blank.\"",
        "",
        "\"Inside pages are printed with quality 148gsm paper in a gloss finish.\"",
        "",
        f"Source: {CANVA_SRC}",
    ], col=BLUE)

    y = heading(c, y, "What the difference actually means")
    y = table(c, y, ["", "layflat", "PUR / perfect bound"], [
        ("Opens to", "a flat plane", "a curve into the spine"),
        ("Full-spread photo", "survives", "loses the centre"),
        ("Face on the fold", "fine", "bent and shadowed"),
        ("Typical cost", "higher", "lower"),
        ("Canva offers it", "no", "yes"),
    ], [2.3 * inch, 2.2 * inch, 2.4 * inch])

    y = para(c, y, "PUR is not a bad binding. It uses a polyurethane adhesive that is stronger "
                   "and more flexible than ordinary perfect binding, it opens flatter, and the "
                   "book will not fall apart. It is simply not layflat — and if you design as "
                   "though it were, the fold takes the best part of your best photo.")
    y -= 4
    y = callout(c, y, "The two-minute test", [
        "Print any spread at home on ordinary paper. Fold it down the centre. Hold it like a book.",
        "That is what the binding will do to it. If the fold lands on somebody's eye, you have",
        "just saved three weeks and the price of a hardback.",
        "Do it on the first spread and you will rarely need it again — by then you can see the",
        "fold before it exists.",
    ], col=GREEN)
    footer(c)
    c.save()


# ----------------------------------------------------- 6 · spread recipes ---
# l/t/w/h are fractions of the SPREAD. Nothing important crosses 0.5.
RECIPES = [
    ("Hero left, quiet right", "the standard opener — subject, then room to breathe", [
        (0.03, 0.06, 0.42, 0.88, "photo"), (0.56, 0.20, 0.30, 0.44, "photo"),
        (0.56, 0.70, 0.34, 0.12, "type"),
    ]),
    ("Sky across the fold", "the ONE thing that may cross the middle", [
        (0.02, 0.05, 0.96, 0.66, "sky"), (0.06, 0.78, 0.30, 0.10, "type"),
    ]),
    ("Four and one", "a day, then the photo that sums it up", [
        (0.03, 0.06, 0.20, 0.40, "photo"), (0.25, 0.06, 0.20, 0.40, "photo"),
        (0.03, 0.52, 0.20, 0.40, "photo"), (0.25, 0.52, 0.20, 0.40, "photo"),
        (0.55, 0.06, 0.42, 0.86, "photo"),
    ]),
    ("The pause", "one photo, a lot of paper — put one every six pages", [
        (0.06, 0.14, 0.34, 0.72, "photo"), (0.58, 0.44, 0.30, 0.10, "type"),
    ]),
    ("Detail pair", "the whole thing, then the close-up", [
        (0.03, 0.08, 0.42, 0.84, "photo"), (0.55, 0.08, 0.42, 0.56, "photo"),
        (0.55, 0.70, 0.28, 0.12, "type"),
    ]),
    ("Dedication", "inside page one — never the inside cover", [
        (0.55, 0.10, 0.42, 0.80, "photo"), (0.06, 0.42, 0.34, 0.10, "type"),
    ]),
]


def pdf_recipes():
    c = pdfcanvas.Canvas(os.path.join(OUT, "06-spread-recipes.pdf"), pagesize=letter)
    y = page(c, "Six spreads that respect the fold", "photo album kit · sheet 6")
    y = para(c, y, "Every layout below keeps faces, text and horizons out of the gutter band. "
                   "The pink stripe is the keep-out from sheet 1, drawn at the same scale.")
    y -= 8

    cols, cw = 2, (W - 2 * M - 22) / 2
    ch = cw * 0.375
    for i, (name, note, blocks) in enumerate(RECIPES):
        col, row = i % cols, i // cols
        x0 = M + col * (cw + 22)
        y0 = y - row * (ch + 54) - ch

        c.setFillColorRGB(0.99, 0.99, 0.98)
        c.rect(x0, y0, cw, ch, stroke=0, fill=1)
        for (l, t, bw, bh, kind) in blocks:
            c.setFillColorRGB(*(PHOTO if kind == "photo" else (0.82, 0.88, 0.93) if kind == "sky" else BOX))
            c.rect(x0 + l * cw, y0 + ch - (t + bh) * ch, bw * cw, bh * ch, stroke=0, fill=1)
            if kind == "type":
                c.setStrokeColorRGB(*GREY)
                c.setLineWidth(0.6)
                c.line(x0 + l * cw, y0 + ch - t * ch, x0 + (l + bw) * cw, y0 + ch - t * ch)
        # the keep-out band, over the artwork
        gfrac = GUTTER_MM / SPREAD_W_MM
        c.setFillColorRGB(0.98, 0.85, 0.93)
        c.setFillAlpha(0.55)
        c.rect(x0 + cw * (0.5 - gfrac), y0, cw * gfrac * 2, ch, stroke=0, fill=1)
        c.setFillAlpha(1)
        c.setStrokeColorRGB(*INK)
        c.setLineWidth(0.9)
        c.line(x0 + cw / 2, y0, x0 + cw / 2, y0 + ch)
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.8)
        c.rect(x0, y0, cw, ch, stroke=1, fill=0)

        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(x0, y0 - 15, f"{i + 1}. {name}")
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 8.8)
        for k, ln in enumerate(wrap(note, cw, 8.8)):
            c.drawString(x0, y0 - 27 - k * 11, ln)

    footer(c)
    c.save()


if __name__ == "__main__":
    pdf_gutter()
    pdf_planner()
    pdf_photos()
    pdf_brief()
    pdf_binding()
    pdf_recipes()
    print("6 sheets written to", OUT)
