#!/usr/bin/env python3
"""Lookbook Kit — the reference sheets that ship with the editable Canva
lookbook template (A4 landscape, cover + six spreads + contact page).

The colour-profile facts are quoted from Canva's own Help Centre and the source
is printed on the sheet so a buyer can check them. The trim arithmetic on the
bleed map is COMPUTED from the page size, so the diagram cannot drift from the
millimetres printed beside it.

Verified 2026-08-26 — canva.com/help/download-file-types.

Outputs (all US Letter):
  01-colour-guide.pdf        RGB vs CMYK, what survives, the free-plan options
  02-bleed-and-trim-map.pdf  page, bleed, trim and safe margin drawn to scale
  03-photo-prep.pdf          the 100%-zoom check and the resolution you need
  04-print-shop-brief.pdf    fill-in-the-blanks email, incl. the proof request
  05-export-checklist.pdf    print version vs screen version, side by side
  06-layout-recipes.pdf      six spread layouts that work, as diagrams
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
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
W, H = letter
M = 0.7 * inch

# ----------------------------------------------------------------- page ----
# A4 landscape, in millimetres. Every diagram below derives from these.
PAGE_W_MM, PAGE_H_MM = 297.0, 210.0
BLEED_MM = 3.0
SAFE_MM = 5.0

# Colours that survive the conversion, and colours that collapse. The CMYK
# column is the printed approximation, not a profile conversion — it is there
# to show the DIRECTION of the shift, which is the point of the sheet.
GAMUT = [
    ("Neon orange", (1.00, 0.42, 0.00), (0.85, 0.45, 0.18), "collapses"),
    ("Electric blue", (0.00, 0.47, 1.00), (0.25, 0.44, 0.66), "collapses"),
    ("Hot pink", (1.00, 0.18, 0.53), (0.82, 0.34, 0.54), "collapses"),
    ("Lime", (0.49, 1.00, 0.20), (0.56, 0.76, 0.40), "collapses"),
    ("Deep teal", (0.06, 0.37, 0.36), (0.08, 0.38, 0.36), "survives"),
    ("Burgundy", (0.42, 0.09, 0.18), (0.43, 0.11, 0.19), "survives"),
    ("Charcoal", (0.12, 0.14, 0.19), (0.14, 0.16, 0.20), "survives"),
]

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
    """A plain table. cols = header strings, widths = point widths."""
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



# ------------------------------------------------------------ 1 · colour ---
def pdf_colour():
    c = pdfcanvas.Canvas(os.path.join(OUT, "01-colour-guide.pdf"), pagesize=letter)
    y = page(c, "Why it printed duller", "COLOUR GUIDE")
    y = para(c, y, "Screens make colour with light — red, green and blue added together. "
                   "Printing makes colour with ink — cyan, magenta, yellow and black stacked "
                   "on paper. They cannot reach the same colours, so some of what you see on "
                   "screen simply does not exist in ink.")
    y -= 6
    y = heading(c, y, "Which colours survive the conversion")
    rows = [(n, s) for n, _, _, s in GAMUT]
    sw = 150
    for name, rgb, cmyk, status in GAMUT:
        c.setFillColorRGB(*rgb); c.rect(M, y - 16, sw, 20, stroke=0, fill=1)
        c.setFillColorRGB(*cmyk); c.rect(M + sw + 8, y - 16, sw, 20, stroke=0, fill=1)
        c.setFillColorRGB(*(PINK if status == "collapses" else GREEN))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(M + sw * 2 + 26, y - 10, status.upper())
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 10.5)
        c.drawString(M + sw * 2 + 100, y - 10, name)
        y -= 26
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 9)
    c.drawString(M, y - 4, "left: on screen   ·   right: roughly what ink reaches")
    y -= 26
    y = callout(c, y, "The setting is behind Pro", [
        "Canva's PDF Print export offers a \u201ccolor profile (RGB or CMYK) selection option\u201d.",
        "The same help page lists CMYK colour profile options among the features",
        "restricted to Pro, Teams, Education and Nonprofit accounts.",
        "So PDF Print works on a free plan — the CMYK choice inside it does not.",
        "Source: canva.com/help/download-file-types",
    ])
    y -= 10
    y = heading(c, y, "Three honest options on a free account")
    y = body(c, y, [
        "1.  Export PDF Print in RGB and tell the printer in writing that it is RGB.",
        "     Ask them to convert, and ask for a proof. Any decent shop does this daily.",
        "2.  Design in colours that survive. Deep colours convert well; neons do not.",
        "     Get a printed swatch before committing to a run.",
        "3.  Pay for one month of Pro, export, cancel. A few pounds against a print run.",
    ])
    footer(c); c.save()


# ------------------------------------------------------------- 2 · bleed ---
def pdf_bleed():
    c = pdfcanvas.Canvas(os.path.join(OUT, "02-bleed-and-trim-map.pdf"), pagesize=letter)
    y = page(c, "Bleed, trim and the safe margin", "TRIM MAP")
    y = para(c, y, "A printer prints on a larger sheet and cuts it down. That cut is accurate "
                   "to about a millimetre. Bleed is the margin of error: artwork that runs past "
                   "the trim so the blade is still cutting through your design.")
    y -= 10
    # drawn to scale from PAGE_W_MM / PAGE_H_MM
    scale = (W - M * 2 - 40) / (PAGE_W_MM + BLEED_MM * 2)
    bw, bh = (PAGE_W_MM + BLEED_MM * 2) * scale, (PAGE_H_MM + BLEED_MM * 2) * scale
    x0, y0 = M + 20, y - bh - 10
    c.setFillColorRGB(*BOX); c.rect(x0, y0, bw, bh, stroke=0, fill=1)
    tx, ty = x0 + BLEED_MM * scale, y0 + BLEED_MM * scale
    c.setStrokeColorRGB(*PINK); c.setLineWidth(1.2); c.setDash(4, 3)
    c.rect(tx, ty, PAGE_W_MM * scale, PAGE_H_MM * scale, stroke=1, fill=0)
    sx, sy = tx + SAFE_MM * scale, ty + SAFE_MM * scale
    c.setStrokeColorRGB(*GREEN)
    c.rect(sx, sy, (PAGE_W_MM - SAFE_MM * 2) * scale, (PAGE_H_MM - SAFE_MM * 2) * scale, stroke=1, fill=0)
    c.setDash()
    c.setFillColorRGB(*GREY); c.setFont("Helvetica", 9)
    c.drawString(x0, y0 - 14, "grey = bleed (%.0f mm)" % BLEED_MM)
    c.setFillColorRGB(*PINK); c.drawString(x0 + 150, y0 - 14, "pink dashes = trim (%.0f x %.0f mm)" % (PAGE_W_MM, PAGE_H_MM))
    c.setFillColorRGB(*GREEN); c.drawString(x0 + 340, y0 - 14, "green = safe margin (%.0f mm in)" % SAFE_MM)
    y = y0 - 40
    y = callout(c, y, "In Canva", [
        "Drag backgrounds and full-page images PAST the edge of the canvas.",
        "At download: PDF Print, then tick Crop marks and bleed. That checkbox is free.",
        "Nothing important — text, faces, prices — goes outside the green line.",
    ], col=GREEN)
    footer(c); c.save()


# ------------------------------------------------------------ 3 · photos ---
def pdf_photos():
    c = pdfcanvas.Canvas(os.path.join(OUT, "03-photo-prep.pdf"), pagesize=letter)
    y = page(c, "Photos that survive paper", "PHOTO PREP")
    y = para(c, y, "Print renders at 300 dpi — roughly four times the detail a screen needs. "
                   "A photo that looks perfect in the Canva editor can print soft, and you will "
                   "not find out until the box arrives.")
    y -= 6
    y = heading(c, y, "The five-second check")
    y = body(c, y, [
        "Zoom the editor to 100% and look at the photo at actual size.",
        "If it is soft there, it is worse on paper. There is no fix at export.",
    ])
    y -= 8
    y = heading(c, y, "What each placement needs, at 300 dpi")
    placements = [
        ("Full spread (297 x 210 mm)", "3508 x 2480 px"),
        ("Full page (148 x 210 mm)", "1754 x 2480 px"),
        ("Half page (148 x 105 mm)", "1754 x 1240 px"),
        ("Quarter (74 x 105 mm)", "874 x 1240 px"),
        ("Thumbnail (50 x 50 mm)", "591 x 591 px"),
    ]
    y = table(c, y, ["Placed at", "Minimum pixels"], placements, [300, 200])
    y -= 12
    y = callout(c, y, "Three rules", [
        "Shoot bigger than you think — you can always throw pixels away.",
        "Ask suppliers for the print versions, not the images off their website.",
        "Never scale a small photo up. Enlarging does not add detail.",
    ])
    footer(c); c.save()


# -------------------------------------------------------- 4 · print brief ---
def pdf_brief():
    c = pdfcanvas.Canvas(os.path.join(OUT, "04-print-shop-brief.pdf"), pagesize=letter)
    y = page(c, "What to send the print shop", "PRINT BRIEF")
    y = para(c, y, "Fill this in and paste it into the email with your PDF. It answers the four "
                   "questions every printer asks, and the last line is the one almost nobody "
                   "thinks to include.")
    y -= 10
    lines = [
        "Hello,",
        "",
        "I would like a quote for a lookbook.",
        "",
        "Finished size:      297 x 210 mm (A4 landscape)",
        "Pages:              ____________  (including cover)",
        "Quantity:           ____________",
        "Paper:              ____________  (your standard catalogue stock is fine)",
        "Binding:            ____________  (saddle-stitched unless you advise otherwise)",
        "",
        "The attached PDF is exported as PDF Print with crop marks and 3 mm bleed.",
        "The colour profile is ____________ (RGB / CMYK).",
        "If it is RGB, please convert it your end and let me know if anything shifts.",
        "",
        "Could I see a proof before the full run?",
        "",
        "Thank you,",
        "____________",
    ]
    c.setFillColorRGB(1, 1, 1)
    c.rect(M - 6, y - (len(lines) * 13) - 12, W - (M - 6) * 2, len(lines) * 13 + 16, stroke=0, fill=1)
    y = body(c, y - 6, lines, size=10, lead=13)
    y -= 14
    y = callout(c, y, "Why the proof matters", [
        "A proof is one printed copy before the run. It costs a little, and it is the only",
        "way to see the colour on your actual paper before you have paid for fifty.",
    ], col=GREEN)
    footer(c); c.save()


# ------------------------------------------------------------ 5 · export ---
def pdf_export():
    c = pdfcanvas.Canvas(os.path.join(OUT, "05-export-checklist.pdf"), pagesize=letter)
    y = page(c, "Two exports, in this order", "EXPORT CHECKLIST")
    y = para(c, y, "You are not making one lookbook. You are making two exports of the same "
                   "design — and sending a printer the wrong one wastes a week.")
    y -= 8
    rows = [
        ("File type", "PDF Print", "PDF Standard"),
        ("Crop marks and bleed", "ON", "off"),
        ("Colour profile", "CMYK (Pro) — else flag RGB", "RGB"),
        ("Resolution", "300 dpi", "screen"),
        ("Target size", "as large as needed", "under 10 MB"),
        ("Name it", "lookbook-print.pdf", "lookbook-screen.pdf"),
    ]
    y = table(c, y, ["", "FOR PAPER", "FOR SCREENS"], rows, [170, 190, 160])
    y -= 14
    y = heading(c, y, "Before you send either one")
    y = body(c, y, [
        "Open the PDF and look at page one at full size. Do not skip this.",
        "Check the trim: is anything important within 5 mm of the edge?",
        "Check the last page has a way to actually buy — email, phone, order link.",
        "DPI does not exist on a screen. Ignore that box for the screen version.",
    ])
    y -= 10
    y = callout(c, y, "The one that actually sells", [
        "The screen version is what gets seen — emailed, linked, read on a phone,",
        "and updated the moment a price changes. Most people over-invest in the print.",
    ], col=GREEN)
    footer(c); c.save()


# ----------------------------------------------------------- 6 · layouts ---
SPREADS = [
    ("Hero left", "one big image, three stacked, one block of type",
     [(0.02, 0.04, 0.44, 0.92, 1), (0.53, 0.04, 0.20, 0.44, 1), (0.75, 0.04, 0.23, 0.44, 1),
      (0.53, 0.53, 0.45, 0.30, 0), (0.53, 0.87, 0.18, 0.09, 0)]),
    ("Full bleed", "one photo across the gutter, type dropped on it",
     [(-0.02, -0.02, 1.04, 1.04, 1), (0.06, 0.70, 0.34, 0.20, 0)]),
    ("Grid of six", "for a range — same crop on every shot",
     [(0.03, 0.06, 0.28, 0.40, 1), (0.34, 0.06, 0.28, 0.40, 1), (0.68, 0.06, 0.28, 0.40, 1),
      (0.03, 0.52, 0.28, 0.40, 1), (0.34, 0.52, 0.28, 0.40, 1), (0.68, 0.52, 0.28, 0.40, 1)]),
    ("Quiet right", "one photo, a lot of paper — the pause page",
     [(0.04, 0.08, 0.40, 0.84, 1), (0.58, 0.36, 0.34, 0.16, 0)]),
    ("Detail pair", "the whole thing, then the close-up",
     [(0.03, 0.08, 0.44, 0.84, 1), (0.53, 0.08, 0.44, 0.60, 1), (0.53, 0.72, 0.30, 0.14, 0)]),
    ("Contact", "the last page — how to actually buy",
     [(0.03, 0.08, 0.44, 0.84, 1), (0.56, 0.24, 0.38, 0.14, 0), (0.56, 0.44, 0.38, 0.28, 0)]),
]


def pdf_layouts():
    c = pdfcanvas.Canvas(os.path.join(OUT, "06-layout-recipes.pdf"), pagesize=letter)
    y = page(c, "Six spreads that work", "LAYOUT RECIPES")
    y = para(c, y, "Identical geometry to the Canva template. Keep one grid across the whole "
                   "book and it reads as a house style — vary it every spread and it reads as "
                   "a scrapbook.")
    y -= 8
    sw = (W - M * 2 - 24) / 2
    sh = sw * 0.354
    for i, (name, note, blocks) in enumerate(SPREADS):
        col, row = i % 2, i // 2
        x0 = M + col * (sw + 24)
        y0 = y - row * (sh + 52) - sh
        c.setFillColorRGB(1, 1, 1); c.rect(x0, y0, sw, sh, stroke=0, fill=1)
        for (bl, bt, bw_, bh_, is_photo) in blocks:
            bx = x0 + max(0.0, bl) * sw
            by = y0 + sh - (bt + bh_) * sh
            bwid = min(bw_, 1.0 - max(0.0, bl)) * sw
            bhei = bh_ * sh
            if is_photo:
                c.setFillColorRGB(*BOX); c.rect(bx, max(y0, by), bwid, min(bhei, sh), stroke=0, fill=1)
            else:
                c.setStrokeColorRGB(*GREY); c.setLineWidth(0.6)
                c.line(bx, max(y0, by) + min(bhei, sh), bx + bwid, max(y0, by) + min(bhei, sh))
        c.setStrokeColorRGB(*GREY); c.setLineWidth(0.4)
        c.line(x0 + sw / 2, y0, x0 + sw / 2, y0 + sh)
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(x0, y0 - 14, name)
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 9)
        c.drawString(x0, y0 - 26, note)
    footer(c); c.save()


if __name__ == "__main__":
    pdf_colour(); pdf_bleed(); pdf_photos(); pdf_brief(); pdf_export(); pdf_layouts()
    print("wrote 6 PDFs")
