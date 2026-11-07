#!/usr/bin/env python3
"""Sticker + Illustration Starter Kit — the reference set that ships with the
editable Canva template.

Outputs (all US Letter):
  drawtool-brush-settings.pdf    what each brush is for, weights that work
  drawtool-shape-assist.pdf      the eight shapes and the one-second pause
  drawtool-stroke-budget.pdf     the 1 MB rule, what costs the most, the fix
  drawtool-sticker-checklist.pdf blank page → a sheet you can list
  drawtool-READ-ME.pdf           how to use the template, and the licence
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

PAPER = (0.984, 0.980, 0.973)
INK = (0.078, 0.094, 0.114)
TEAL = (0.184, 0.490, 0.471)
AMBER = (0.851, 0.604, 0.169)
GREY = (0.659, 0.690, 0.682)
PINK = (0.914, 0.118, 0.549)
W, H = letter
M = 0.85 * inch


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
    return y - 62


def footer(c):
    c.setFillColorRGB(0.62, 0.64, 0.63)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(W / 2, M - 16, "Genius Junkie · geniusjunkie.net")


def body(c, y, lines, size=10.5, lead=15, indent=0, col=(0.28, 0.30, 0.31)):
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


def callout(c, y, title, lines, col=PINK):
    h = 34 + 13 * len(lines)
    c.setStrokeColorRGB(*col)
    c.setLineWidth(2)
    c.roundRect(M, y - h, W - 2 * M, h + 6, 9, stroke=1, fill=0)
    c.setFillColorRGB(*col)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 14, y - 16, title)
    c.setFillColorRGB(0.28, 0.30, 0.31)
    c.setFont("Helvetica", 9.5)
    yy = y - 33
    for ln in lines:
        c.drawString(M + 14, yy, ln)
        yy -= 13
    return y - h - 18


def checkbox_list(c, y, items, gap=21):
    for q in items:
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(1)
        c.rect(M, y - 3, 11, 11, stroke=1, fill=0)
        c.setFillColorRGB(0.28, 0.30, 0.31)
        c.setFont("Helvetica", 10)
        c.drawString(M + 20, y, q)
        y -= gap
    return y


# ------------------------------------------------------------ brushes -------
def brush_settings(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "The four brushes", "sticker + illustration kit")
    y = body(c, y, [
        "Draw lives under Tools in the side panel — not Elements. Elements is for things",
        "Canva already made. Everything below is on the free plan.",
    ])
    y -= 16

    rows = [
        ("Pen", "Outlines, handwriting, anything deliberate.",
         "Weight 8–14 for sticker outlines. Type the number rather than dragging the",
         "slider if the whole set has to match."),
        ("Marker", "Filling, underlines, anything that should look quick.",
         "Weight 24–34. Softer edge than the pen, so it reads as a fill rather than",
         "a second outline."),
        ("Highlighter", "Shading. It is semi-transparent and it stacks.",
         "One pass for a soft shadow, two over the same spot for a darker one. Never",
         "use it for an outline — the overlap at every corner shows."),
        ("Eraser", "Removes whole strokes, not pixels.",
         "This is why you draw in short pieces. A long single stroke is all-or-nothing;",
         "six short ones can be repaired."),
    ]
    for name, what, l1, l2 in rows:
        c.setFillColorRGB(*PINK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(M, y, name)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", 10.5)
        c.drawString(M + 90, y, what)
        y -= 17
        y = body(c, y, [l1, l2], size=9.5, lead=13, indent=90)
        y -= 12

    y = heading(c, y, "Settings")
    y = body(c, y, [
        "Thickness takes a typed number as well as the presets — use it when a set has to match.",
        "Transparency at about 30% turns the pen into a sketch layer you can draw over.",
        "Hold Shift while dragging for a perfectly straight line. Works with every brush.",
    ], size=10, lead=14)
    y -= 10

    y = callout(c, y, "Pick the colour before the stroke", [
        "You cannot recolour a stroke after it is drawn. Everywhere else in Canva a wrong",
        "colour is one click to fix; in the draw tool it is a redraw. Seed the document",
        "colours row first (see the read-me) and pick from there every time.",
    ])
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------- shape assist -------
def shape_assist(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Draw badly. Pause. Get the clean one.", "sticker + illustration kit")
    y = body(c, y, [
        "You do not need a steady hand. Draw the shape, and then hold still for one",
        "second before lifting. Canva replaces it with a refined version.",
        "The pause is the whole trick — lift immediately and nothing happens.",
    ])
    y -= 20

    y = heading(c, y, "The eight it knows")
    shapes = ["Rectangles", "Arrows", "Triangles", "Circles", "Stars", "Lines", "Hearts", "Diamonds"]
    colw = (W - 2 * M) / 4
    for i, s in enumerate(shapes):
        col, row = i % 4, i // 4
        x = M + col * colw
        yy = y - row * 54
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(1)
        c.roundRect(x, yy - 34, colw - 12, 42, 7, stroke=1, fill=0)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(x + (colw - 12) / 2, yy - 18, s)
    y -= 122

    y = callout(c, y, "Where this actually earns its keep", [
        "Annotating a screenshot. Draw a rough box round the thing, hold one second, and",
        "you have a clean highlight box. Draw a rough arrow, hold, and you have an arrow.",
        "No Elements panel, no searching — and because it is still a drawing it keeps the",
        "weight and colour you set, so the whole annotation looks like one hand made it.",
    ], col=TEAL)

    y = heading(c, y, "If nothing happens")
    y = body(c, y, [
        "You lifted too early. One full second, completely still, at the end of the stroke.",
        "The shape also has to be recognisable — a squashed blob will not become a circle.",
        "Shift gives you a straight line without the pause, if a line is all you wanted.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------ stroke budget -------
def stroke_budget(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "The 1 MB stroke limit", "sticker + illustration kit")
    y = body(c, y, [
        "This is the one that costs people an afternoon, and it is in Canva's own help",
        "pages. Read it once and it will never happen to you.",
    ])
    y -= 16

    y = callout(c, y, "What actually happens", [
        "Every stroke is stored as a path. Once all the paths in one design pass 1 MB,",
        "Canva stops SAVING your drawings. It does not stop you drawing — the brush still",
        "works and the strokes still appear on screen. They are simply not being written",
        "to the file. You find out when you refresh and everything past the limit is gone.",
    ])

    y = heading(c, y, "The fix, in ten seconds")
    y = body(c, y, [
        "1.  Finish a page.",
        "2.  Duplicate the design — not the page, the design.",
        "3.  Carry on in the copy. Each design gets a fresh 1 MB.",
        "",
        "Already stuck? Delete some strokes and it will save again.",
    ], size=10.5, lead=15)
    y -= 12

    y = heading(c, y, "What eats the budget")
    for what, cost in [
        ("Long continuous strokes with lots of curve", "expensive"),
        ("Detailed shading and cross-hatching", "expensive"),
        ("Short outline strokes", "cheap"),
        ("Shape-assist shapes (they become clean geometry)", "cheap"),
        ("Text, photos, elements", "not counted — this limit is strokes only"),
    ]:
        c.setFillColorRGB(0.28, 0.30, 0.31)
        c.setFont("Helvetica", 10)
        c.drawString(M + 8, y, what)
        c.setFillColorRGB(*(AMBER if cost == "expensive" else TEAL))
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(W - M - 8, y, cost)
        y -= 18
    y -= 14

    y = heading(c, y, "Plan the set before you start")
    y = body(c, y, [
        "One design per four or five stickers is a comfortable working rule. Name them",
        "as you go — set 01, set 02 — and you can drop all of them onto one sheet at the",
        "end by copying the finished drawings across.",
    ], size=10, lead=14)
    y -= 16

    y = heading(c, y, "Working log")
    for lab in ["design 01", "design 02", "design 03", "design 04"]:
        c.setFillColorRGB(*TEAL)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M, y, lab.upper())
        c.setStrokeColorRGB(0.80, 0.82, 0.81)
        c.setLineWidth(0.8)
        c.line(M + 70, y - 2, W - M, y - 2)
        y -= 26
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------- checklist -------
def sticker_checklist(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Blank page to a sheet you can list", "sticker + illustration kit")
    y = body(c, y, [
        "Twelve steps. The order matters — four of them cannot be undone later.",
    ])
    y -= 16

    y = heading(c, y, "Before you draw")
    y = checkbox_list(c, y, [
        "New design, square, 2000 × 2000 px. Not a Doc — Draw is unavailable there.",
        "Drop four coloured shapes on the page to seed the document colours row.",
        "Tools → Draw. Set the pen weight by typing the number, not dragging.",
        "Pick the colour from the document colours row, never the rainbow picker.",
    ])
    y -= 8

    y = heading(c, y, "While you draw")
    y = checkbox_list(c, y, [
        "Short strokes, not long ones, so the eraser can repair them.",
        "Shift for anything straight.",
        "One second of stillness at the end of a shape for the clean version.",
        "Duplicate the design when a page is finished — before the 1 MB limit bites.",
    ])
    y -= 8

    y = heading(c, y, "Turning it into a product")
    y = checkbox_list(c, y, [
        "Copy the finished drawings onto the sticker sheet page in the template.",
        "Check every sticker sits inside the safe margin, away from the cut lines.",
        "Download as PDF Print, not PNG — the sheet is meant to be printed.",
        "Name the file with what it is and the sheet count, not \"final v3\".",
    ])
    y -= 6

    y = callout(c, y, "The transparent-background wall", [
        "Downloading with a transparent background is Canva Pro only, as are SVG exports.",
        "On the free plan a cut-out sticker exports as a PNG with a white box behind it.",
        "Two honest ways round it: sell the printable SHEET instead — no transparency",
        "needed, and it is a better product — or upgrade if you genuinely need die-cuts.",
    ])
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------------ read me -------
def readme(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Read me first", "sticker + illustration kit")

    blocks = [
        ("What's in this kit", [
            "The editable Canva template — the sticker sheet with cut lines and safe",
            "   margins, a tracing page, a brush-test page, and a palette page",
            "The four reference PDFs (brushes, shape assist, the stroke budget,",
            "   the sticker checklist)",
        ]),
        ("How to use the template", [
            "Open the template link — it copies into your own Canva account.",
            "Start on the PALETTE page. The four blocks there seed the document",
            "   colours row, which is the row you should pick every stroke from.",
            "   Change them to your colours first, before you draw anything.",
            "The BRUSH TEST page is scrap. Try weights there, not on your artwork.",
            "The TRACING page has the transparency already set — drop a photo in,",
            "   draw over it, then delete the photo. The strokes stay.",
            "The STICKER SHEET page has the cut lines and the safe margin. Copy your",
            "   finished drawings onto it at the end.",
        ]),
        ("The two rules that cannot be undone", [
            "Colour is baked into a stroke. You cannot recolour it afterwards, so pick",
            "   the colour first, every time.",
            "The eraser removes whole strokes, not pixels. Draw in short pieces or a",
            "   single mistake costs you the whole line.",
        ]),
        ("And the one that costs an afternoon", [
            "1 MB of strokes per design. Past that, Canva stops SAVING your drawings",
            "   without stopping you drawing them. Duplicate the design when a page is",
            "   done and carry on in the copy — each design gets a fresh 1 MB.",
        ]),
        ("Licence", [
            "Use this kit for your own stickers and illustrations, including ones you",
            "   sell, on unlimited products.",
            "You may not resell, share or redistribute the template or these PDFs",
            "   themselves, and you may not sell the kit as your own.",
        ]),
    ]
    for title, lines in blocks:
        y = heading(c, y, title)
        y = body(c, y, ["• " + ln if not ln.startswith("   ") else ln for ln in lines], size=9.5, lead=13)
        y -= 10

    footer(c)
    c.showPage()
    c.save()


if __name__ == "__main__":
    made = [
        ("drawtool-brush-settings.pdf", brush_settings),
        ("drawtool-shape-assist.pdf", shape_assist),
        ("drawtool-stroke-budget.pdf", stroke_budget),
        ("drawtool-sticker-checklist.pdf", sticker_checklist),
        ("drawtool-READ-ME.pdf", readme),
    ]
    for name, fn in made:
        fn(os.path.join(OUT, name))
    print(f"wrote {len(made)} PDFs")
