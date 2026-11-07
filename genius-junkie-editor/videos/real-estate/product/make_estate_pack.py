#!/usr/bin/env python3
"""Real Estate Listing Kit — the reference sheets that ship with the editable
Canva listing kit (A4 portrait window card, flyer, brochure pages, social set).

The licence clauses are quoted verbatim from Canva's own Content License
Agreement and the source is printed on the sheet, so a buyer can take it
straight to their broker. The A4 geometry on the safe-zone map is COMPUTED from
the page size, so the diagram cannot drift from the millimetres printed beside
it.

Verified 2026-09-01 — canva.com/policies/content-license-agreement.

Outputs (all US Letter):
  01-licence-summary.pdf     the clauses, in plain English, with the source
  02-window-card-map.pdf     A4 portrait drawn to scale with the 15 mm guide
  03-photography-shot-list.pdf  walking a property so nothing is missed
  04-portal-export-spec.pdf  what each export is for, and how to check
  05-hierarchy-guide.pdf     three things large, everything else quiet
  06-compliance-band.pdf     what goes on every piece, and locking it
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

PAPER = (0.984, 0.980, 0.973)
INK = (0.086, 0.125, 0.180)
BLUE = (0.071, 0.231, 0.369)
AMBER = (0.961, 0.620, 0.043)
GREY = (0.659, 0.690, 0.682)
PINK = (0.914, 0.118, 0.549)
GREEN = (0.133, 0.773, 0.369)
BODY = (0.28, 0.30, 0.31)
W, H = letter
M = 0.7 * inch

# The window card, in millimetres. Every diagram derives from these.
PAGE_W_MM, PAGE_H_MM = 210.0, 297.0     # A4 portrait
GUIDE_MM = 15.0                          # frames eat the outside edge
BLEED_MM = 3.0

SRC = "canva.com/policies/content-license-agreement — verified 1 September 2026"


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
    c.setFont("Helvetica-Bold", 23)
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
        wrapped.extend(wrap(ln, w - 28, 9.5) if ln else [""])
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


def checkbox_list(c, y, items, size=10.5, lead=19):
    for t in items:
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.9)
        c.rect(M, y - 2, 10, 10, stroke=1, fill=0)
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", size)
        c.drawString(M + 20, y, t)
        y -= lead
    return y


# --------------------------------------------------------- 1 · the licence ---
def pdf_licence():
    c = pdfcanvas.Canvas(os.path.join(OUT, "01-licence-summary.pdf"), pagesize=letter)
    y = page(c, "The clauses, in plain English", "listing kit · sheet 1")
    y = para(c, y, "This sheet exists so you can take one page to your broker or compliance lead "
                   "rather than a video. Everything in quotes is Canva's own wording and the "
                   "source is printed at the bottom.")
    y -= 8

    y = callout(c, y, "Model releases — the one that matters for property marketing", [
        "\"Releases are generally not obtained for Free Content, and some jurisdictions",
        "provide legal protection against a person's image, likeness or property being",
        "used for commercial purposes when they have not provided a release.\"",
        "",
        "Note the wording: image, likeness OR PROPERTY. Property marketing is",
        "commercial use, and the agreement puts the job of deciding whether a release",
        "is needed — and getting it — on you, not on Canva.",
    ])

    y = callout(c, y, "Endorsement", [
        "\"You may not use Branded Content in any way that implies endorsement,",
        "affiliation, or sponsorship by the brand or its affiliates.\"",
        "",
        "A stock headshot beside a testimonial presents a model as a genuine client",
        "endorsing your business. Do not do it.",
    ], col=AMBER)

    y = callout(c, y, "Standalone use", [
        "Content may not be used or displayed \"on a standalone basis\" in venues",
        "designed to sell or distribute on-demand products. A Canva stock photo is",
        "not something you can sell as the product itself.",
    ], col=BLUE)

    y = heading(c, y, "What that means on a Tuesday morning")
    y = checkbox_list(c, y, [
        "No stock people on the flyer",
        "No stock people on the window card",
        "No stock people on a testimonial card — ever",
        "Photographs of the property are photographs OF THE PROPERTY",
        "If you need a person, it is you. Photograph yourself once, properly.",
    ])
    y -= 6
    y = para(c, y, "This sheet is not legal advice, and agents are regulated differently in every "
                   "market. It is the sentence to go and ask about.", size=9.5, lead=13)
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(M, M + 6, SRC)
    footer(c)
    c.save()


# ----------------------------------------------------- 2 · window card map ---
def pdf_map():
    c = pdfcanvas.Canvas(os.path.join(OUT, "02-window-card-map.pdf"), pagesize=letter)
    y = page(c, "The window card, drawn to scale", "listing kit · sheet 2")
    y = para(c, y, "A window card sits behind glass in a frame, and frames eat the outside edge. "
                   "Everything that matters lives inside the guide.")
    y -= 6

    avail_h = 4.6 * inch
    scale = avail_h / (PAGE_H_MM * mm)
    pw = PAGE_W_MM * mm * scale
    ph = PAGE_H_MM * mm * scale
    x0, y0 = M, y - ph

    c.setFillColorRGB(1, 1, 1)
    c.rect(x0, y0, pw, ph, stroke=0, fill=1)
    g = GUIDE_MM * mm * scale
    c.setStrokeColorRGB(*PINK)
    c.setLineWidth(1.1)
    c.setDash(4, 3)
    c.rect(x0 + g, y0 + g, pw - 2 * g, ph - 2 * g, stroke=1, fill=0)
    c.setDash()
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.0)
    c.rect(x0, y0, pw, ph, stroke=1, fill=0)

    # the three zones, to scale
    inner_w = pw - 2 * g
    hero_h = (ph - 2 * g) * 0.50
    c.setFillColorRGB(0.80, 0.87, 0.92)
    c.rect(x0 + g, y0 + ph - g - hero_h, inner_w, hero_h, stroke=0, fill=1)
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x0 + g + 6, y0 + ph - g - hero_h + 8, "HERO PHOTOGRAPH — TOP HALF")
    c.setFont("Helvetica-Bold", 15)
    c.drawString(x0 + g + 6, y0 + ph - g - hero_h - 24, "THE PRICE")
    c.setFont("Helvetica", 10)
    c.drawString(x0 + g + 6, y0 + ph - g - hero_h - 40, "the location")
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 7)
    for i, t in enumerate(["everything else, deliberately quiet", "bedrooms · tenure · size", "your number"]):
        c.drawString(x0 + g + 6, y0 + g + 34 - i * 10, t)
    c.setFillColorRGB(*BLUE)
    c.rect(x0, y0, pw, g * 0.9, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x0 + 6, y0 + g * 0.32, "NAME · AGENCY · REGISTRATION")

    tx = x0 + pw + 26
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(tx, y - 14, f"{GUIDE_MM:.0f} MM GUIDE, ALL ROUND")
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 9.5)
    for i, ln in enumerate(wrap("Frames overlap the edge of the card. Anything closer than fifteen "
                                "millimetres to the trim can disappear behind the rebate.", W - tx - M, 9.5)):
        c.drawString(tx, y - 32 - i * 13, ln)

    y = y0 - 26
    y = table(c, y, ["measurement", "millimetres", "inches"], [
        ("Window card / flyer", f"{PAGE_W_MM:.0f} x {PAGE_H_MM:.0f}", "A4 portrait"),
        ("US equivalent", "216 x 279", "Letter portrait"),
        ("Guide, all round", f"{GUIDE_MM:.0f}", "0.59"),
        ("Bleed, if a print shop asks", f"{BLEED_MM:.0f}", "0.12"),
    ], [2.9 * inch, 2.0 * inch, 1.4 * inch])
    footer(c)
    c.save()


# ------------------------------------------------------- 3 · the shot list ---
def pdf_shots():
    c = pdfcanvas.Canvas(os.path.join(OUT, "03-photography-shot-list.pdf"), pagesize=letter)
    y = page(c, "Walking a property", "listing kit · sheet 3")
    y = para(c, y, "Print this and carry it. The point is not artistry — it is coming back with "
                   "every shot you need, so you never design around a photograph you did not take.")
    y -= 6
    y = callout(c, y, "Before you start", [
        "Bright but overcast, so the windows are not blown out. Every light on anyway.",
        "Shoot each room from its corner, not its doorway — corners show the real size.",
        "Tidy first. Ten minutes of tidying beats an hour of editing.",
    ], col=GREEN)

    for group, shots in [
        ("Outside", ["Front elevation, straight on", "Front, three-quarter angle",
                     "The street looking both ways", "Garden from the house",
                     "Garden looking back at the house", "Parking / garage / access"]),
        ("Inside — every room", ["Wide from the corner", "The feature (fireplace, island, view)",
                                 "Looking back toward the door"]),
        ("Do not forget", ["Kitchen from two corners", "Bathroom without your reflection",
                           "Boiler, meter, consumer unit", "Loft hatch / storage",
                           "The view from the main bedroom", "Anything the vendor is proud of"]),
    ]:
        y = heading(c, y, group)
        y = checkbox_list(c, y, shots, lead=17)
        y -= 8

    y = para(c, y, "If a photograph is genuinely poor, go back — do not compensate in the design. "
                   "The listing looks honest, which is the thing you are actually selling.",
             size=9.5, lead=13)
    footer(c)
    c.save()


# --------------------------------------------------------- 4 · export spec ---
def pdf_export():
    c = pdfcanvas.Canvas(os.path.join(OUT, "04-portal-export-spec.pdf"), pagesize=letter)
    y = page(c, "Three exports, one design", "listing kit · sheet 4")
    y = para(c, y, "The same design leaves Canva three different ways, and using the wrong one is "
                   "the most common reason a flyer looks soft or a portal upload gets rejected.")
    y -= 8
    y = table(c, y, ["where it is going", "download as", "watch for"], [
        ("Office printer", "PDF Print", "nothing — it just works"),
        ("A print shop", "PDF Print", "tick crop marks + bleed"),
        ("A property portal", "JPEG or PDF", "their own spec sheet"),
        ("Social", "PNG, square", "rebuild, do not shrink"),
    ], [2.4 * inch, 1.9 * inch, 2.4 * inch])

    y = callout(c, y, "Every portal publishes a spec sheet — and they do not agree", [
        "Before you export for a portal, find their current image and PDF requirements",
        "and write the numbers in the box below. They change, and they differ between",
        "portals in the same market.",
    ], col=AMBER)

    y = heading(c, y, "Your portals")
    for i in range(4):
        yy = y - i * 52
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.7)
        c.roundRect(M, yy - 40, W - 2 * M, 44, 5, stroke=1, fill=0)
        c.setFillColorRGB(*GREY)
        c.setFont("Helvetica", 8.5)
        for lbl, dx in [("portal", 12), ("image size", 2.3 * inch), ("file type", 4.1 * inch), ("max MB", 5.6 * inch)]:
            c.drawString(M + dx, yy - 32, lbl)
        c.setStrokeColorRGB(0.85, 0.86, 0.85)
        c.line(M + 12, yy - 14, W - M - 12, yy - 14)
    y = y - 4 * 52 - 10

    y = heading(c, y, "The social set")
    y = para(c, y, "Duplicate the design, resize the copy to a square, and rebuild the same three "
                   "pieces of information for a phone. Not a shrunk flyer — the detail band that "
                   "works at arm's length is invisible at thumbnail size.", size=10, lead=14)
    footer(c)
    c.save()


# ---------------------------------------------------------- 5 · hierarchy ---
def pdf_hierarchy():
    c = pdfcanvas.Canvas(os.path.join(OUT, "05-hierarchy-guide.pdf"), pagesize=letter)
    y = page(c, "Three things large", "listing kit · sheet 5")
    y = para(c, y, "Somebody walking past your window gives it about three seconds. That buys you "
                   "three pieces of information, in this order.")
    y -= 8
    y = table(c, y, ["rank", "element", "how big"], [
        ("1", "The price", "largest type on the page"),
        ("2", "The location", "under it, smaller but still large"),
        ("3", "One photograph", "the top half, minimum"),
        ("—", "Everything else", "small, in a band at the bottom"),
    ], [0.9 * inch, 2.6 * inch, 3.2 * inch])

    y = callout(c, y, "The test", [
        "Export the card, put it on your phone, and look at it from across the room.",
        "If the price is not the first thing you can read, the type is not big enough.",
        "This takes thirty seconds and it is the only layout test that matters here.",
    ], col=GREEN)

    y = heading(c, y, "Where the floor plan goes")
    y = para(c, y, "Not on the window card — it is unreadable at that size and it steals room from "
                   "the photograph. Put it on the back of the flyer, or on its own brochure page, "
                   "where somebody is holding it. A floor plan is what buyers study the longest "
                   "once they are interested, and almost never before they are.")
    y -= 4
    y = heading(c, y, "The second tier, in full")
    y = body(c, y, [
        "· bedrooms and bathrooms",
        "· tenure",
        "· floor area",
        "· EPC / energy rating",
        "· council tax or local property tax band",
        "· your telephone number",
    ], size=10.5, lead=16)
    footer(c)
    c.save()


# --------------------------------------------------- 6 · compliance band ---
def pdf_compliance():
    c = pdfcanvas.Canvas(os.path.join(OUT, "06-compliance-band.pdf"), pagesize=letter)
    y = page(c, "The band on every piece", "listing kit · sheet 6")
    y = para(c, y, "Every item in the kit carries the same three things in the same place. Set it "
                   "once, group it, lock it, and stop thinking about it.")
    y -= 8
    y = table(c, y, ["what", "example", "why"], [
        ("Your name", "A. Morrow", "buyers ring a person"),
        ("Your agency", "Hexham", "and check the agency"),
        ("Registration", "REG 04482", "whatever your market requires"),
    ], [1.9 * inch, 2.2 * inch, 3.0 * inch])

    y = callout(c, y, "Group it and lock it in Canva", [
        "Select the three elements → right-click → Group. Then click the padlock.",
        "A locked group cannot be dragged out of place while you are working quickly,",
        "which is the actual failure mode. Nobody deletes their registration number",
        "on purpose — it gets nudged off the artboard on the fourth flyer of a busy week.",
    ], col=BLUE)

    y = heading(c, y, "Check before every send")
    y = checkbox_list(c, y, [
        "The band is present on all four pieces",
        "The registration line matches what your market requires today",
        "The group is still locked",
        "The phone number is the one you actually answer",
        "No stock people anywhere",
        "Every photograph is of this property",
    ])
    y -= 8
    y = para(c, y, "Requirements differ by market and they change. Confirm the exact wording with "
                   "your broker or compliance lead, then set it once here.", size=9.5, lead=13)
    footer(c)
    c.save()


if __name__ == "__main__":
    pdf_licence()
    pdf_map()
    pdf_shots()
    pdf_export()
    pdf_hierarchy()
    pdf_compliance()
    print("6 sheets written to", OUT)
