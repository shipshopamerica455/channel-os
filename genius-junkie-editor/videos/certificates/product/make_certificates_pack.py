#!/usr/bin/env python3
"""Certificate + Bulk Create Kit — the reference set that ships with the
editable Canva certificate.

Outputs (all US Letter):
  certificates-data-sheet.pdf         the column headings, and the real limits
  certificates-placeholder-guide.pdf  building elements Bulk Create can connect
  certificates-bulk-checklist.pdf     the pre-generate checks, incl. Advanced options
  certificates-wording-bank.pdf       award lines and reason lines you can lift
  certificates-READ-ME.pdf            how to use the template, and the licence
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


# ------------------------------------------------------- data sheet --------
def data_sheet(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "The data sheet", "certificate + bulk create kit")
    y = body(c, y, [
        "Each COLUMN is one field. Each ROW is one finished certificate. That is the whole",
        "feature. Get the headings right and the rest takes ten minutes.",
    ])
    y -= 18

    y = heading(c, y, "Use these headings")
    cols = [
        ("Name", "Priya Raghunathan", "goes in the big centred box"),
        ("Course", "Level 2 First Aid", "the reason, one line"),
        ("Date", "18 August 2026", "write it out — 18/08/26 reads as US or UK"),
        ("Signature", "Mrs A. Okafor", "optional, if it changes per row"),
    ]
    c.setFillColorRGB(*TEAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M + 8, y, "HEADING")
    c.drawString(M + 130, y, "EXAMPLE")
    c.drawString(M + 330, y, "NOTE")
    y -= 16
    for h, ex, note in cols:
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M + 8, y, h)
        c.setFillColorRGB(0.28, 0.30, 0.31)
        c.setFont("Helvetica", 10)
        c.drawString(M + 130, y, ex)
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(M + 330, y, note)
        y -= 20
    y -= 10

    y = callout(c, y, "Headings become the field names you drag", [
        "\"First name\" is far easier to work with than \"Column D\". Clean them before you",
        "upload, because you cannot rename a field once you are in the connect step —",
        "you have to go back out, fix the sheet, and upload again.",
    ], col=TEAL)

    y = heading(c, y, "The limits that actually exist")
    for what, limit in [
        ("Data fields (columns) you can connect", "150"),
        ("Rows you can select from a Canva Sheet", "300"),
        ("Text boxes per field", "exactly 1"),
    ]:
        c.setFillColorRGB(0.28, 0.30, 0.31)
        c.setFont("Helvetica", 10)
        c.drawString(M + 8, y, what)
        c.setFillColorRGB(*AMBER)
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(W - M - 8, y, limit)
        y -= 19
    y -= 8
    y = body(c, y, [
        "A whole school in one run will hit the 300-row ceiling. Split it by year group,",
        "which is usually how you wanted to hand them out anyway.",
    ], size=10, lead=14)
    y -= 12

    y = callout(c, y, "If you type the data straight into Canva", [
        "Click CLEAR TABLE first. Bulk Create opens with sample data already in it, and if",
        "you leave it there you will generate certificates for people who do not exist.",
    ])

    y = heading(c, y, "Images (crests, headshots, badges)")
    body(c, y, [
        "Add a frame or a grid to the template as the placeholder, then EMBED the picture",
        "inside a single cell of your sheet. Canva's docs: image URLs from cloud photo",
        "storage \"are not supported and will be treated as plain text\" — so a Drive link",
        "prints the words http://... across your certificate instead of the photo.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------- placeholder guide -----
def placeholder_guide(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Building placeholders", "certificate + bulk create kit")
    y = body(c, y, [
        "Bulk Create connects one data field to one element. Everything that changes",
        "between certificates therefore has to be its own separate text box. This is the",
        "step people skip, and it is the reason their first run comes out wrong.",
    ])
    y -= 18

    y = callout(c, y, "The mistake", [
        "One text box containing:   Awarded to ______________",
        "",
        "You cannot connect just the blank half — Canva has no way to reach inside a text",
        "box. Connecting the field replaces the WHOLE line, so every certificate loses the",
        "words \"Awarded to\" as well.",
    ])

    y = heading(c, y, "The fix")
    y = body(c, y, [
        "Box 1:   Awarded to            ← fixed text, never connected",
        "Box 2:   NAME                  ← its own box, connected to the Name field",
        "Box 3:   for                   ← fixed",
        "Box 4:   COURSE                ← its own box, connected to Course",
        "Box 5:   DATE                  ← its own box, connected to Date",
    ], size=10.5, lead=16)
    y -= 12

    y = heading(c, y, "Type the placeholder in CAPITALS")
    y = body(c, y, [
        "NAME, COURSE, DATE. You are going to be looking for these in a list of elements",
        "in a minute, and \"NAME\" is findable in a way that \"Your name here\" is not.",
        "It also makes auto-match far more likely to get it right first time.",
    ], size=10, lead=14)
    y -= 12

    y = callout(c, y, "The one setting that saves you fixing fifty by hand", [
        "Set the NAME box to CENTRED, and to a FIXED WIDTH rather than one that grows.",
        "",
        "Your list has names of four letters and names of twenty-five. A box that grows",
        "from the left leaves the short ones sitting off to one side and pushes the long",
        "ones off the edge. Centred and fixed width, and both sit correctly.",
    ], col=TEAL)

    y = heading(c, y, "Style everything BEFORE you connect")
    body(c, y, [
        "Font, size, colour and alignment are inherited by all fifty. Changing your mind",
        "afterwards means re-running the whole thing. Set the name at roughly 80–100pt:",
        "a certificate is read from arm's length on a wall, not on a screen.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------------- checklist -------
def bulk_checklist(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Before you press Create", "certificate + bulk create kit")
    y = body(c, y, [
        "Fourteen checks. The last three are the ones that turn a fifty-page file into",
        "fifty finished certificates with the right names on them.",
    ])
    y -= 16

    y = heading(c, y, "The template")
    y = checkbox_list(c, y, [
        "Every changing field is its own separate text box.",
        "Placeholders typed in CAPITALS so you can find them.",
        "The name box is centred and fixed width.",
        "Font, size and colour are final — all fifty inherit them.",
        "If the template has more than one page, connections set on EVERY page.",
    ])
    y -= 6

    y = heading(c, y, "The data")
    y = checkbox_list(c, y, [
        "Column headings are clean — they become the field names.",
        "Sample data cleared from the table.",
        "Dates written out in full (18 August 2026), not 18/08/26.",
        "Under 300 rows in this run.",
        "Any images embedded IN the cell, not linked from a cloud drive.",
    ])
    y -= 6

    y = heading(c, y, "The connect step")
    y = checkbox_list(c, y, [
        "Connections read by eye — auto-match can put the date in the course box.",
        "Previewed. (The preview is review-only; fix problems back in the data step.)",
    ])
    y -= 8

    y = callout(c, y, "ADVANCED OPTIONS — below the Continue button", [
        "This is the part almost nobody opens, and it is the whole reason to bother.",
        "",
        "  Output              →  INDIVIDUAL DESIGNS  (not \"1 design with multiple pages\")",
        "  Name each page using →  your Name column",
        "  Save in             →  a folder you made for this run",
        "",
        "Set those three and you get fifty separate files, each named after the person it",
        "belongs to, sitting in one folder. Miss them and you get one fifty-page design",
        "and an hour of renaming.",
    ])
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------- wording bank ------
BANK = [
    ("School and classroom", [
        "Awarded for outstanding effort in",
        "In recognition of consistent progress in",
        "For showing real kindness to others this term",
        "For reading every single day this half term",
        "Most improved in",
    ]),
    ("Sports and clubs", [
        "Awarded for commitment and attendance throughout the season",
        "Player of the season",
        "For sportsmanship shown on and off the pitch",
        "In recognition of completing the",
    ]),
    ("Training and courses", [
        "This is to certify that the above named has successfully completed",
        "Awarded on successful completion of",
        "In recognition of attendance and participation in",
        "Has demonstrated competence in",
    ]),
    ("Workplace", [
        "In recognition of outstanding contribution to",
        "For going above and beyond in",
        "Awarded in appreciation of five years of service",
        "Employee of the month",
    ]),
]


def wording_bank(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "What to actually write", "certificate + bulk create kit")
    y = body(c, y, [
        "The award line is fixed text — it never connects to your data, so you write it",
        "once. These are lines you can lift. Keep the reason to ONE line: it sits under a",
        "very large name and competing with it makes both harder to read.",
    ])
    y -= 18

    for title, lines in BANK:
        y = heading(c, y, title)
        for ln in lines:
            c.setFillColorRGB(*PINK)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(M + 8, y, "·")
            c.setFillColorRGB(0.28, 0.30, 0.31)
            c.setFont("Helvetica", 10.5)
            c.drawString(M + 22, y, ln)
            y -= 17
        y -= 10

    y = callout(c, y, "Two words to avoid on a certificate", [
        "\"Participation\" and \"Attendance\", unless that genuinely is the award. Both read",
        "as a consolation prize to the person holding it — and a certificate is kept for",
        "years, on a wall, by someone who will read it more carefully than you wrote it.",
    ])
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------------- read me ---------
def readme(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Read me first", "certificate + bulk create kit")

    blocks = [
        ("Before anything else — can you use Bulk Create?", [
            "Bulk Create is a Canva PRO feature, and it is DESKTOP ONLY. It will not",
            "   appear on your phone at all.",
            "But Canva for Education is free for verified K-12 teachers and includes",
            "   the Pro feature set, so Bulk Create is included. Verify with a school",
            "   email at canva.com/education — it usually takes a day or two.",
            "Without Pro or Education, the template still works perfectly; you just",
            "   fill the names in by hand.",
        ]),
        ("What's in this kit", [
            "The editable Canva certificate — A4 landscape, with the placeholder text",
            "   boxes already separated, styled, centred and fixed width",
            "The four reference PDFs (data sheet, placeholder guide, bulk checklist,",
            "   wording bank)",
        ]),
        ("How to use the template", [
            "Open the template link — it copies into your own Canva account.",
            "Write the award line and the reason (they never change, so they are not",
            "   connected to anything).",
            "Leave NAME, COURSE and DATE exactly as they are — those are the",
            "   placeholders Bulk Create connects to. Restyle them if you like, but",
            "   keep them as separate boxes and keep NAME centred and fixed width.",
            "Then Edit → Bulk create, or Apps → Bulk create.",
        ]),
        ("The setting that makes this worth doing", [
            "At the connect step there is a Continue button, and BELOW it, in small",
            "   text, Advanced options. Open it.",
            "Output → Individual designs (the default is one design with many pages).",
            "Name each page using → your Name column.",
            "That gives you one folder holding fifty separate files, each named after",
            "   the person on it. The default gives you one long file and an hour of",
            "   renaming.",
        ]),
        ("Licence", [
            "Use this kit for your own certificates, in your school, club or business,",
            "   including ones you are paid to produce.",
            "You may not resell, share or redistribute the template or these PDFs",
            "   themselves, and you may not sell the kit as your own.",
        ]),
    ]
    for title, lines in blocks:
        y = heading(c, y, title)
        y = body(c, y, ["• " + ln if not ln.startswith("   ") else ln for ln in lines], size=9.5, lead=13)
        y -= 9

    footer(c)
    c.showPage()
    c.save()


if __name__ == "__main__":
    made = [
        ("certificates-data-sheet.pdf", data_sheet),
        ("certificates-placeholder-guide.pdf", placeholder_guide),
        ("certificates-bulk-checklist.pdf", bulk_checklist),
        ("certificates-wording-bank.pdf", wording_bank),
        ("certificates-READ-ME.pdf", readme),
    ]
    for name, fn in made:
        fn(os.path.join(OUT, name))
    print(f"wrote {len(made)} PDFs")
