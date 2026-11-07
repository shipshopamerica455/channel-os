#!/usr/bin/env python3
"""Menu Template Pack — print-ready sample PDFs + quick-start guide.

Outputs (US Letter):
  menu-sample.pdf            the finished menu, flatten-style (home printing)
  menu-sample-cropmarks.pdf  same artwork + 0.125" bleed and crop marks (print shop)
  menu-pack-guide.pdf        1-page quick start: Canva template link, export recipes, checklist
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas

# The Canva template link is the paid product, so it is not in this file. It
# comes from gitignored pipeline/canva-links.json; without it the PDF would ship
# a dead link, so this fails loudly instead of guessing.
import json as _json, pathlib as _pathlib
TEMPLATE_LINK = _json.loads(
    (_pathlib.Path(__file__).resolve().parents[3] / "pipeline" / "canva-links.json").read_text()
)["links"]["restaurant-menu"]["canvaTemplate"]

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = letter  # 612 x 792 pt

PAPER = (0.98, 0.965, 0.933)   # #faf6ee
INK = (0.169, 0.129, 0.094)    # #2b2118
DIM = (0.42, 0.373, 0.322)     # #6b5f52
ACCENT = (0.71, 0.263, 0.18)   # #b5432e

STARTERS = [
    ("Whipped Feta & Honey", "8", "warm flatbread, chilli oil, toasted seeds"),
    ("Crispy Squid", "9", "lemon aioli, parsley, cracked pepper"),
    ("Roast Tomato Soup", "7", "basil cream, sourdough croutons"),
]
MAINS = [
    ("Slow-Braised Beef Shortrib", "19", "red wine, rosemary, buttered mash"),
    ("Wood-Fired Half Chicken", "16", "smoked paprika, charred lemon, house fries"),
    ("Wild Mushroom Risotto", "14", "aged parmesan, truffle oil, crispy sage"),
    ("Pan-Seared Salmon", "18", "brown butter, capers, seasonal greens"),
    ("The House Burger", "15", "dry-aged beef, smoked cheddar, pickles"),
]
DESSERTS = [
    ("Basque Cheesecake", "7", "burnt top, vanilla cream"),
    ("Dark Chocolate Torte", "8", "sea salt, crème fraîche"),
]


def draw_menu(c, ox=0.0, oy=0.0, bleed=0.0):
    """Draw the menu artwork; ox/oy offset the page origin, bleed extends the bg."""
    c.setFillColorRGB(*PAPER)
    c.rect(ox - bleed, oy - bleed, W + 2 * bleed, H + 2 * bleed, stroke=0, fill=1)

    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(ox + W / 2, oy + H - 1.0 * inch, "THE OLIVE & FIG")
    c.setFillColorRGB(*DIM)
    c.setFont("Helvetica", 11)
    c.drawCentredString(ox + W / 2, oy + H - 1.28 * inch, "Wood-fired kitchen · Est. 2011")
    c.setFillColorRGB(*ACCENT)
    c.rect(ox + W / 2 - 0.5 * inch, oy + H - 1.45 * inch, 1.0 * inch, 2.2, stroke=0, fill=1)

    y = H - 2.0 * inch
    for label, dishes in (("STARTERS", STARTERS), ("MAINS", MAINS), ("DESSERTS", DESSERTS)):
        c.setFillColorRGB(*ACCENT)
        c.setFont("Helvetica-Bold", 12)
        t = c.beginText(ox + 0.75 * inch, oy + y)
        t.setCharSpace(2.5)
        t.textOut(label)
        c.drawText(t)
        y -= 0.32 * inch
        for name, price, desc in dishes:
            c.setFillColorRGB(*INK)
            c.setFont("Helvetica-Bold", 12.5)
            c.drawString(ox + 0.75 * inch, oy + y, f"{name}   {price}")
            y -= 0.19 * inch
            c.setFillColorRGB(*DIM)
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(ox + 0.75 * inch, oy + y, desc)
            y -= 0.30 * inch
        y -= 0.12 * inch

    # QR placeholder + labels
    qx, qy, qs = ox + 0.75 * inch, oy + 0.7 * inch, 0.8 * inch
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.6)
    c.roundRect(qx, qy, qs, qs, 5, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColorRGB(*DIM)
    c.drawCentredString(qx + qs / 2, qy + qs / 2 - 2, "YOUR QR")
    c.setFont("Helvetica", 9.5)
    c.drawString(qx + qs + 0.18 * inch, qy + qs / 2 + 2, "Scan for allergens & the full drinks list")
    c.setFont("Helvetica-Oblique", 9)
    c.drawRightString(ox + W - 0.75 * inch, qy + 2, "— ask your server about today's specials —")


def sample_flat():
    p = os.path.join(OUT, "menu-sample.pdf")
    c = pdfcanvas.Canvas(p, pagesize=letter)
    draw_menu(c)
    c.showPage()
    c.save()
    return p


def sample_cropmarks():
    b = 0.125 * inch          # bleed
    m = 0.25 * inch           # margin for the marks
    pw, ph = W + 2 * (b + m), H + 2 * (b + m)
    p = os.path.join(OUT, "menu-sample-cropmarks.pdf")
    c = pdfcanvas.Canvas(p, pagesize=(pw, ph))
    ox = oy = b + m
    draw_menu(c, ox, oy, bleed=b)
    # crop marks at the TRIM box corners
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.6)
    L = 0.18 * inch
    g = 0.06 * inch  # gap from trim
    for cx, cy, dx, dy in ((ox, oy, -1, -1), (ox + W, oy, 1, -1), (ox, oy + H, -1, 1), (ox + W, oy + H, 1, 1)):
        c.line(cx + dx * g, cy, cx + dx * (g + L), cy)
        c.line(cx, cy + dy * g, cx, cy + dy * (g + L))
    c.showPage()
    c.save()
    return p


def guide():
    p = os.path.join(OUT, "menu-pack-guide.pdf")
    c = pdfcanvas.Canvas(p, pagesize=letter)
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(0.75 * inch, H - 1.0 * inch, "Menu Template Pack — Quick Start")
    c.setFillColorRGB(*ACCENT)
    c.rect(0.75 * inch, H - 1.12 * inch, 1.4 * inch, 2.4, stroke=0, fill=1)

    def block(y, title, lines):
        c.setFillColorRGB(*ACCENT)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(0.75 * inch, y, title)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", 11)
        yy = y - 0.26 * inch
        for ln in lines:
            c.drawString(0.95 * inch, yy, ln)
            yy -= 0.22 * inch
        return yy - 0.18 * inch

    y = H - 1.7 * inch
    y = block(y, "1 · OPEN THE EDITABLE TEMPLATE", [
        "Open this link (free Canva account is fine) — it makes your own private copy:",
        TEMPLATE_LINK,
        "Nothing you change affects anyone else's copy.",
    ])
    y = block(y, "2 · MAKE IT YOURS (10 MINUTES)", [
        "Replace the restaurant name + identity line, then your dishes.",
        "Keep ~7 items per section · write appetite, not inventory.",
        "Prices: no currency symbols, no trailing zeros, tucked at the line end",
        "(the Cornell trick from the video — diners spend more without the $).",
        "Swap the QR placeholder: Apps → \"QR Code\" → paste your allergens/drinks link.",
        "Test the QR with your own phone BEFORE printing.",
    ])
    y = block(y, "3 · EXPORT — TWO RECIPES", [
        "PRINT SHOP:  Share → Download → PDF Print → tick \"Crop marks and bleed\".",
        "HOME/OFFICE:  PDF Print → untick crop marks → tick \"Flatten PDF\".",
        "Ask for 300gsm stock or lamination — standard paper dies in a week.",
    ])
    y = block(y, "4 · WHAT'S IN THIS PACK", [
        "menu-sample.pdf — the finished design (home-print reference)",
        "menu-sample-cropmarks.pdf — the professional print-shop handoff format",
        "The editable Canva template (link above) — yours to keep, all future tweaks free",
    ])
    c.setFillColorRGB(*DIM)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, 0.6 * inch, "© Genius Junkie · geniusjunkie.net · single-venue licence — not for resale")
    c.showPage()
    c.save()
    return p


for f in (sample_flat(), sample_cropmarks(), guide()):
    print("wrote", os.path.basename(f))
