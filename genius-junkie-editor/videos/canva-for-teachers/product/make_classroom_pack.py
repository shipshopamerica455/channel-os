#!/usr/bin/env python3
"""Classroom Kit — the reference set that ships with the editable Canva
activity shells.

The six shells are DRAWN to proportion rather than described, the same way the
scrapbook kit does it: the teacher can see the geometry of each page before
opening Canva.

Every Canva rule quoted here is from Canva's own Help Centre, checked
2026-08-19, and the sources are printed on the read-me so it can be verified.
Nothing here is legal advice — the consent letter is a starting point that your
school's own policy overrides.

Outputs (all US Letter):
  teachers-activity-shells.pdf     the six shells, drawn to proportion
  teachers-eligibility-setup.pdf   can you get it, verifying, inviting students
  teachers-assign-collect.pdf      Assign vs Share, link vs code, marking
  teachers-consent-letter.pdf      parental consent letter for under-13s
  teachers-prompt-bank.pdf         a term of do-now and exit-ticket prompts
  teachers-READ-ME.pdf             how to use the kit, sources, licence
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

OUT = os.path.dirname(os.path.abspath(__file__))

PAPER = (0.984, 0.980, 0.973)
INK = (0.078, 0.094, 0.114)
TEAL = (0.184, 0.490, 0.471)
AMBER = (0.851, 0.604, 0.169)
GREY = (0.659, 0.690, 0.682)
PINK = (0.914, 0.118, 0.549)
GREEN = (0.133, 0.773, 0.369)
BODY = (0.28, 0.30, 0.31)
BOX = (0.898, 0.925, 0.945)
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


def wrap(text, width_pt, size, font="Helvetica"):
    """Greedy wrap on real string widths — a char estimate overflows columns."""
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


# ----------------------------------------------------------------- shells ---
# (left, top, width, height, kind) in 0-1 page fractions, top measured DOWN.
# kind: 'box' = an empty answer box the student types in · 'rule' = ruled lines
#       'title' = a solid header bar · 'chip' = a small draggable piece
SHELLS = [
    ("1 · Do-now", "Four boxes. Same page every Monday.", [
        (0.06, 0.05, 0.88, 0.08, 'title'),
        (0.06, 0.19, 0.42, 0.30, 'box'), (0.52, 0.19, 0.42, 0.30, 'box'),
        (0.06, 0.55, 0.42, 0.30, 'box'), (0.52, 0.55, 0.42, 0.30, 'box'),
    ]),
    ("2 · Exit ticket", "Three questions and a confidence scale.", [
        (0.06, 0.05, 0.88, 0.08, 'title'),
        (0.06, 0.20, 0.88, 0.16, 'box'), (0.06, 0.40, 0.88, 0.16, 'box'),
        (0.06, 0.60, 0.88, 0.16, 'box'),
        (0.06, 0.84, 0.30, 0.07, 'chip'), (0.38, 0.84, 0.24, 0.07, 'chip'),
        (0.64, 0.84, 0.30, 0.07, 'chip'),
    ]),
    ("3 · Vocabulary", "Word · definition · sentence · picture.", [
        (0.06, 0.05, 0.88, 0.08, 'title'),
        (0.06, 0.18, 0.20, 0.72, 'box'), (0.28, 0.18, 0.30, 0.72, 'rule'),
        (0.60, 0.18, 0.34, 0.36, 'rule'), (0.60, 0.56, 0.34, 0.34, 'box'),
    ]),
    ("4 · Comparison grid", "Two things, four rows, one conclusion.", [
        (0.06, 0.05, 0.88, 0.08, 'title'),
        (0.06, 0.18, 0.26, 0.08, 'chip'), (0.34, 0.18, 0.30, 0.08, 'chip'),
        (0.66, 0.18, 0.28, 0.08, 'chip'),
        (0.06, 0.28, 0.26, 0.52, 'rule'), (0.34, 0.28, 0.30, 0.52, 'box'),
        (0.66, 0.28, 0.28, 0.52, 'box'),
        (0.06, 0.84, 0.88, 0.09, 'box'),
    ]),
    ("5 · Labelled diagram", "Drop your image in. Labels down the side.", [
        (0.06, 0.05, 0.88, 0.08, 'title'),
        (0.06, 0.18, 0.60, 0.62, 'box'),
        (0.70, 0.18, 0.24, 0.07, 'chip'), (0.70, 0.28, 0.24, 0.07, 'chip'),
        (0.70, 0.38, 0.24, 0.07, 'chip'), (0.70, 0.48, 0.24, 0.07, 'chip'),
        (0.70, 0.58, 0.24, 0.07, 'chip'), (0.70, 0.68, 0.24, 0.07, 'chip'),
        (0.06, 0.84, 0.88, 0.09, 'rule'),
    ]),
    ("6 · Reading response", "What it says · what it means · what you think.", [
        (0.06, 0.05, 0.88, 0.08, 'title'),
        (0.06, 0.18, 0.88, 0.06, 'chip'),
        (0.06, 0.28, 0.88, 0.18, 'rule'),
        (0.06, 0.50, 0.88, 0.18, 'rule'),
        (0.06, 0.72, 0.88, 0.21, 'box'),
    ]),
]


def shell_box(c, x, y, s, blocks, title, note):
    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(1)
    c.rect(x, y - s * 1.294, s, s * 1.294, stroke=1, fill=0)   # A4 proportion
    hh = s * 1.294
    for (bl, bt, bw, bh, kind) in blocks:
        bx = x + bl * s
        by = y - (bt + bh) * hh
        bw_pt, bh_pt = bw * s, bh * hh
        if kind == 'title':
            c.setFillColorRGB(*(0.16, 0.42, 0.41))
            c.rect(bx, by, bw_pt, bh_pt, stroke=0, fill=1)
        elif kind == 'chip':
            c.setFillColorRGB(*(0.93, 0.90, 0.84))
            c.rect(bx, by, bw_pt, bh_pt, stroke=0, fill=1)
        elif kind == 'rule':
            c.setStrokeColorRGB(*GREY)
            c.setLineWidth(0.6)
            rows = max(2, int(bh_pt / 8))
            for r in range(rows):
                ly = by + bh_pt - (r + 1) * (bh_pt / (rows + 1))
                c.line(bx, ly, bx + bw_pt, ly)
        else:   # an empty answer box — drawn as an outline, because it IS empty
            c.setStrokeColorRGB(0.62, 0.70, 0.76)
            c.setLineWidth(0.9)
            c.rect(bx, by, bw_pt, bh_pt, stroke=1, fill=0)
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x, y - hh - 16, title)
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 8.5)
    ny = y - hh - 28
    for ln in wrap(note, s, 8.5)[:2]:
        c.drawString(x, ny, ln)
        ny -= 10.5


def pdf_shells():
    c = pdfcanvas.Canvas(os.path.join(OUT, "teachers-activity-shells.pdf"), pagesize=letter)
    y = page(c, "Six shells, reused all term", "classroom kit")
    y = para(c, y, "These are the six activity pages in the template, drawn to proportion. None of "
                   "them contain any subject content — that is the point. Tuesday's lesson is typing "
                   "this week's words into a page that already exists, not designing a page.")
    y -= 4
    y = body(c, y, [
        "Teal bar = locked header.   Blue outline = an EMPTY answer box the student types in.",
        "Ruled block = lined writing space.   Sand chip = a small draggable label or option.",
    ], size=9.5, lead=13)
    y -= 10
    s = 1.55 * inch
    gap = 0.42 * inch
    col_x = [M, M + s + gap, M + 2 * (s + gap)]
    for i, (title, note, blocks) in enumerate(SHELLS):
        row = i // 3
        yy = y - row * (s * 1.294 + 62)
        shell_box(c, col_x[i % 3], yy, s, blocks, title, note)
    y = y - 2 * (s * 1.294 + 62) + 6
    y = callout(c, y, "The two things that make a shell work", [
        "1.  Leave the answer boxes genuinely EMPTY. A box with placeholder text in it is a box",
        "    the student has to clear first, and half of them will type underneath instead.",
        "2.  LOCK the title, the instructions and the borders. A student will drag your heading",
        "    off the page by accident, not by mischief, and will not notice they have done it.",
    ], col=TEAL)
    y = heading(c, y, "Handing them out")
    para(c, y, "Assign, not Share. Share points everyone at the same design; Assign gives every "
               "student their own copy. See the assign-and-collect sheet.")
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------------ eligibility ---
def pdf_eligibility():
    c = pdfcanvas.Canvas(os.path.join(OUT, "teachers-eligibility-setup.pdf"), pagesize=letter)
    y = page(c, "Can you actually have this?", "classroom kit")
    y = para(c, y, "Canva Education is free, worldwide, and not restricted by country — but the "
                   "eligibility list is narrower than most people assume. Check before you build.")
    y -= 4
    y = heading(c, y, "Eligible — if you are CURRENTLY active in the role")
    y = body(c, y, [
        "·  Certified K-12 (primary/secondary) teacher at a formally accredited school",
        "·  Certified K-12 school librarian",
        "·  Certified K-12 learning support assistant or teacher",
        "·  Certified K-12 curriculum specialist",
        "·  Certified teacher at a technical or vocational school serving those ages",
        "·  K-12 schools, school districts, departments of education, other school systems",
    ], size=10, lead=14)
    y -= 6
    y = callout(c, y, "NOT eligible — Canva is explicit about this list", [
        "·  Qualified teachers who are not currently in a teaching position",
        "·  Public librarians (city or county)      ·  Preschool and daycare assistants",
        "·  Colleges, universities, their lecturers, staff and students",
        "·  Continuing / further education, and adult education institutions",
        "·  Organisations running extracurricular activities outside school",
        "·  Parents of K-12 children",
        "·  Homeschool educators not licensed or employed by a K-12 institution",
        "If you are on this list, use a TEMPLATE LINK instead — see the last page of the read-me.",
    ])
    y = heading(c, y, "Signing up")
    y = body(c, y, [
        "1.  Go to the Canva Education sign-up page and choose Teacher.",
        "2.  Sign up with a verified educational email domain and you get access straight away.",
        "    You can also use your school's Clever, Microsoft or Google account.",
        "3.  If your domain is not recognised, upload ONE document showing your name, your school,",
        "    and your teaching position.",
    ], size=10, lead=14)
    y -= 2
    y = callout(c, y, "If you are in one of these countries", [
        "Japan, Australia, Canada, New Zealand, the United Kingdom, the United States,",
        "South Korea, or Europe — Canva says a copy of your teaching licence alone is enough.",
    ], col=AMBER)
    y = heading(c, y, "Adding your students")
    body(c, y, [
        "Students can only get access if YOU invite them, from your settings — they cannot join",
        "themselves. Canva Education is for K-12 age students; it is not available to college or",
        "university students.",
        "",
        "For any child under 13 you must have parental consent first. There is a letter you can",
        "send in this pack. Canva states the product is FERPA, COPPA and GDPR compliant, which is",
        "usually the sentence your safeguarding or data lead is asking for.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


# --------------------------------------------------------- assign/collect ---
def pdf_assign():
    c = pdfcanvas.Canvas(os.path.join(OUT, "teachers-assign-collect.pdf"), pagesize=letter)
    y = page(c, "Assign, then collect", "classroom kit")
    y = para(c, y, "The single most common Canva mistake in a classroom is sharing a design when you "
                   "meant to hand out copies of it. They look almost identical to set up and they do "
                   "opposite things.")
    y -= 6
    # the two-column comparison
    colw = (W - 2 * M - 20) / 2
    for i, (t, sub, lines, col) in enumerate([
        ("SHARE", "for colleagues", [
            "Everyone opens the SAME design.",
            "Edit / comment / view — all three",
            "point at one file.",
            "",
            "Right for co-planning with another",
            "teacher. Wrong for a class of 30.",
        ], AMBER),
        ("ASSIGN", "for students", [
            "Every student gets THEIR OWN copy.",
            "Their copy comes back to you when",
            "they submit it.",
            "",
            "The Assign button is in the top",
            "corner, and in the Share menu.",
        ], GREEN),
    ]):
        x = M + i * (colw + 20)
        c.setStrokeColorRGB(*col)
        c.setLineWidth(2)
        c.roundRect(x, y - 128, colw, 128, 9, stroke=1, fill=0)
        c.setFillColorRGB(*col)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(x + 14, y - 24, t)
        c.setFillColorRGB(*GREY)
        c.setFont("Helvetica-Oblique", 9.5)
        c.drawString(x + 14 + stringWidth(t, "Helvetica-Bold", 15) + 8, y - 24, sub)
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 9.5)
        yy = y - 44
        for ln in lines:
            c.drawString(x + 14, yy, ln)
            yy -= 13
    y -= 150
    y = heading(c, y, "Two ways to hand it out — and they are not equivalent")
    y = body(c, y, [
        "SHARE VIA LINK      Canva copies the link to your clipboard. Paste it into Google",
        "                    Classroom, Teams, email or your VLE.",
        "                    The link stays active for 30 DAYS. Deactivate link kills it sooner.",
        "",
        "ASSIGNMENT CODE     A short code students type in at the assignment join page.",
        "                    THE CODE EXPIRES IN 4 HOURS.",
    ], size=10, lead=14)
    y -= 2
    y = callout(c, y, "The four-hour rule", [
        "Generate the CODE in the lesson, never the night before — it will be dead by the bell.",
        "For anything you plan in advance, use the LINK.",
    ])
    y = heading(c, y, "What the student does")
    y = body(c, y, [
        "They need a Canva account — if they do not have one they are prompted to sign up, so",
        "budget a few minutes for a cold class. They open the assignment, work in their own copy,",
        "then select Send to teacher.",
        "",
        "After they send it, THEIR DESIGN BECOMES READ-ONLY. That is deliberate — it is handing the",
        "book in. If they need to change it, you request changes and they Resubmit. If they just",
        "want to keep experimenting, Make a copy leaves their submission untouched.",
    ], size=10, lead=14)
    y -= 4
    y = heading(c, y, "Collecting it")
    y = body(c, y, [
        "Everything lands on Classwork, as a status list rather than an inbox:",
        "     Not submitted  ·  To review  ·  Done  ·  Resubmission requested",
        "Set your classes up and you get a class dropdown to filter both the assignment list and",
        "the student list inside each one.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()

    # page two — the LMS routes
    y = page(c, "If your school lives in an LMS", "classroom kit")
    y = para(c, y, "Canva integrates directly with Canvas, Schoology, D2L, Moodle, Blackboard, "
                   "Google Classroom and Microsoft Teams. You do not have to move your class.")
    y -= 4
    y = heading(c, y, "Google Classroom")
    y = body(c, y, [
        "Assign  ->  Assign in Google Classroom  ->  connect the account once  ->  fill in title,",
        "instructions, class, due date and points  ->  Assign in Google Classroom.",
        "You can push the same activity to UP TO 20 CLASSES at once.",
    ], size=10, lead=14)
    y -= 2
    y = callout(c, y, "The one that wastes an afternoon", [
        "To assign the same design on a DIFFERENT platform as well, Canva says make a new copy",
        "of the design first. One design, one platform.",
    ], col=AMBER)
    y = heading(c, y, "Canvas")
    y = body(c, y, [
        "Assignments  ->  + Assignment  ->  Submission type: External Tool  ->  Find  ->  Canva",
        "Education  ->  pick or create the design  ->  Save & Publish.",
        "Students are given their own copy, and submit back for review in SpeedGrader.",
    ], size=10, lead=14)
    y -= 4
    y = heading(c, y, "Schoology")
    y = body(c, y, [
        "Add Materials  ->  Add Assignment  ->  Insert Content  ->  Canva Education  ->  pick the",
        "design  ->  Link text  ->  NEW DESIGN FOR EACH STUDENT  ->  Create.",
        "That last setting is the same idea as the Assign button, in Schoology's words.",
    ], size=10, lead=14)
    y -= 4
    y = heading(c, y, "D2L and Blackboard")
    y = body(c, y, [
        "Both follow the same shape: create the assignment, insert Canva Education as the tool,",
        "pick or create the design, publish. Submissions come back into the platform's own",
        "grading screen, where you can view the design and leave comments.",
    ], size=10, lead=14)
    y -= 6
    callout(c, y, "Whatever the route, check one thing", [
        "Open the assignment as a student would, or ask a colleague to. You are checking that you",
        "get YOUR OWN copy — not the teacher's original. If you land in the original, you shared",
        "instead of assigning, and thirty students are about to edit the same file.",
    ], col=TEAL)
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------------- consent ---
def _letter_lines():
    """The letter body as (text, bold, gap_before) — measured before it is drawn
    so the box fits it and the return slip always has room on the page."""
    return [
        ("Dear parent or carer,", True, 0),
        ("", False, 0),
        ("This term, [CLASS] will be using Canva for Education to complete some of their "
         "classwork — things like worksheets, posters, diagrams and short presentations. It "
         "replaces some of the paper we would normally hand out, and lets me give feedback on "
         "their work directly.", False, 2),
        ("", False, 0),
        ("Canva is a design tool used widely in schools. Canva states that Canva for Education "
         "is FERPA, COPPA and GDPR compliant and provides safe-for-school content.", False, 2),
        ("", False, 0),
        ("What this means in practice:", True, 2),
        ("·  Your child will have an account that I create and invite them to. They cannot sign "
         "themselves up to our class.", False, 0),
        ("·  They will use it to complete work I set, and to send that work back to me.", False, 0),
        ("·  Their work is visible to me and to them. It is not public.", False, 0),
        ("·  We will use it at school, and they may be asked to finish work at home.", False, 0),
        ("", False, 0),
        ("Because your child is under 13, I need your permission before I set their account up. "
         "Please complete and return the slip below by [DATE].", False, 2),
        ("", False, 0),
        ("If you would prefer your child not to have an account, that is completely fine — say so "
         "below and they will be given the same work on paper. It will not affect their marks or "
         "how they are taught.", False, 2),
        ("", False, 0),
        ("With thanks,", False, 0),
        ("[TEACHER NAME] · [SCHOOL] · [EMAIL]", False, 0),
    ]


def pdf_consent():
    c = pdfcanvas.Canvas(os.path.join(OUT, "teachers-consent-letter.pdf"), pagesize=letter)
    y = page(c, "Parental consent letter", "for students under 13")
    y = para(c, y, "Canva requires parental consent before a child under 13 uses a Canva Education "
                   "account. This is a starting point you can paste into your school's letterhead "
                   "and adapt — your school's own data protection policy and wording take "
                   "precedence over anything here.", size=10, lead=14)
    y -= 8

    SIZE, LEAD, PAD = 9.5, 13.4, 22
    inner = W - 2 * M - 36
    rows = []
    for text, bold, gap in _letter_lines():
        font = "Helvetica-Bold" if bold else "Helvetica"
        wrapped = wrap(text, inner, SIZE, font) if text else [""]
        rows.append((wrapped, font, gap))
    box_h = PAD * 2 + sum(len(w) * LEAD + g for w, _, g in rows)

    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(0.8)
    c.roundRect(M, y - box_h, W - 2 * M, box_h, 8, stroke=1, fill=0)
    ix, yy = M + 18, y - PAD - SIZE
    c.setFillColorRGB(*BODY)
    for wrapped, font, gap in rows:
        yy -= gap
        c.setFont(font, SIZE)
        for ln in wrapped:
            c.drawString(ix, yy, ln)
            yy -= LEAD

    y = y - box_h - 20
    c.setStrokeColorRGB(*GREY)
    c.setDash(3, 3)
    c.line(M, y, W - M, y)
    c.setDash()
    y -= 22
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M, y, "Please return this slip")
    y -= 21
    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 10)
    for label in ["Child's name", "Class"]:
        c.drawString(M, y, label)
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.6)
        c.line(M + 110, y - 2, W - M, y - 2)
        y -= 23
    y -= 2
    for opt in ["I give permission for my child to use a Canva for Education account.",
                "I would prefer my child to be given this work on paper."]:
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(1)
        c.rect(M, y - 3, 12, 12, stroke=1, fill=0)
        c.setFillColorRGB(*BODY)
        c.setFont("Helvetica", 10)
        c.drawString(M + 22, y, opt)
        y -= 23
    y -= 2
    for label in ["Signed", "Print name", "Date"]:
        c.setFillColorRGB(*BODY)
        c.drawString(M, y, label)
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.6)
        c.line(M + 110, y - 2, W - M, y - 2)
        y -= 23
    footer(c)
    c.showPage()
    c.save()


# ------------------------------------------------------------ prompt bank ---
DO_NOW = [
    "Write down three things you remember from last lesson. No looking.",
    "What is one word from this topic you still could not explain to a friend?",
    "Put these in order. You have two minutes.",
    "Correct the mistake in this sentence, and say why it is wrong.",
    "What would happen if we changed one thing about this?",
    "Draw it. Badly is fine.",
    "Two facts and one lie. Write them. We will guess.",
    "Finish this sentence: the hardest part of this topic is…",
    "What question would you ask an expert about this?",
    "Which of these two is the odd one out, and why? There is no wrong answer.",
]
EXIT = [
    "What is one thing you understand now that you did not at the start?",
    "What is still confusing? Be specific — 'all of it' does not help me.",
    "Explain today's idea to somebody two years younger.",
    "Where would you use this outside this room?",
    "Rate yourself out of five, then say what would move you up one.",
    "What did somebody else say today that changed your mind?",
    "Write the one sentence you would want on a revision card.",
    "What do you think we will do next lesson, and why?",
    "If you had to teach this, what would you do differently to me?",
    "One thing you got wrong today, and what you now know instead.",
]


def pdf_prompts():
    c = pdfcanvas.Canvas(os.path.join(OUT, "teachers-prompt-bank.pdf"), pagesize=letter)
    y = page(c, "A term of prompts", "classroom kit")
    y = para(c, y, "Subject-neutral, so they work in any lesson. Type one into the do-now or exit "
                   "ticket shell and assign it — that is the whole preparation.")
    y -= 8
    for title, items, col in [("Do-now — the first five minutes", DO_NOW, TEAL),
                              ("Exit ticket — the last five", EXIT, PINK)]:
        y = heading(c, y, title)
        for i, q in enumerate(items, 1):
            c.setFillColorRGB(*col)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(M + 2, y, f"{i:>2}")
            c.setFillColorRGB(*BODY)
            c.setFont("Helvetica", 10)
            for j, ln in enumerate(wrap(q, W - 2 * M - 30, 10)):
                c.drawString(M + 26, y, ln)
                if j:
                    y -= 13
            y -= 15.5
        y -= 12
    callout(c, y, "Why these are deliberately not subject-specific", [
        "A prompt bank you have to rewrite per topic is a prompt bank you stop using in week three.",
        "These ask about thinking, so the same ten carry a whole term in any subject.",
    ], col=AMBER)
    footer(c)
    c.showPage()
    c.save()


# ---------------------------------------------------------------- read me ---
def pdf_readme():
    c = pdfcanvas.Canvas(os.path.join(OUT, "teachers-READ-ME.pdf"), pagesize=letter)
    y = page(c, "Read me first", "classroom kit")
    y = para(c, y, "Thank you. Here is what is in the kit, and the order to use it in.")
    y -= 4
    y = heading(c, y, "What you have")
    y = body(c, y, [
        "The Canva template        six A4 activity shells — do-now, exit ticket, vocabulary,",
        "                          comparison grid, labelled diagram, reading response.",
        "                          Answer boxes are real empty boxes. Furniture is locked.",
        "activity-shells.pdf       the six, drawn to proportion",
        "eligibility-setup.pdf     can you get Canva Education, verifying, inviting students",
        "assign-collect.pdf        Assign vs Share, link vs code, marking, the LMS routes",
        "consent-letter.pdf        a parental consent letter for under-13s",
        "prompt-bank.pdf           twenty subject-neutral do-now and exit-ticket prompts",
    ], size=10, lead=14)
    y -= 4
    y = heading(c, y, "The order")
    y = body(c, y, [
        "1.  Check eligibility FIRST. The list is narrower than people expect.",
        "2.  Verify your account, then invite your students. Consent letters out for under-13s.",
        "3.  Open the template, type this week's content into a shell. Do not redesign the page.",
        "4.  Hand it out with ASSIGN, not Share. Link if you planned ahead, code only in the room.",
        "5.  Collect on Classwork and filter by status.",
    ], size=10, lead=14)
    y -= 4
    y = callout(c, y, "The mistake this kit exists to prevent", [
        "Share points every student at the SAME design — one file, thirty editors, work",
        "disappearing off each other's screens. Assign gives every student THEIR OWN copy.",
        "If you only remember one thing from the video, remember which button does which.",
    ])
    y = heading(c, y, "If you are not eligible for Canva Education")
    y = para(c, y, "You can still get the important half. Open the design, Share, and choose "
                   "Template link — Canva's own description is \"anyone with the link can use this "
                   "design as a template\", which means each learner opens their own copy and your "
                   "original is untouched. You do not get Classwork, statuses or submissions, so "
                   "work comes back however it does now. But nobody is editing your master file.",
             size=10, lead=14)
    y -= 6
    y = heading(c, y, "Sources, so you can check them")
    y = body(c, y, [
        "From Canva's Help Centre, checked 19 August 2026:",
        "  · \"Share class assignments in Canva\"   (Assign, the 30-day link, the 4-hour code,",
        "     Send to teacher, read-only on submit, Resubmit, Make a copy, Classwork statuses)",
        "  · \"About Canva Education\"   (who is and is not eligible, verification, inviting",
        "     students, parental consent under 13, FERPA / COPPA / GDPR)",
        "  · \"Use Canva on Canvas / Schoology / D2L / Blackboard (for teachers)\"   (own copy",
        "     per student, \"new design for each student\")",
        "  · \"Publish to Google Classroom\"   (up to 20 classes, new copy per platform)",
        "  · \"Share your design as a template link\"   (the not-eligible workaround)",
        "Canva changes things. If something here no longer matches, believe Canva.",
    ], size=9.5, lead=13)
    y -= 2
    y = heading(c, y, "Licence")
    body(c, y, [
        "Use it with your own classes, including in a school you are paid to teach at. Share the",
        "finished activities with your students freely. The template and these PDFs are not for",
        "resale or redistribution as templates.",
        "",
        "The consent letter is a starting point, not legal advice — your school's policy wins.",
    ], size=10, lead=14)
    footer(c)
    c.showPage()
    c.save()


if __name__ == "__main__":
    pdf_shells()
    pdf_eligibility()
    pdf_assign()
    pdf_consent()
    pdf_prompts()
    pdf_readme()
    print("wrote 6 PDFs")
