#!/usr/bin/env python3
"""Digital Magazine Kit — the printable reference set that ships with the
editable Canva magazine template.

Outputs (all A4 portrait, the same shape as the magazine itself):
  magazine-grid-spec.pdf      the 15 mm margins + 3 columns, drawn to scale
  magazine-type-scale.pdf     the four sizes, set at their real sizes
  magazine-flatplan.pdf       a 16-page flatplan you fill in before designing
  magazine-link-map.pdf       every link in the issue, and where it points
  magazine-export-checklist.pdf  the six checks, printable and tickable
  magazine-READ-ME.pdf        how to use the template, and the licence
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

PAPER = (0.992, 0.984, 0.969)   # #fdfbf7
INK = (0.090, 0.082, 0.071)     # #171512
RED = (0.784, 0.251, 0.184)     # #c8402f
SLATE = (0.290, 0.353, 0.416)   # #4a5a6a
GREY = (0.725, 0.698, 0.655)    # #b9b2a7
PINK = (0.914, 0.118, 0.549)    # Genius Junkie pink
W, H = A4
M = 20 * mm


def page(c, title, kicker=None):
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - M
    if kicker:
        c.setFillColorRGB(*SLATE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(M, y + 4, kicker.upper())
        y -= 6
    c.setFillColorRGB(*RED)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, y - 20, title)
    c.rect(M, y - 34, 60, 3, stroke=0, fill=1)
    return y - 62


def footer(c):
    c.setFillColorRGB(0.62, 0.60, 0.57)
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawCentredString(W / 2, M - 12, "Genius Junkie · geniusjunkie.net")


def body(c, y, lines, size=10.5, lead=15, indent=0, col=(0.30, 0.28, 0.26)):
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


# ------------------------------------------------------------- grid spec ----
def grid_spec(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "The grid, drawn to scale", "digital magazine kit")

    y = body(c, y, [
        "This is a real A4 page with the template's grid on it. The margins are 15 mm",
        "from every edge; two guides split the live area into three even columns.",
    ])
    y -= 12

    # a scale drawing of the page inside the page
    pw = W - 2 * M - 62 * mm
    ph = pw * (297 / 210.0)
    px, py = M, y - ph
    c.setFillColorRGB(1, 1, 1)
    c.rect(px, py, pw, ph, stroke=0, fill=1)
    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(0.8)
    c.rect(px, py, pw, ph, stroke=1, fill=0)

    mg = pw * (15 / 210.0)
    c.setStrokeColorRGB(*PINK)
    c.setLineWidth(1.1)
    c.setDash(3, 3)
    c.rect(px + mg, py + mg * (210 / 297.0) * (297 / 210.0), pw - 2 * mg, ph - 2 * mg, stroke=1, fill=0)
    c.setDash()

    live = pw - 2 * mg
    for i in (1, 2):
        gx = px + mg + live * i / 3.0
        c.setStrokeColorRGB(*SLATE)
        c.setLineWidth(0.7)
        c.line(gx, py + mg, gx, py + ph - mg)

    c.setFillColorRGB(*RED)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(px + 4, py + ph - mg + 4, "15 mm margin")
    c.setFillColorRGB(*SLATE)
    c.drawString(px + mg + 4, py + mg - 12, "3 even columns")

    # the notes column
    nx = px + pw + 14
    ny = py + ph - 6
    for lab, val in [
        ("Canvas", "210 × 297 mm, portrait"),
        ("Pages", "single — never a spread"),
        ("Margin", "15 mm on all four edges"),
        ("Columns", "3 even, inside the margins"),
        ("Body", "1 or 2 columns"),
        ("Image", "the remaining column"),
        ("Pull quote", "breaks across 2"),
        ("Rulers", "File → Settings → Show rulers"),
    ]:
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(nx, ny, lab)
        c.setFillColorRGB(0.45, 0.43, 0.41)
        c.setFont("Helvetica", 8.5)
        c.drawString(nx, ny - 10, val)
        ny -= 30

    y = py - 24
    y = heading(c, y, "Why portrait, and why single pages")
    body(c, y, [
        "A magazine on paper is designed as a spread — two pages side by side, one wide",
        "canvas. On a phone held upright that spread renders as a strip of text about the",
        "height of a postage stamp. Nobody zooms; they leave. Single pages, portrait,",
        "unless you genuinely know your readers are on laptops.",
    ])
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------------ type scale ----
def type_scale(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "Four sizes, decided once", "digital magazine kit")

    y = body(c, y, [
        "Set these once, style one of each on a blank page, and leave that page in the",
        "file. From then on you copy a heading from there rather than restyling one.",
    ])
    y -= 16

    rows = [
        ("Headline", 48, "Helvetica-Bold", INK),
        ("A standfirst line", 20, "Helvetica", SLATE),
        ("Body text — the size everything is read at", 11, "Helvetica", INK),
        ("Caption", 8, "Helvetica", GREY),
    ]
    for label, size, font, col in rows:
        c.setFillColorRGB(*RED)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(M, y + size * 0.75, f"{size} PT")
        c.setFillColorRGB(*col)
        c.setFont(font, size)
        c.drawString(M + 46 * mm, y, label)
        y -= size + 26
        c.setStrokeColorRGB(0.88, 0.86, 0.84)
        c.setLineWidth(0.6)
        c.line(M, y + 12, W - M, y + 12)
        y -= 10

    y -= 10
    y = heading(c, y, "Two fonts, maximum")
    y = body(c, y, [
        "One for headlines, one for everything else. A third font is the fastest way to",
        "make a page look homemade.",
    ])
    y -= 14
    y = heading(c, y, "The pull quote")
    body(c, y, [
        "Take a sentence out of the body, set it at roughly three times body size, break",
        "it across two columns, and give it space above and below. That single element",
        "does more for how professional a spread reads than anything else on the page.",
    ])
    footer(c)
    c.showPage()
    c.save()


# -------------------------------------------------------------- flatplan ----
def flatplan(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "Flatplan — 16 pages", "digital magazine kit")
    y = body(c, y, [
        "Fill this in before you design anything. Knowing what is on page 11 is the",
        "difference between an afternoon and a weekend.",
    ])
    y -= 14

    cols, rows = 4, 4
    bw = (W - 2 * M - (cols - 1) * 8) / cols
    bh = bw * 1.2
    preset = {1: "COVER", 2: "CONTENTS", 3: "EDITOR'S LETTER", 16: "BACK PAGE / CTA"}
    n = 1
    for r in range(rows):
        for col in range(cols):
            bx = M + col * (bw + 8)
            by = y - bh - r * (bh + 20)
            c.setStrokeColorRGB(*GREY)
            c.setLineWidth(0.9)
            c.rect(bx, by, bw, bh, stroke=1, fill=0)
            c.setFillColorRGB(*RED)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(bx + 5, by + bh - 13, f"{n:02d}")
            if n in preset:
                c.setFillColorRGB(*SLATE)
                c.setFont("Helvetica-Bold", 7)
                c.drawString(bx + 5, by + bh - 26, preset[n])
            n += 1

    yy = y - rows * (bh + 20) - 6
    yy = heading(c, yy, "A working default")
    body(c, yy, [
        "01 cover · 02 contents · 03 editor's letter · 04–05 short pieces",
        "06 sponsor page · 07–10 the feature · 11 sponsor page · 12–14 interview",
        "15 short piece · 16 back page with your call to action",
    ])
    footer(c)
    c.showPage()
    c.save()


# -------------------------------------------------------------- link map ----
def link_map(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "Link map", "digital magazine kit")
    y = body(c, y, [
        "Every link in the issue, and where it points. Fill it in as you build, then use",
        "it as the click-test list once you have exported.",
    ])
    y -= 18

    heads = ["PAGE", "WHAT IS LINKED", "WHERE IT GOES", "TYPE", "✓"]
    xs = [M, M + 22 * mm, M + 78 * mm, M + 132 * mm, W - M - 10 * mm]
    c.setFillColorRGB(*RED)
    c.setFont("Helvetica-Bold", 8.5)
    for x, h in zip(xs, heads):
        c.drawString(x, y, h)
    y -= 8
    c.setStrokeColorRGB(*RED)
    c.setLineWidth(1.2)
    c.line(M, y, W - M, y)
    y -= 16

    seeded = [
        ("02", "contents line — The grid", "page 4", "in-doc"),
        ("02", "contents line — Feature", "page 7", "in-doc"),
        ("06", "sponsor button", "sponsor URL", "web"),
    ]
    c.setFont("Helvetica", 9)
    for i in range(18):
        row = seeded[i] if i < len(seeded) else ("", "", "", "")
        c.setFillColorRGB(0.30, 0.28, 0.26) if row[0] else c.setFillColorRGB(0.85, 0.83, 0.81)
        for x, v in zip(xs[:4], row):
            c.drawString(x, y, v or "")
        c.setStrokeColorRGB(0.86, 0.84, 0.82)
        c.setLineWidth(0.6)
        c.line(M, y - 6, W - M, y - 6)
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.9)
        c.rect(xs[4], y - 3, 10, 10, stroke=1, fill=0)
        y -= 22

    y -= 6
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M, y, "⚠  Links do not work on text with a text effect applied (Lift, Neon, that family).")
    y -= 14
    body(c, y, [
        "The link attaches perfectly in the editor and is simply dead in the exported file.",
        "Fix: duplicate the text, take the effect off the copy, put the link on the copy,",
        "and sit it exactly on top of the styled original.",
    ], size=9.5, lead=13)
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------------- checklist ----
def checklist(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "Before you send it", "digital magazine kit")

    checks = [
        ("Portrait, single pages — not spreads", "a spread on a phone is a postage stamp"),
        ("A grid and a type scale you can reuse", "15 mm margins, 3 columns, 4 sizes"),
        ("A contents page where every line links to its page", "Link → Pages in this document"),
        ("Every sponsor and product link attached", "and none of them on effect text"),
        ("Exported PDF Standard with Flatten UNTICKED", "Flatten strips every hyperlink out"),
        ("Open your own exported file and click three links", "the check everybody skips"),
    ]
    y -= 4
    for i, (t, sub) in enumerate(checks, 1):
        c.setStrokeColorRGB(0.45, 0.43, 0.41)
        c.setLineWidth(1.2)
        c.rect(M, y - 10, 16, 16, stroke=1, fill=0)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(M + 28, y, f"{i}. {t}")
        c.setFillColorRGB(0.45, 0.43, 0.41)
        c.setFont("Helvetica", 9.5)
        c.drawString(M + 28, y - 15, sub)
        y -= 46

    y -= 6
    c.setStrokeColorRGB(*PINK)
    c.setLineWidth(2)
    c.roundRect(M, y - 52, W - 2 * M, 58, 10, stroke=1, fill=0)
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M + 16, y - 18, "The one that decides whether it earns")
    c.setFillColorRGB(0.30, 0.28, 0.26)
    c.setFont("Helvetica", 10)
    c.drawString(M + 16, y - 36, "Flatten PDF bakes every layer into a flat image and strips out every hyperlink.")

    y -= 82
    y = heading(c, y, "The four mistakes that lose readers")
    body(c, y, [
        "landscape spreads — unusable in the only place it will actually be opened",
        "body text under about 11 pt — unreadable held at arm's length",
        "body text sitting directly on a full-page photograph — use a solid block",
        "exporting PDF Print for a digital file — 20 MB that half of email refuses",
    ], size=10, lead=15)
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------------------- read me ----
def readme(path):
    c = pdfcanvas.Canvas(path, pagesize=A4)
    y = page(c, "Read me first", "digital magazine kit")

    blocks = [
        ("What's in this kit", [
            "The editable Canva magazine template — cover, contents page with the",
            "   links already wired, feature layout, sponsor page and the parts bin",
            "The five reference PDFs in this folder (grid spec, type scale, flatplan,",
            "   link map, export checklist)",
        ]),
        ("How to use the template", [
            "Open the template link — it copies into your own Canva account.",
            "Page 1 is the cover: drop one photograph in edge to edge (the cover is",
            "   the one page that ignores the guides), then set the masthead.",
            "Page 2 is the contents page. Select each line, hit Link, and choose",
            "   Pages in this document — that is what makes it jump.",
            "Pages 3–5 are the feature, the sponsor page and the parts bin.",
            "Duplicate pages as you need them; the grid comes with each copy.",
        ]),
        ("Exporting (the part that matters)", [
            "Share → Download → PDF Standard, not PDF Print.",
            "Leave the Flatten PDF checkbox UNTICKED. Flatten bakes every layer",
            "   into a flat image and strips out every hyperlink in the document —",
            "   and the file still looks completely perfect, so nobody catches it.",
            "Then open your own exported file and click three links.",
        ]),
        ("The other two delivery routes", [
            "Share → Publish as a website gives you a free .canva.site address, and",
            "   every link still works. On the free plan you can keep up to five live",
            "   websites at once. A PDF is frozen the second somebody downloads it;",
            "   a website you can just fix. Do both.",
            "A true page-turn flipbook needs a viewer outside Canva. Feed it exactly",
            "   the PDF you just made. Most are monthly subscriptions and most host",
            "   your file, so the day you stop paying, the link stops working.",
        ]),
        ("For the next issue", [
            "Duplicate the whole design, swap the photographs and the words, change",
            "   the issue line. The layout is already solved.",
            "Because every issue uses the same grid and the same two fonts, back",
            "   issues start to look like a publication rather than a folder of",
            "   unrelated PDFs — which is what makes a sponsor take you seriously.",
        ]),
        ("Licence", [
            "Use this kit for your own magazines, including ones you sell or take",
            "   sponsorship for, on unlimited issues.",
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
        ("magazine-grid-spec.pdf", grid_spec),
        ("magazine-type-scale.pdf", type_scale),
        ("magazine-flatplan.pdf", flatplan),
        ("magazine-link-map.pdf", link_map),
        ("magazine-export-checklist.pdf", checklist),
        ("magazine-READ-ME.pdf", readme),
    ]
    for name, fn in made:
        fn(os.path.join(OUT, name))
    print(f"wrote {len(made)} PDFs")
