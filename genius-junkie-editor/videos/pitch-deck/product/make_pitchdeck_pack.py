#!/usr/bin/env python3
"""Pitch Deck Kit — the reference set that ships with the editable Canva deck.

Outputs (all US Letter):
  pitchdeck-ten-slides.pdf         what goes on each slide, and what it must answer
  pitchdeck-traction-worksheet.pdf get the numbers straight before designing
  pitchdeck-send-checklist.pdf     the pre-send checks, incl. the two file traps
  pitchdeck-email-scripts.pdf      cold intro, warm intro, the one follow-up
  pitchdeck-READ-ME.pdf            how to use the template, and the licence
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


def rule(c, y, x0=None, x1=None):
    c.setStrokeColorRGB(0.80, 0.82, 0.81)
    c.setLineWidth(0.8)
    c.line(x0 or M, y, x1 or (W - M), y)


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


# ------------------------------------------------------- ten slides ---------
SLIDES = [
    ("1  Title", "Who you are, in plain words.",
     "Company name, and one line saying what you do. No adjectives."),
    ("2  Problem", "Does this problem exist, and is it painful?",
     "A headline that is a SENTENCE, not a topic. Three lines of evidence under it."),
    ("3  Solution", "What is the thing?",
     "Same shape. Then show it — a screenshot, a photo, a diagram. Not a paragraph."),
    ("4  How it works", "Do I believe you can build it?",
     "Three steps maximum. If it needs four, the slide is describing the product tour."),
    ("5  Market", "Is this big enough to matter?",
     "Who exactly, how many, and where the number came from. Cite it."),
    ("6  Business model", "How does money reach you?",
     "Who pays, how much, how often. One sentence beats a pricing table here."),
    ("7  Traction", "Does anybody actually want it?",
     "THE slide they read. One chart, labelled axis, date range. Numbers, not adjectives."),
    ("8  Competition", "Why does this not already exist?",
     "Name the real alternatives, including 'they do nothing'. Never say you have none."),
    ("9  Team", "Why you?",
     "The specific reason each person is the one to do this. Not job titles."),
    ("10 The ask", "What do you want?",
     "How much, and what it buys — the milestone it gets you to, and by when."),
]


def ten_slides(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "The ten slides", "pitch deck kit")
    y = body(c, y, [
        "Ten slides, in this order. The order is not arbitrary: problem before solution,",
        "because a solution to a problem nobody stated sounds like a hobby. Traction before",
        "competition, because once they believe somebody wants this, the competition slide",
        "reads as reassurance instead of as a warning.",
    ], size=10, lead=14)
    y -= 16

    for name, question, note in SLIDES:
        c.setFillColorRGB(*PINK)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(M, y, name)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(M + 110, y, question)
        y -= 14
        y = body(c, y, [note], size=9.3, lead=12, indent=110)
        y -= 7

    y = callout(c, y, "If you cannot fill a slide", [
        "That is not a design problem. It is something to go and find out. An empty",
        "traction slide is information — it says talk to more customers before you raise.",
    ])
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------------- traction --------
def traction_worksheet(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "The traction slide", "pitch deck kit")
    y = body(c, y, [
        "Slide seven is the one they actually read. Get the numbers straight here before",
        "you design anything — the slide is easy once the numbers are honest.",
    ])
    y -= 18

    # two blocks, not three — three pushed the closing section past the footer
    for i in range(1, 3):
        y = heading(c, y, f"Metric {i}")
        for lab, w in [("the number", 300), ("the window it covers", 300),
                       ("where it came from", 460), ("the honest version, if it is small", 460)]:
            c.setFillColorRGB(*TEAL)
            c.setFont("Helvetica-Bold", 8.5)
            c.drawString(M + 8, y, lab.upper())
            y -= 13
            rule(c, y, M + 8, M + 8 + w)
            y -= 19
        y -= 6

    y = callout(c, y, "Three rules for the chart", [
        "One chart, not three. Line for change over time, bar for comparing things.",
        "Delete the chart's own title — your slide headline already said it, and two",
        "titles on one slide is the fastest way to look amateur.",
        "Label the axis and put the date range on it. A line going up with no dates is",
        "not evidence, it is decoration — and it reads as something you are hiding.",
    ])

    y = heading(c, y, "Honest and small beats vague and impressive")
    body(c, y, [
        "\"Forty-one paying customers, up from twelve in March\" is a better slide than",
        "\"strong growth\", even though the number is small. Vague is what an investor sees",
        "forty times a week, so vague is what they have learned to discount.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# -------------------------------------------------------- checklist --------
def send_checklist(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Before you send it", "pitch deck kit")
    y = body(c, y, [
        "A pitch deck is a file that gets forwarded, not a presentation you give. These",
        "are the checks that matter once it leaves your hands.",
    ])
    y -= 16

    y = heading(c, y, "The deck")
    y = checkbox_list(c, y, [
        "Ten slides, one idea each.",
        "Every headline is a sentence, not a topic.",
        "Nothing under 18 point anywhere in the deck.",
        "The traction chart has a labelled axis and a date range.",
        "Margins identical on every slide (duplicate slides, never start from blank).",
    ])
    y -= 6

    y = heading(c, y, "The file")
    y = checkbox_list(c, y, [
        "Flatten PDF is TICKED.",
        "Include notes is UNTICKED.",
        "PDF Standard (96 dpi) for email — Print (300 dpi) is for paper.",
        "Under 10 MB. Flattening makes files bigger, so check after ticking it.",
        "Filename is your company name and the month. Not \"deck final v3\".",
        "A system font, if there is any chance they ask for an editable copy.",
    ])
    y -= 8

    y = callout(c, y, "The two things your file carries", [
        "1.  CROPPED IMAGES.  Canva's own docs: a PDF export \"will include the original",
        "     image\", so anyone can pull the full uncropped picture back out with a PDF",
        "     editor. Crop is a mask, not a delete. Flatten PDF is what makes it a delete.",
        "2.  YOUR NOTES.  The Include-notes checkbox exists so you can print your own cue",
        "     cards. Tick it by accident and you email an investor every private note you",
        "     wrote to yourself.",
    ])

    y = heading(c, y, "And if they ask for PowerPoint")
    body(c, y, [
        "Canva's own warning: PPTX files \"may look different when opened in Microsoft",
        "PowerPoint\" and you may need to install the fonts you used. Animations and",
        "embedded videos are not supported at all. Send a PDF by default; only send PPTX",
        "when they have said they want to edit it — and tell them which font you used.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------- emails ---------
def email_scripts(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "The three emails", "pitch deck kit")
    y = body(c, y, [
        "Short, specific, and the deck attached rather than linked. A link can be revoked",
        "and can ask them to sign in — and the forward is the whole point.",
    ])
    y -= 12

    blocks = [
        ("EMAIL 1 — COLD INTRO", [
            "Subject:  <company> — <the one-line what you do>",
            "",
            "<Name> — we make <what> for <who>.",
            "",
            "<The single most surprising true number you have.>",
            "",
            "Deck attached. Raising <amount> to <the milestone it buys>.",
            "Happy to answer anything by email if that is easier than a call.",
        ], PINK),
        ("EMAIL 2 — WARM INTRO, REPLYING TO THE INTRODUCER", [
            "Subject:  Re: intro — <company>",
            "",
            "Thanks <introducer>, moving you to bcc.",
            "",
            "<Name> — <one line on what we do>. <The number.>",
            "Deck attached. Raising <amount> to <milestone>.",
            "",
            "Keep it to four lines. The introduction did the persuading.",
        ], TEAL),
        ("EMAIL 3 — ONE FOLLOW-UP, THEN STOP", [
            "Subject:  Re: <original subject>",
            "",
            "Bumping this once — since I sent it, <the one new thing>.",
            "",
            "No problem at all if it is not a fit or the timing is wrong.",
            "",
            "One follow-up. Then move on to the next name on the list.",
        ], AMBER),
    ]
    for title, lines, col in blocks:
        c.setFillColorRGB(*col)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(M, y, title)
        y -= 8
        c.setStrokeColorRGB(*col)
        c.setLineWidth(1.4)
        c.line(M, y, W - M, y)
        y -= 17
        c.setFont("Courier", 9.3)
        c.setFillColorRGB(0.20, 0.22, 0.23)
        for ln in lines:
            c.drawString(M + 8, y, ln)
            y -= 13
        y -= 16

    y = heading(c, y, "The rule for all three")
    body(c, y, [
        "Attach the PDF. Do not make them click a link, sign in, or request access — every",
        "one of those is a reason to close the tab, and none of them make you look careful.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------------- read me ---------
def readme(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Read me first", "pitch deck kit")

    blocks = [
        ("What's in this kit", [
            "The editable Canva deck — ten slides at 1920 × 1080, with the type sizes",
            "   and margins already set so the deck cannot drift",
            "The four reference PDFs (the ten slides, the traction worksheet, the send",
            "   checklist, the three emails)",
        ]),
        ("How to use the template", [
            "Open the template link — it copies into your own Canva account.",
            "Replace the words slide by slide. To add a slide, DUPLICATE an existing",
            "   one and swap the text — never start from a blank page, or the type",
            "   sizes and margins drift and the deck stops looking like one deck.",
            "The traction slide has a chart with a labelled axis and a date range",
            "   already in place. Keep both when you swap your data in.",
        ]),
        ("The font decision, which is hard to undo", [
            "The deck ships in a system font on purpose. A PPTX export does not carry",
            "   your font with it — Canva's own docs say the file \"may look different\"",
            "   and that you may need to install the fonts you used.",
            "If you change to a decorative font and an investor later asks for an",
            "   editable copy, their version substitutes it and the layout collapses.",
        ]),
        ("The two things your exported file carries", [
            "Cropped images. Canva: a PDF export \"will include the original image\", so",
            "   a cropped-out revenue figure can be recovered with a PDF editor. Crop is",
            "   a mask, not a delete.",
            "Your speaker notes, if the Include-notes checkbox is ticked.",
            "Both are solved by ticking Flatten PDF on download — it converts the file",
            "   to a static image, which also locks your fonts and stops anyone editing",
            "   the deck in Acrobat. It makes the file bigger. Tick it anyway.",
        ]),
        ("Licence", [
            "Use this kit for your own company and your own fundraising, including",
            "   client work.",
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
        ("pitchdeck-ten-slides.pdf", ten_slides),
        ("pitchdeck-traction-worksheet.pdf", traction_worksheet),
        ("pitchdeck-send-checklist.pdf", send_checklist),
        ("pitchdeck-email-scripts.pdf", email_scripts),
        ("pitchdeck-READ-ME.pdf", readme),
    ]
    for name, fn in made:
        fn(os.path.join(OUT, name))
    print(f"wrote {len(made)} PDFs")
