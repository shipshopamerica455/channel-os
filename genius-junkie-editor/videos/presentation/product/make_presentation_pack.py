#!/usr/bin/env python3
"""Presentation Kit — the reference sheets that ship with the editable Canva
business deck (1920 x 1080).

The handover table is the sheet the kit exists for: what each export keeps and
what it costs, with Canva's own wording quoted and the source printed so a buyer
can check it.

Verified 2026-08-29 — canva.com/help/download-file-types.

Outputs (all US Letter):
  01-handover-guide.pdf     link vs PDF vs PPTX, and how to choose
  02-font-safe-list.pdf     fonts that survive a PPTX export, and what to avoid
  03-chart-recipes.pdf      six chart types, when each is honest, what to strip
  04-headline-writing.pdf   turning labels into statements, before and after
  05-send-checklist.pdf     the four checks and the file-naming convention
  06-reusable-system.pdf    keeping the shell so the next deck is a fifth of the work
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

# Fonts that ship with BOTH Windows and macOS, so a PPTX opens as designed.
SAFE_FONTS = [
    ("Arial", "sans", "the safe default; Helvetica on Mac renders near-identically"),
    ("Calibri", "sans", "ships with Office; the PowerPoint house font"),
    ("Verdana", "sans", "wide, very legible on a projector"),
    ("Tahoma", "sans", "narrower than Verdana, same clarity"),
    ("Georgia", "serif", "the readable serif; good for quotes"),
    ("Times New Roman", "serif", "everywhere, but reads dated"),
    ("Courier New", "mono", "for code or figures only"),
    ("Trebuchet MS", "sans", "friendlier than Arial, still universal"),
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



# ---------------------------------------------------------- 1 · handover ---
def pdf_handover():
    c = pdfcanvas.Canvas(os.path.join(OUT, "01-handover-guide.pdf"), pagesize=letter)
    y = page(c, "Three doors out of Canva", "HANDOVER GUIDE")
    y = para(c, y, "Every deck leaves Canva one of three ways, and each one costs you "
                   "something different. Pick from one question: does this deck need to be "
                   "READ, PRESENTED, or EDITED?")
    y -= 8
    rows = [
        ("A LINK", "you present it", "everything works", "needs you there"),
        ("A PDF", "they read it", "layout + fonts frozen", "no animation"),
        ("A PPTX", "they edit it", "editable", "fonts swap, animation dies"),
    ]
    y = table(c, y, ["Door", "When", "Keeps", "Costs"], rows, [110, 130, 150, 160])
    y -= 14
    y = callout(c, y, "Canva's own wording, all from one help page", [
        "\u201cDesigns downloaded as PPTX or DOCX files may look different when opened in",
        "Microsoft Powerpoint or Microsoft Word.\u201d",
        "\u201cYou may need to make edits, or download and install the fonts you used in Canva",
        "to your device.\u201d",
        "\u201cAnimations and embedded videos are not yet supported in Microsoft PowerPoint",
        "and Microsoft Word \u2026 they may not play as expected.\u201d",
        "Source: canva.com/help/download-file-types",
    ])
    y -= 10
    y = heading(c, y, "If it has to be a PowerPoint")
    y = body(c, y, [
        "1.  Design in a system font from the start (see sheet 02).",
        "2.  Keep animation out of the deck entirely.",
        "3.  Export, then OPEN THE FILE YOURSELF and look at every slide.",
        "4.  Send it with a PDF alongside, so they can see what it should look like.",
    ])
    footer(c); c.save()


# --------------------------------------------------------------- 2 · fonts ---
def pdf_fonts():
    c = pdfcanvas.Canvas(os.path.join(OUT, "02-font-safe-list.pdf"), pagesize=letter)
    y = page(c, "Fonts that survive the trip", "FONT-SAFE LIST")
    y = para(c, y, "A PPTX does not carry the font with it. If the machine opening your deck "
                   "does not have it, PowerPoint substitutes something else and your line "
                   "breaks move. These ship with both Windows and macOS.")
    y -= 8
    y = table(c, y, ["Font", "Kind", "Notes"], [(n, k, note) for n, k, note in SAFE_FONTS], [140, 80, 320])
    y -= 14
    y = callout(c, y, "What to avoid in a deck that will be exported", [
        "Anything from Canva's font list that is not on the table above \u2014 however good it",
        "looks, it is not on your client's machine.",
        "Font pairings that rely on a distinctive display face for the headings.",
        "Very tight tracking: substituted fonts are usually wider, and tight lines break first.",
    ], col=PINK)
    y -= 10
    y = para(c, y, "If the deck is going out as a PDF or being presented from a link, none of "
                   "this applies. Use whatever you like.", col=GREY)
    footer(c); c.save()


# -------------------------------------------------------------- 3 · charts ---
CHARTS = [
    ("Column", "comparing a few things at one moment", "gridlines, 3D, legend if you can label directly"),
    ("Line", "change over time, three series maximum", "markers on every point, a second axis"),
    ("Bar", "ranking, or long category names", "sorting by anything except the value"),
    ("Stacked column", "parts of a whole over time", "more than four segments \u2014 nobody can read them"),
    ("Scatter", "relationship between two numbers", "a trend line you cannot justify"),
    ("Single number", "one figure that carries the slide", "a chart. If it is one number, say the number"),
]


def pdf_charts():
    c = pdfcanvas.Canvas(os.path.join(OUT, "03-chart-recipes.pdf"), pagesize=letter)
    y = page(c, "Six charts, and what to strip", "CHART RECIPES")
    y = para(c, y, "One chart per slide, and the chart gets a headline that says what it "
                   "means. Use Canva's chart element rather than pasting a screenshot from a "
                   "spreadsheet \u2014 a screenshot is at screen resolution and prints soft.")
    y -= 8
    y = table(c, y, ["Chart", "Use it for", "Strip out"], CHARTS, [130, 190, 220])
    y -= 14
    y = callout(c, y, "The rule that covers all six", [
        "If the audience has to look at the axis labels to understand the point,",
        "the headline is not doing its job. Fix the headline, not the chart.",
    ], col=GREEN)
    footer(c); c.save()


# ------------------------------------------------------------ 4 · headlines ---
PAIRS = [
    ("Q3 results", "Q3 revenue grew nineteen percent"),
    ("Revenue by quarter", "Revenue grew every quarter except the one we repriced"),
    ("Customer feedback", "Four in five customers named the same missing feature"),
    ("Market overview", "Two competitors left the category this year"),
    ("Next steps", "We need a decision on budget by the fifteenth"),
    ("Team structure", "One hire unblocks three of the four workstreams"),
]


def pdf_headlines():
    c = pdfcanvas.Canvas(os.path.join(OUT, "04-headline-writing.pdf"), pagesize=letter)
    y = page(c, "Labels and statements", "HEADLINE WRITING")
    y = para(c, y, "A label names the topic. A statement makes the point. If somebody reads "
                   "only your headlines, top to bottom, they should get the whole argument \u2014 "
                   "that is the test, and most decks fail it.")
    y -= 10
    for label, statement in PAIRS:
        c.setFillColorRGB(*PINK); c.setFont("Helvetica-Bold", 10)
        c.drawString(M, y, "LABEL")
        c.setFillColorRGB(*BODY); c.setFont("Helvetica", 11)
        c.drawString(M + 60, y, label)
        y -= 16
        c.setFillColorRGB(*GREEN); c.setFont("Helvetica-Bold", 10)
        c.drawString(M, y, "SAYS IT")
        c.setFillColorRGB(*INK); c.setFont("Helvetica-Bold", 11)
        c.drawString(M + 60, y, statement)
        y -= 26
    y -= 4
    y = callout(c, y, "The test", [
        "Read only the headlines, top to bottom. Do they tell the story on their own?",
        "If they do not, the deck does not work without you in the room \u2014 and it will be",
        "forwarded to somebody who was not in the room.",
    ])
    footer(c); c.save()


# --------------------------------------------------------------- 5 · send ---
def pdf_send():
    c = pdfcanvas.Canvas(os.path.join(OUT, "05-send-checklist.pdf"), pagesize=letter)
    y = page(c, "Before it goes", "SEND CHECKLIST")
    y = heading(c, y, "Four checks")
    y = body(c, y, [
        "1.  Read only the headlines, top to bottom. Do they tell the story alone?",
        "2.  Does anything touch the margins you set at the start?",
        "3.  If it is a PowerPoint: open the exported file and look at EVERY slide.",
        "4.  Check the numbers against the source, one more time.",
    ])
    y -= 12
    y = heading(c, y, "Name the file properly")
    y = para(c, y, "Not \u201cdeck final version two\u201d. Company, what it is, and the date \u2014 so "
                   "they can find it in their inbox in three weeks.")
    y = body(c, y, [
        "Acme \u2014 Q3 review \u2014 2026-09-14.pdf",
        "Acme \u2014 Q3 review \u2014 2026-09-14.pptx",
    ], col=INK)
    y -= 12
    y = callout(c, y, "Send both", [
        "If they asked for an editable file, send the PPTX and the PDF together.",
        "The PDF is what it is supposed to look like. It costs you nothing and it",
        "settles any argument about formatting before it starts.",
    ], col=GREEN)
    footer(c); c.save()


# ------------------------------------------------------------- 6 · system ---
def pdf_system():
    c = pdfcanvas.Canvas(os.path.join(OUT, "06-reusable-system.pdf"), pagesize=letter)
    y = page(c, "Keep the shell", "THE REUSABLE SYSTEM")
    y = para(c, y, "What you have built is not a presentation, it is a system. The second deck "
                   "takes about a fifth of the time the first one did \u2014 but only if you keep "
                   "the empty version.")
    y -= 8
    y = heading(c, y, "How to set it up")
    y = body(c, y, [
        "Delete the content from your finished deck, keep the four slide types.",
        "Duplicate the whole design and name it Deck Template.",
        "Put your brand colours in as a palette while you are in there.",
        "Every future deck starts from a copy of that, never from a blank page.",
        "Keep one page you never use in a real deck: all four layouts, shrunk down,",
        "side by side. It is the fastest way to remember the system in three months.",
    ])
    y -= 12
    y = heading(c, y, "The four slide types")
    y = table(c, y, ["Slide", "What it does"], [
        ("Title", "the name, who it is for, the date OF THE MEETING"),
        ("Section", "full-bleed colour, a number, three or four words"),
        ("Content", "statement headline, three lines max, one piece of evidence"),
        ("Closing", "what happens next \u2014 not \u201cthank you\u201d"),
    ], [130, 380])
    y -= 12
    y = callout(c, y, "If you work with other people", [
        "Share the shell. The fastest way to make everything look consistent is to",
        "make the consistent thing the easiest thing to start from.",
    ], col=GREEN)
    footer(c); c.save()


if __name__ == "__main__":
    pdf_handover(); pdf_fonts(); pdf_charts(); pdf_headlines(); pdf_send(); pdf_system()
    print("wrote 6 PDFs")
