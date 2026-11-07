#!/usr/bin/env python3
"""Media Kit + Rate Card — the fill-in set that ships with the editable Canva kit.

Outputs (all US Letter):
  mediakit-five-numbers-worksheet.pdf  the five numbers, where each one lives in Studio
  mediakit-pricing-calculator.pdf      the formula, the multipliers, three worked examples
  mediakit-email-scripts.pdf           inbound reply, outbound pitch, negotiation, follow-up
  mediakit-send-checklist.pdf          the eleven checks before it leaves your outbox
  mediakit-READ-ME.pdf                 how to use the template, and the licence
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


def fill_line(c, y, label, n=1, gap=22, width=None):
    c.setFillColorRGB(*TEAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M, y, label.upper())
    y -= 14
    for _ in range(n):
        rule(c, y, x1=(M + width) if width else None)
        y -= gap
    return y - 6


def callout(c, y, title, lines, col=PINK, h=None):
    """A bordered note. Height is derived so the body can never run past it."""
    h = h or (34 + 13 * len(lines))
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


# --------------------------------------------------- five numbers -----------
def five_numbers(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "The five numbers", "media kit + rate card")
    y = body(c, y, [
        "Everything a sponsor needs to decide is five numbers. Pull them once, write them",
        "here, and the kit becomes a twenty-minute job instead of a guessing game.",
        "All five live in YouTube Studio → Analytics → last 28 days.",
    ])
    y -= 16

    rows = [
        ("1. Delivered views per video",
         "Overview → Views ÷ videos published in the window. Not your subscriber count —",
         "this is the number they are actually buying."),
        ("2. Watch time, in minutes",
         "Overview → Watch time (hours) × 60. It says the audience stays, which is the",
         "difference between a view and an impression."),
        ("3. Where they live — top 4 countries",
         "Audience → Top geographies. Percentages, not raw numbers. This is the number",
         "that moves your price more than any other, so it goes in the kit, not out of it."),
        ("4. Who they are — age, gender, device",
         "Audience → Age and gender, and Overview → Device type. Two lines of the kit,",
         "and the thing that tells a brand whether their product fits at all."),
        ("5. How they found you",
         "Reach → Traffic source types. A high search share is worth saying out loud —",
         "it means the video keeps working after the campaign week ends."),
    ]
    for title, l1, l2 in rows:
        y = heading(c, y, title)
        y = body(c, y, [l1, l2], size=9.5, lead=13)
        y = fill_line(c, y, "your number", 1, gap=20, width=280)
        y -= 2

    y = callout(c, y, "Round down, and say the window", [
        "43,000 views a month over the last 28 days. Not 43,218, and not \"about 50k\".",
        "A rounded number with a date range attached reads as measured. A precise one",
        "with no window attached reads as picked.",
    ])
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------- calculator ---------
def pricing_calculator(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "What to charge", "media kit + rate card")
    y = body(c, y, [
        "Sponsorship pricing has a formula. It is not a secret and it is not a feeling.",
    ])
    y -= 18

    # the formula
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.4)
    c.roundRect(M, y - 52, W - 2 * M, 58, 9, stroke=1, fill=0)
    c.setFillColorRGB(*INK)
    c.setFont("Courier-Bold", 15)
    c.drawCentredString(W / 2, y - 24, "( delivered views / 1,000 )  x  CPM  x  format")
    c.setFillColorRGB(0.45, 0.47, 0.48)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, y - 42, "then adjust for where your audience lives")
    y -= 84

    y = heading(c, y, "CPM — what a thousand views is worth")
    y = body(c, y, [
        "Most creators sit somewhere around $15 to $25 in 2026. It swings hard by subject:",
        "software, finance and B2B run higher; entertainment and vlogs run lower.",
    ], size=9.5, lead=13)
    y = fill_line(c, y, "your CPM", 1, gap=20, width=200)

    y = heading(c, y, "Format — the multiplier")
    for t, v in [("A dedicated video, built around the product", "1.3 – 1.5x"),
                 ("A 60–90 second integration inside a bigger video", "0.7 – 0.9x"),
                 ("A description link + pinned comment", "0.2 – 0.3x"),
                 ("A Short", "0.5x")]:
        c.setFillColorRGB(0.28, 0.30, 0.31)
        c.setFont("Helvetica", 10)
        c.drawString(M + 8, y, t)
        c.setFillColorRGB(*AMBER)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawRightString(W - M - 8, y, v)
        y -= 17
    y -= 8

    y = heading(c, y, "Three worked examples")
    for label, calc, out in [
        ("5,000 views, $20 CPM, dedicated video", "5 x 20 = 100,  x 1.4", "$140"),
        ("20,000 views, $18 CPM, 90s integration", "20 x 18 = 360,  x 0.8", "$288"),
        ("43,000 views/mo, $15 CPM, description link", "43 x 15 = 645,  x 0.25", "$161"),
    ]:
        c.setFillColorRGB(0.28, 0.30, 0.31)
        c.setFont("Helvetica", 9.5)
        c.drawString(M + 8, y, label)
        c.setFont("Courier", 9.5)
        c.setFillColorRGB(0.45, 0.47, 0.48)
        c.drawString(M + 268, y, calc)
        c.setFont("Helvetica-Bold", 11)
        c.setFillColorRGB(*TEAL)
        c.drawRightString(W - M - 8, y, out)
        y -= 18
    y -= 10

    y = callout(c, y, "The multiplier nobody mentions", [
        "Where your audience lives moves that number by two to three times, for the exact same",
        "views in the exact same niche. US, UK, Canada and Australia price at the top of the range;",
        "a lower-CPM market prices well below it. That is not a reason to hide your country mix —",
        "it is the reason to put it on page two, with one sentence saying what it buys them.",
    ])

    # three rates side by side — a stacked column runs into the footer
    y = heading(c, y, "Your three rates")
    colw = (W - 2 * M - 40) / 3
    for i, lab in enumerate(["link placement", "integrated segment", "dedicated video"]):
        x = M + i * (colw + 20)
        c.setFillColorRGB(*TEAL)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x, y, lab.upper())
        c.setStrokeColorRGB(0.80, 0.82, 0.81)
        c.setLineWidth(0.8)
        c.line(x, y - 22, x + colw, y - 22)
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------- emails ----------
def email_scripts(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "The four emails", "media kit + rate card")
    y = body(c, y, [
        "Fill in the blanks and keep them short. The kit does the persuading; the email",
        "only has to get the kit opened.",
    ])
    y -= 12

    blocks = [
        ("EMAIL 1 — A BRAND APPROACHED YOU (reply same day)", [
            "Subject:  Re: <their subject line>",
            "",
            "Thanks for reaching out — <product> is a genuine fit for this audience.",
            "",
            "Media kit attached: audience, numbers and rates in one page each.",
            "Rates start at <link rate> for a description placement and <dedicated>",
            "for a dedicated video.",
            "",
            "Happy to put together a package if you'd like more than one placement.",
        ], PINK),
        ("EMAIL 2 — YOU APPROACHED THEM (cold)", [
            "Subject:  <their product> + <your channel> — <n> views/month",
            "",
            "I make <subject> tutorials for <who>. Last month: <views> views,",
            "<pct>% of them from search.",
            "",
            "<Their product> comes up constantly in the questions I get about <topic>.",
            "Media kit attached if it's useful — happy to send a rough plan for one video.",
        ], TEAL),
        ("EMAIL 3 — THEY SAID THE PRICE IS TOO HIGH", [
            "Subject:  Re: rates",
            "",
            "Understood. Two options rather than a discount:",
            "  • <smaller format> at <lower rate> — same audience, shorter placement",
            "  • the dedicated video at <rate>, paid half up front, half on publish",
            "",
            "I keep the rate the same across brands, so I can't go under it — but I",
            "can change what you get for it.",
        ], AMBER),
        ("EMAIL 4 — NOTHING BACK (one follow-up, then stop)", [
            "Subject:  Re: <original subject>",
            "",
            "Bumping this once in case it got buried — no problem at all if the timing",
            "is wrong. I'll leave it there either way.",
        ], (0.45, 0.47, 0.48)),
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
        y -= 14

    footer(c)
    c.showPage()

    # page two — the things not to write
    y = page(c, "Three lines to delete", "media kit + rate card")
    for t, s in [
        ('"Rates on request"',
         "It adds an email to the chain and tells them you have not decided. Put the number in."),
        ('"Negotiable"',
         "It tells them your first number was fiction, so they open below it. Price it once."),
        ('"I have a small but engaged audience"',
         "Never apologise for the size in the pitch. The numbers are on page one; let them read."),
    ]:
        c.setFillColorRGB(*PINK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(M, y, t)
        y -= 16
        y = body(c, y, [s], size=9.8, lead=13)
        y -= 10

    y -= 6
    y = callout(c, y, "One line that raises your price", [
        '"No undisclosed ads, and nothing I have not used."',
        "",
        "It costs you nothing and it tells a serious brand you will not be the creator who",
        "embarrasses them next quarter. Put it at the bottom of the rates page.",
    ], col=TEAL)

    y = heading(c, y, "And one thing to always state")
    body(c, y, [
        "How long the placement lasts. A description link with no end date is permanent,",
        "and permanent should not cost the same as six months. Put the duration next to",
        "every rate — it is the cheapest way to make the price look considered.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# -------------------------------------------------------- checklist ---------
def send_checklist(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Before you send it", "media kit + rate card")
    y = body(c, y, [
        "Eleven checks. Print it, or tick it on screen. Most rejected pitches fail on",
        "one of the first four.",
    ])
    y -= 16

    checks = [
        "Every number has a date range next to it (\"last 28 days\").",
        "Delivered views appear before subscriber count — or instead of it.",
        "The top four countries are on the audience page, in percentages.",
        "Age, gender and device are one line each, not a chart each.",
        "Three rates, three prices. No \"rates on request\", no \"negotiable\".",
        "Every rate says how long the placement lasts.",
        "The one-line standards sentence is on the rates page.",
        "One contact email, and it is one you actually check.",
        "The file is a PDF, not a Canva link — exported at PDF Standard.",
        "The filename is your channel name and the month, not \"media kit final v3\".",
        "It is three pages. Not eight.",
    ]
    for q in checks:
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(1)
        c.rect(M, y - 3, 11, 11, stroke=1, fill=0)
        c.setFillColorRGB(0.28, 0.30, 0.31)
        c.setFont("Helvetica", 10)
        c.drawString(M + 20, y, q)
        y -= 21

    y -= 10
    y = callout(c, y, "Update it once a month, not once a deal", [
        "The five numbers take ten minutes to re-pull. A kit with last quarter's figures",
        "is worse than no kit — the first thing a brand does is check your recent views.",
    ])

    y = heading(c, y, "What happens after you send it")
    body(c, y, [
        "Most approaches go quiet. That is normal and it is not about the kit. Send one",
        "follow-up after a week, then stop and move on to the next one. The kit is a",
        "document you write once and attach for years — its value is that it makes the",
        "next twenty conversations take four minutes each.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------------- read me ----------
def readme(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    y = page(c, "Read me first", "media kit + rate card")

    blocks = [
        ("What's in this kit", [
            "The editable Canva media kit — cover with the number cards, the audience",
            "   page, and the rates page with the three-row table",
            "The four reference PDFs (five-numbers worksheet, pricing calculator,",
            "   email scripts, send checklist)",
        ]),
        ("How to use the template", [
            "Open the template link — it copies into your own Canva account.",
            "Page 1 is the cover: your channel, what you make, and four number cards.",
            "   Four, not six — the cards stop being read past four.",
            "Page 2 is the audience: countries, age, gender, device. This is the page",
            "   brands read twice, because it is the one that tells them if they fit.",
            "Page 3 is the rates table: three formats, three prices, three durations,",
            "   and the one-line standards sentence underneath.",
            "Fill it in from the five-numbers worksheet, then export it as a PDF.",
        ]),
        ("The part people get backwards", [
            "A media kit is a pricing document, not a design problem. Its only job is to",
            "   make one specific number feel obviously fair.",
            "A sponsor is not buying your subscriber count — they are buying delivered",
            "   views. Those two numbers come apart much further than people expect,",
            "   and the kit that leads with the wrong one gets priced on the wrong one.",
        ]),
        ("Where your audience lives", [
            "It moves your price by two to three times, for identical views in an",
            "   identical niche. Put the country mix in the kit anyway — a brand selling",
            "   into those markets is buying reach it cannot get cheaper elsewhere.",
            "Hiding it does not raise your price. It just delays the question.",
        ]),
        ("Licence", [
            "Use this kit for your own channel and your own sponsorship pitches,",
            "   including paid ones.",
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
        ("mediakit-five-numbers-worksheet.pdf", five_numbers),
        ("mediakit-pricing-calculator.pdf", pricing_calculator),
        ("mediakit-email-scripts.pdf", email_scripts),
        ("mediakit-send-checklist.pdf", send_checklist),
        ("mediakit-READ-ME.pdf", readme),
    ]
    for name, fn in made:
        fn(os.path.join(OUT, name))
    print(f"wrote {len(made)} PDFs")
