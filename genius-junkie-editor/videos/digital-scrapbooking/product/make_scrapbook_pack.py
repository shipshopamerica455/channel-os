#!/usr/bin/env python3
"""Scrapbook + Photo Book Kit — the reference set that ships with the editable
Canva scrapbook.

The layout recipes are DRAWN, not described: each one is a real proportional
diagram of the page, so the buyer can see the geometry rather than read about
it. That is the part people actually get wrong — every page designed from
scratch, none of them matching.

Every Canva limit quoted in here is from Canva's own Help Centre, checked
2026-08-19. Sources are printed on the read-me so the buyer can verify them.

Outputs (all US Letter):
  scrapbook-layout-recipes.pdf      six page layouts, drawn to proportion
  scrapbook-photo-prep.pdf          getting photos in, and the real limits
  scrapbook-export-checklist.pdf    where is it going -> which settings
  scrapbook-print-brief.pdf         a brief you can send a print shop as-is
  scrapbook-journaling-prompts.pdf  what to write when the box is empty
  scrapbook-READ-ME.pdf             how to use the template, and the licence
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
BODY = (0.28, 0.30, 0.31)
PHOTO = (0.855, 0.886, 0.906)
W, H = letter
M = 0.7 * inch


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


def callout(c, y, title, lines, col=PINK):
    h = 34 + 13 * len(lines)
    c.setStrokeColorRGB(*col)
    c.setLineWidth(2)
    c.roundRect(M, y - h, W - 2 * M, h + 6, 9, stroke=1, fill=0)
    c.setFillColorRGB(*col)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 14, y - 16, title)
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 9.5)
    yy = y - 33
    for ln in lines:
        c.drawString(M + 14, yy, ln)
        yy -= 13
    return y - h - 18


def checkbox_list(c, y, items, gap=20):
    for q in items:
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(1)
        c.rect(M, y - 3, 11, 11, stroke=1, fill=0)
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 10)
        c.drawString(M + 20, y, q)
        y -= gap
    return y


def wrap(text, width_pt, size):
    """Greedy wrap using reportlab's real string widths, not a char estimate."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    out, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if stringWidth(trial, "Helvetica", size) <= width_pt:
            line = trial
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def rule_line(c, y, w=None):
    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(0.6)
    c.line(M, y, M + (w or (W - 2 * M)), y)
    return y - 14


# ---------------------------------------------------------------- layouts ---
def layout_box(c, x, y, s, blocks, title, note):
    """Draw one square page layout to proportion.

    `blocks` are (left, top, width, height) in 0-1 page fractions, where top is
    measured DOWN from the top edge — the same way you read a page. Text blocks
    are drawn as rule lines instead of a filled photo box.
    """
    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(1)
    c.rect(x, y - s, s, s, stroke=1, fill=0)
    for (bl, bt, bw, bh, kind) in blocks:
        bx = x + bl * s
        by = y - (bt + bh) * s
        if kind == 'text':
            c.setStrokeColorRGB(*GREY)
            c.setLineWidth(0.7)
            rows = max(2, int(bh * s / 7))
            for r in range(rows):
                ly = by + bh * s - (r + 1) * (bh * s / (rows + 1))
                c.line(bx, ly, bx + bw * s * (0.95 if r % 3 else 0.62), ly)
        else:
            c.setFillColorRGB(*(PHOTO if kind == 'photo' else (0.93, 0.90, 0.84)))
            c.rect(bx, by, bw * s, bh * s, stroke=0, fill=1)
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x, y - s - 16, title)
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 8.5)
    ny = y - s - 28
    for ln in wrap(note, s, 8.5)[:2]:
        c.drawString(x, ny, ln)
        ny -= 10.5


LAYOUTS = [
    ("1 · The hero",
     "One photo, off centre, running off two edges.",
     [(-0.02, 0.06, 0.72, 0.62, 'photo'), (0.08, 0.76, 0.60, 0.14, 'text')]),
    ("2 · Hero and three",
     "The video's spread. Three aligned supports.",
     [(0.06, 0.06, 0.58, 0.58, 'photo'),
      (0.70, 0.06, 0.24, 0.18, 'photo'), (0.70, 0.26, 0.24, 0.18, 'photo'),
      (0.70, 0.46, 0.24, 0.18, 'photo'), (0.06, 0.72, 0.58, 0.16, 'text')]),
    ("3 · Four up",
     "Equal weight. Identical gaps.",
     [(0.06, 0.08, 0.41, 0.34, 'photo'), (0.53, 0.08, 0.41, 0.34, 'photo'),
      (0.06, 0.46, 0.41, 0.34, 'photo'), (0.53, 0.46, 0.41, 0.34, 'photo'),
      (0.06, 0.84, 0.60, 0.09, 'text')]),
    ("4 · The writing page",
     "Mostly words. Every album needs these.",
     [(0.06, 0.06, 0.40, 0.28, 'photo'), (0.06, 0.40, 0.88, 0.50, 'text')]),
    ("5 · Full bleed",
     "Edge to edge. Needs bleed ticked.",
     [(-0.03, -0.03, 1.06, 1.06, 'photo'), (0.08, 0.80, 0.50, 0.10, 'text')]),
    ("6 · The breather",
     "One small photo, a lot of paper.",
     [(0.33, 0.34, 0.34, 0.30, 'photo'), (0.30, 0.70, 0.40, 0.07, 'text')]),
]


def pdf_layouts():
    c = pdfcanvas.Canvas(os.path.join(OUT, "scrapbook-layout-recipes.pdf"), pagesize=letter)
    y = page(c, "Six layouts that hold together", "scrapbook kit")
    y = body(c, y, [
        "These are the six pages in the template, drawn to proportion. The point is not that",
        "they are clever — it is that they are the SAME six, reused. Consistent geometry is",
        "what makes an album look made rather than assembled.",
        "",
        "Grey blocks are photos. Ruled blocks are journaling text.",
    ])
    y -= 6
    s = 2.05 * inch
    gap = 0.55 * inch
    col_x = [M, M + s + gap, M + 2 * (s + gap)]
    row = 0
    for i, (title, note, blocks) in enumerate(LAYOUTS):
        if i and i % 3 == 0:
            row += 1
        x = col_x[i % 3]
        yy = y - row * (s + 72)
        layout_box(c, x, yy, s, blocks, title, note)
    y = y - 2 * (s + 72) + 24
    y = callout(c, y, "The one rule that does the work", [
        "Select a group, then use Position > Align, then Position > Tidy up / spacing.",
        "Eyeballed gaps are the single biggest tell of a homemade page. The tools are",
        "faster than nudging anyway.",
    ], col=TEAL)
    y = heading(c, y, "Building your own from these")
    body(c, y, [
        "Delete the photos out of a page, keep the frames, the text box and the spacing,",
        "and duplicate it. That empty page is a layout. Six of them is a kit.",
    ])
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------------- photo prep ---
def pdf_photo_prep():
    c = pdfcanvas.Canvas(os.path.join(OUT, "scrapbook-photo-prep.pdf"), pagesize=letter)
    y = page(c, "Getting the photos in", "scrapbook kit")
    y = body(c, y, [
        "Do this before you open the template. An hour here saves three later, and two of",
        "these limits are the reason uploads fail silently.",
    ])
    y -= 4
    y = heading(c, y, "Canva's actual upload limits")
    y = body(c, y, [
        "Each image      under 50 MB, and no more than 250 million total pixels (w x h)",
        "Formats         JPEG, PNG, HEIC/HEIF, WebP  (WebP: static images only)",
        "Storage         Canva Free 5 GB · Canva Pro 100 GB",
        "Folder size     Canva Free 200 items · Pro / Teams / Education 1000 items",
        "PDF import      300 MB max, 500 pages max",
    ], size=10)
    y -= 4
    y = callout(c, y, "The one that actually bites", [
        "A 20-year family archive hits the 200-item folder cap on a free account long",
        "before it gets anywhere near 5 GB of storage. Split by year into several folders,",
        "or upgrade before you start rather than halfway through.",
    ])
    y = heading(c, y, "Asking other people for photos")
    y = body(c, y, [
        "Never accept photos sent through a messaging app. WhatsApp, Messenger and iMessage",
        "compress hard, and you will not find out until it is printed and soft.",
        "",
        "Send them this line instead:",
    ])
    y -= 2
    y = callout(c, y, "Copy and paste this", [
        "\"Could you put the original files in this shared folder rather than sending them",
        "to me in chat? Chat apps shrink photos and they come out blurry when printed.",
        "On iPhone: select, Share, Save to Files. On Android: select, Share, Drive.\"",
    ], col=AMBER)
    y = heading(c, y, "Scanning old prints")
    body(c, y, [
        "300 dpi is enough for a same-size reprint. 600 dpi if you intend to crop in hard or",
        "enlarge. Above that you are making a file that is slower to work with and no better",
        "on paper — and very large scans are the ones that trip the 50 MB limit.",
        "",
        "Scan in colour even for black-and-white prints: it captures the paper tone, and you",
        "can always desaturate later. You cannot put it back.",
    ])
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------------------- exporting --
def pdf_export():
    c = pdfcanvas.Canvas(os.path.join(OUT, "scrapbook-export-checklist.pdf"), pagesize=letter)
    y = page(c, "Before you send it anywhere", "scrapbook kit")
    y = body(c, y, [
        "Export is not one setting. It is a decision about where the file is going, and the",
        "wrong branch is expensive — either a soft print or a privacy problem.",
    ])
    y -= 4
    y = heading(c, y, "Where is it going?")
    y = body(c, y, [
        "A print shop or photo book service",
        "    PDF Print  ·  300 dpi  ·  bleed ON  ·  crop marks ON  ·  flatten ON",
        "    Ask them whether they want CMYK. If they do, pick it in the same dialog.",
        "",
        "A home printer",
        "    PDF Print  ·  300 dpi  ·  bleed OFF",
        "    A home printer cannot print to the edge. Bleed gives your reader a white",
        "    border and a cropped page.",
        "",
        "Family, on a screen",
        "    PDF Standard  ·  96 dpi  ·  flatten ON",
        "    Far smaller file. Nobody is printing it, so 300 dpi is wasted megabytes.",
    ], size=10, lead=14)
    y -= 2
    y = callout(c, y, "Flatten PDF — tick it, and know what it does", [
        "Canva: flattening \"converts your design with multiple layers into one\" and",
        "\"converts the file into a static image, preventing editing in software like",
        "Adobe Acrobat\".  That is what closes the crop hole (see below).",
        "Two costs: the file gets bigger, and accessibility tagging is removed — so if",
        "this document has to work with a screen reader, leave it unticked.",
    ])
    y = heading(c, y, "The crop hole, in Canva's own words")
    y = body(c, y, [
        "\"If you download a design containing cropped images to a PDF file, the PDF format",
        "will include the original image. This means someone could use a third-party tool",
        "(for example, a PDF editor) to get the full, uncropped image from your PDF export.\"",
        "",
        "In a scrapbook this is a privacy question, not a design one. Anyone you cropped out",
        "is still in the file you emailed. Flatten it, or rebuild those images.",
    ], size=10)
    y -= 4
    y = heading(c, y, "Last checks")
    checkbox_list(c, y, [
        "Same page size on every page",
        "Every crop flattened, or the image rebuilt",
        "Bleed matches the destination (shop ON / home OFF)",
        "Under 350 pages, or split into two designs",
        "Pages as separate files, if the printer asked (Pro only)",
        "The Canva design saved and named — it is the only editable copy",
    ])
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------------ print brief ---
def pdf_print_brief():
    c = pdfcanvas.Canvas(os.path.join(OUT, "scrapbook-print-brief.pdf"), pagesize=letter)
    y = page(c, "Print brief", "send this to the printer")
    y = body(c, y, [
        "Fill this in and send it with the file. Printers ask these questions anyway, and",
        "answering them up front is usually the difference between one proof and three.",
    ])
    y -= 6
    fields = [
        ("Project", "____________________________________________"),
        ("Finished page size", "12 x 12 in   /   8.5 x 11 in   /   A4   /   other: __________"),
        ("Number of pages", "__________   (must be even for most binding)"),
        ("Single or double sided", "single  /  double"),
        ("Binding", "wire-o  /  perfect bound  /  layflat  /  loose in sleeves  /  none"),
        ("Paper weight", "__________ gsm    (170-250 gsm suits photo pages)"),
        ("Finish", "matt  /  satin  /  gloss"),
        ("Colour", "RGB  /  CMYK  (tell me which and I will re-export)"),
        ("Bleed", "3 mm supplied  /  none needed"),
        ("File supplied as", "one multi-page PDF  /  one PDF per page (zip)"),
        ("Proof required", "yes, before the full run  /  no"),
        ("Deadline", "____________________________________________"),
    ]
    c.setFont("Helvetica", 10)
    for label, val in fields:
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(M, y, label)
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 9.5)
        c.drawString(M + 2.0 * inch, y, val)
        y -= 12
        c.setStrokeColorRGB(0.88, 0.88, 0.86)
        c.setLineWidth(0.5)
        c.line(M, y + 3, W - M, y + 3)
        y -= 10
    y -= 6
    y = callout(c, y, "If they come back and say it looks blurry", [
        "Canva's own three fixes, in order: download as a flattened PDF; check the filename",
        "has no full stops or special characters; and double the dimensions of the design",
        "for a bigger, clearer print. Then ask for a printed proof before the full run.",
    ], col=AMBER)
    y = heading(c, y, "A note on page count")
    body(c, y, [
        "A Canva design holds up to 350 pages. Past that, Canva's own advice is to build a",
        "second design and merge the two downloads with any file merger — so keep the page",
        "size identical between them, and number your pages before you split.",
    ])
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------------- journaling ---
PROMPTS = [
    ("The ordinary day", [
        "What did a normal Tuesday look like this year?",
        "What was for dinner most weeks?",
        "What did the house sound like at seven in the morning?",
        "Which song was on constantly, whether anyone liked it or not?",
    ]),
    ("The people", [
        "Who is in this photo that you have not spoken to since?",
        "Who took this picture? They are never in the album.",
        "What was the running joke that year?",
        "Who would you have expected to be here, and why aren't they?",
    ]),
    ("The moment itself", [
        "What happened in the ten minutes before this was taken?",
        "What is just outside the frame?",
        "Was anyone in a mood? Say so. It ages well.",
        "What did it smell like?",
    ]),
    ("The honest one", [
        "What was hard about this year that the photos do not show?",
        "What were you worried about that turned out fine?",
        "What did you get wrong?",
        "What would you tell yourself in this picture?",
    ]),
    ("For a child's album", [
        "What were they obsessed with this month?",
        "The word they said wrong, and how they said it.",
        "What they were frightened of, and what fixed it.",
        "Something they said that you wrote down so you would not forget.",
    ]),
    ("Closing a book", [
        "What changed between the first page and this one?",
        "What do you want whoever opens this in thirty years to know?",
        "Who is this actually for?",
    ]),
]


def pdf_prompts():
    c = pdfcanvas.Canvas(os.path.join(OUT, "scrapbook-journaling-prompts.pdf"), pagesize=letter)
    y = page(c, "What to write in the box", "scrapbook kit")
    y = body(c, y, [
        "The text box is where most scrapbooks give up and write the date. The date is",
        "already in the photo's file. Write the thing the photo cannot show.",
        "",
        "One or two sentences is plenty. You are not writing an essay, you are leaving a note.",
    ])
    y -= 8
    for title, qs in PROMPTS:
        if y < 130:
            footer(c)
            c.showPage()
            y = page(c, "What to write in the box", "continued")
        y = heading(c, y, title, size=11.5)
        for q in qs:
            c.setFillColorRGB(*TEAL)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(M + 2, y, "—")
            c.setFillColorRGB(*BODY)
            c.setFont("Helvetica", 10)
            c.drawString(M + 16, y, q)
            y -= 14
        y -= 8
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------------- read me ---
def pdf_readme():
    c = pdfcanvas.Canvas(os.path.join(OUT, "scrapbook-READ-ME.pdf"), pagesize=letter)
    y = page(c, "Read me first", "scrapbook + photo book kit")
    y = body(c, y, [
        "Thank you. Here is what is in the kit and the order to use it in.",
    ])
    y -= 4
    y = heading(c, y, "What you have")
    y = body(c, y, [
        "The Canva template     12 x 12 in for print, plus a letter-size home version.",
        "                       A cover, six layout pages, and a journaling page.",
        "layout-recipes.pdf     the six layouts drawn to proportion",
        "photo-prep.pdf         upload limits, scanning, and how to ask for originals",
        "export-checklist.pdf   which export settings, for which destination",
        "print-brief.pdf        fill in and send to your printer",
        "journaling-prompts.pdf what to write when the box is empty",
    ], size=10, lead=14)
    y -= 4
    y = heading(c, y, "The order")
    y = body(c, y, [
        "1.  Decide the page size FIRST. It cannot be changed sensibly later, and an",
        "    exported PDF cannot be brought back into Canva as an editable design.",
        "2.  Collect and upload the photos into one folder. Check the limits sheet.",
        "3.  Open the template, and pour photos into the layouts. Do not redesign each page.",
        "4.  Write one or two lines per spread. Prompts sheet if you are stuck.",
        "5.  Export using the checklist. Tick Flatten PDF.",
    ], size=10, lead=14)
    y -= 4
    y = callout(c, y, "The one thing people regret", [
        "Cropping is hiding, not deleting. An unflattened PDF still contains the whole",
        "original of every photo you cropped — Canva documents this. In a family album",
        "that is a privacy issue. Tick Flatten PDF before you send it to anyone.",
    ])
    y = heading(c, y, "Sources, so you can check them")
    y = body(c, y, [
        "All limits and quotes above are from Canva's Help Centre, checked 19 August 2026:",
        "  · \"Check file upload formats and requirements for Canva\"  (upload + import limits)",
        "  · \"Add, duplicate, and delete pages\"  (350 pages, and the merge workaround)",
        "  · \"Choose the right download file type for your Canva design\"  (dpi, the crop note)",
        "  · \"Download designs as flattened PDF\"  (what flattening does, and its costs)",
        "  · \"Can't use design at an online print shop\"  (the blurry-print fixes)",
        "Canva changes things. If a number here no longer matches, believe Canva.",
    ], size=9.5, lead=13)
    y -= 2
    y = heading(c, y, "Licence")
    body(c, y, [
        "Use it for your own albums, and for albums you are paid to make, printed or digital.",
        "The template and these PDFs are not for resale or redistribution as templates.",
    ], size=10)
    footer(c)
    c.showPage()
    c.save()


if __name__ == "__main__":
    pdf_layouts()
    pdf_photo_prep()
    pdf_export()
    pdf_print_brief()
    pdf_prompts()
    pdf_readme()
    print("wrote 6 PDFs")
