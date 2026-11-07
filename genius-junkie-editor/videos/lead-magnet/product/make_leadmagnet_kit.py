#!/usr/bin/env python3
"""Lead Magnet Kit — the fill-in set that ships with the editable Canva template.

Outputs (all US Letter, the same size as the magnet itself):
  leadmagnet-promise-worksheet.pdf   narrow the promise down to one sentence
  leadmagnet-email-scripts.pdf       the delivery email + all three follow-ups
  leadmagnet-form-wording.pdf        the form, the button, the thank-you page
  leadmagnet-launch-checklist.pdf    the six checks, printable and tickable
  leadmagnet-READ-ME.pdf             how to use the template, and the licence
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

PAPER = (0.984, 0.980, 0.973)   # #fbfaf8
INK = (0.078, 0.094, 0.114)     # #14181d
TEAL = (0.184, 0.490, 0.471)    # #2f7d78
AMBER = (0.851, 0.604, 0.169)   # #d99a2b
GREY = (0.659, 0.690, 0.682)    # #a8b0ae
PINK = (0.914, 0.118, 0.549)    # Genius Junkie pink
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


def fill_line(c, y, label, n=1, gap=22):
    """A labelled fill-in line (or n of them)."""
    c.setFillColorRGB(*TEAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M, y, label.upper())
    y -= 14
    for _ in range(n):
        rule(c, y)
        y -= gap
    return y - 6


# --------------------------------------------------------- promise ----------
def promise_worksheet(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Narrow the promise", "lead magnet kit")
    y = body(c, y, [
        "The narrower it is, the better it converts — and this is counter-intuitive enough",
        "that most people get it backwards. They widen the promise to appeal to more",
        "people, and it stops appealing to anybody. Work down the page.",
    ])
    y -= 14

    y = heading(c, y, "1. Who, exactly")
    y = body(c, y, ['Not "small business owners". A bakery owner. A newly qualified PT.'], size=9.5, lead=13)
    y = fill_line(c, y - 4, "one specific person", 1)

    y = heading(c, y, "2. What they are stuck on this week")
    y = fill_line(c, y, "the one problem", 2)

    y = heading(c, y, "3. The promise, in one sentence")
    y = body(c, y, ['Start it with "the" and a number if you can — "the 30 captions I rotate for a bakery".'], size=9.5, lead=13)
    y = fill_line(c, y - 4, "one sentence", 2)

    y = heading(c, y, "4. Sanity checks")
    for q in [
        "Could they finish it in under five minutes?",
        "Would they recognise themselves in the first line?",
        "Is it one thing, not a survey of everything?",
        "Does the title say what they get, not what it is about?",
    ]:
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(1)
        c.rect(M, y - 3, 11, 11, stroke=1, fill=0)
        c.setFillColorRGB(0.28, 0.30, 0.31)
        c.setFont("Helvetica", 10)
        c.drawString(M + 20, y, q)
        y -= 20

    y -= 8
    c.setStrokeColorRGB(*PINK)
    c.setLineWidth(2)
    c.roundRect(M, y - 44, W - 2 * M, 50, 9, stroke=1, fill=0)
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 14, y - 16, "One to five pages. Not thirty.")
    c.setFillColorRGB(0.28, 0.30, 0.31)
    c.setFont("Helvetica", 9.5)
    c.drawString(M + 14, y - 32, "A thing that gets finished builds trust. A thirty-page ebook gets downloaded and never opened.")
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------- emails ----------
def email_scripts(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "The four emails", "lead magnet kit")
    y = body(c, y, [
        "Written once. Sent automatically. Fill in the blanks and paste them into",
        "whatever sends your email.",
    ])
    y -= 12

    blocks = [
        ("EMAIL 1 — THE DELIVERY (immediately)", [
            "Subject:  <the name of the thing they asked for>",
            "",
            "Here it is —",
            "[ BUTTON: Open the <thing> ]",
            "",
            "Open page <n> and do the first item.",
            "",
            "⚠ Link to a hosted file. Never attach it.",
        ], PINK),
        ("EMAIL 2 — DID YOU USE IT (day 1–2)", [
            "Subject:  the bit people get stuck on",
            "",
            "Quick one — did you get a chance to try <the thing>?",
            "The place most people stall is <the sticking point>.",
            "The fix: <one or two sentences>.",
            "",
            "Reply and tell me how you got on — I read them all.",
        ], TEAL),
        ("EMAIL 3 — THE OFFER (a few days later)", [
            "Subject:  <the outcome they want>",
            "",
            "If <the thing> was useful, the next step is <your offer>.",
            "It's for <who>, it does <what>, it costs <how much>.",
            "[ BUTTON: <the one action> ]",
            "",
            "You've given two useful things first — this is allowed to be an offer.",
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
        y -= 18
        c.setFont("Courier", 9.5)
        c.setFillColorRGB(0.20, 0.22, 0.23)
        for ln in lines:
            c.drawString(M + 8, y, ln)
            y -= 13.5
        y -= 16

    y = heading(c, y, "The rule for all three")
    body(c, y, [
        "Almost empty. No life story, no seven other links, no social icons. Every extra",
        "thing is another chance to click something that isn't the file.",
    ], size=10)
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------------ form ----------
def form_wording(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "The form and the page after", "lead magnet kit")

    y = heading(c, y, "The form — three rules")
    y = body(c, y, [
        "1.  Ask for the email and nothing else. Every extra field costs you sign-ups,",
        "     and you do not need their phone number for a PDF.",
        "2.  Put the promise directly above the field, in the same words as the cover.",
        "3.  Label the button with what they get.",
    ], size=10, lead=14)
    y -= 10

    y = fill_line(c, y, "the promise line (same as the cover)", 1)
    y = fill_line(c, y, "the button says", 1)
    y = body(c, y, ['Good: "Send me the templates."   ·   Bad: "Submit."'], size=9.5, lead=13, col=(0.45, 0.47, 0.46))
    y -= 14

    y = heading(c, y, "Where the addresses go")
    y = body(c, y, [
        "Canva can capture an email now — drop a form into a design, share it by public",
        "link, and the addresses land in a Canva Sheet. Free, five minutes, genuinely",
        "fine for your first fifty.",
        "",
        "But a Sheet is a list of addresses, not an email list. It doesn't send the file",
        "and it doesn't follow anybody up. Nothing happens until you connect something",
        "that sends.",
    ], size=10, lead=14)
    y -= 12

    y = heading(c, y, "The thank-you page — three jobs, not one")
    y = body(c, y, [
        "1.  Reassure: it's on its way, check the Promotions tab.",
        "2.  The same single next step that's on the last page of the magnet.",
        "3.  Something that makes the wait feel short — a two-minute video, a quick win.",
        "",
        "This is the highest-intent moment you will ever get with this person. They have",
        "just raised their hand. A page that says \"thanks\" and nothing else throws it away.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------- checklist ----------
def launch_checklist(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Before you turn it on", "lead magnet kit")

    checks = [
        ("The promise is one sentence and one person", "not \"my free guide to social media\""),
        ("It can be finished in under five minutes", "one to five pages"),
        ("The last page has exactly one next step", "one button, one link, one sentence"),
        ("Exported PDF Standard, and small", "Print is for paper and several times the size"),
        ("The file is hosted and the email links to it", "NEVER attached — this is the expensive one"),
        ("Sign up to your own form, on a phone, all the way through",
         "did it arrive? did it land in promotions? did the button work?"),
    ]
    y -= 4
    for i, (t, sub) in enumerate(checks, 1):
        hot = i in (5, 6)
        c.setStrokeColorRGB(*(PINK if hot else (0.45, 0.47, 0.46)))
        c.setLineWidth(1.4 if hot else 1.1)
        c.rect(M, y - 10, 16, 16, stroke=1, fill=0)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString(M + 28, y, f"{i}. {t}")
        c.setFillColorRGB(*(PINK if hot else (0.45, 0.47, 0.46)))
        c.setFont("Helvetica", 9.5)
        c.drawString(M + 28, y - 15, sub)
        y -= 46

    y -= 4
    c.setStrokeColorRGB(*PINK)
    c.setLineWidth(2)
    c.roundRect(M, y - 56, W - 2 * M, 62, 10, stroke=1, fill=0)
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 12.5)
    c.drawString(M + 16, y - 20, "The one that kills lead magnets silently")
    c.setFillColorRGB(0.28, 0.30, 0.31)
    c.setFont("Helvetica", 9.8)
    c.drawString(M + 16, y - 37, "Attachments are one of the most reliable ways to land in spam. Mailchimp's own docs say they")
    c.drawString(M + 16, y - 50, "can slow or stop bulk delivery — which is why it hosts your file instead, capped at 10 MB.")

    y -= 84
    y = heading(c, y, "The five that cost sign-ups")
    body(c, y, [
        "attaching the file · asking for a name, phone and company · a promise so broad",
        "nobody feels it's for them · thirty pages instead of two · no follow-up at all",
        "",
        "Four of those five have nothing to do with the design.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------------- read me ----------
def readme(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Read me first", "lead magnet kit")

    blocks = [
        ("What's in this kit", [
            "The editable Canva template — cover, the what-you-get page, a content",
            "   page, a checklist page with real checkboxes, and the one-step last page",
            "The four reference PDFs (promise worksheet, email scripts, form wording,",
            "   launch checklist)",
        ]),
        ("How to use the template", [
            "Open the template link — it copies into your own Canva account.",
            "Page 1 is the cover: the promise as a headline, your name small. Resist",
            "   putting your logo enormous at the top — nobody downloaded it for that.",
            "Page 2 is the page almost everybody skips, and the one that makes people",
            "   read the rest: what this is, what they'll be able to do, how long it takes.",
            "Pages 3+ are one idea each. Resist filling the space — a page that looks",
            "   quick to read gets read.",
            "The last page is not a goodbye. It's one next step, one button, one line.",
        ]),
        ("Then the part that decides whether it works", [
            "Share → Download → PDF Standard (not Print).",
            "Upload that PDF somewhere it lives — your email tool's own file hosting,",
            "   your website, or a cloud drive with the link set to anyone-with-the-link.",
            "The delivery email contains a BUTTON pointing at it. The file never travels",
            "   inside the email. See the launch checklist for why.",
        ]),
        ("The machine, in order", [
            "the magnet (this template) → the form (one field) → the delivery email",
            "   (linked, immediate) → the thank-you page (three jobs) → three follow-ups",
            "Written once, it runs for every person who ever downloads the file.",
        ]),
        ("Licence", [
            "Use this kit for your own lead magnets, on unlimited offers, including ones",
            "   you sell.",
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
        ("leadmagnet-promise-worksheet.pdf", promise_worksheet),
        ("leadmagnet-email-scripts.pdf", email_scripts),
        ("leadmagnet-form-wording.pdf", form_wording),
        ("leadmagnet-launch-checklist.pdf", launch_checklist),
        ("leadmagnet-READ-ME.pdf", readme),
    ]
    for name, fn in made:
        fn(os.path.join(OUT, name))
    print(f"wrote {len(made)} PDFs")
