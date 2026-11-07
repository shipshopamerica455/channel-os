"""TPT worksheet pack — the exact product the tutorial builds.
US letter (8.5x11"), 0.5" margins, the skeleton from the video:
header (Name/Date) · title · instruction · 4x5 problem grid · footer.

    python3 make_worksheets.py

Outputs:
  tpt-addition-pack-15-worksheets.pdf   (easy/medium/challenge x5)
  tpt-addition-pack-answer-keys.pdf     (matching keys, answers in red)
  tpt-pack-cover.pdf                    (listing cover page)
  tpt-pack-preview.pdf                  (3 watermarked preview pages)
"""
import random
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

W, H = letter
M = 0.5 * inch
random.seed(42)  # reproducible pack

LEVELS = [
    ("Easy",      lambda: (random.randint(1, 9),   random.randint(1, 9))),
    ("Medium",    lambda: (random.randint(10, 49), random.randint(10, 49))),
    ("Challenge", lambda: (random.randint(50, 99), random.randint(50, 99))),
]

def sheet_problems():
    return None  # per-level generation below

def draw_skeleton(c, title, subtitle, key=False):
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawString(M, H - M - 14, "Name: ______________________")
    c.drawRightString(W - M, H - M - 14, "Date: ______________")
    c.setFont("Helvetica-Bold", 22)
    c.setFillColorRGB(0.07, 0.07, 0.07)
    t = title + ("   —   ANSWER KEY" if key else "")
    c.drawCentredString(W / 2, H - M - 52, t)
    if key:
        c.setStrokeColorRGB(0.82, 0.13, 0.13)
        c.setLineWidth(2)
        c.rect(W / 2 - 90, H - M - 60, 180, 0.01)  # subtle underline substitute
    c.setFont("Helvetica", 11.5)
    c.setFillColorRGB(0.27, 0.27, 0.27)
    c.drawString(M, H - M - 80, subtitle)
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.6, 0.6, 0.6)
    c.drawCentredString(W / 2, M - 16, "© Genius Junkie Resources · geniusjunkie.net")

def draw_grid(c, problems, answers=False):
    cols, rows = 4, 5
    x0, y1 = M, H - M - 100
    gw, gh = (W - 2 * M) / cols, (y1 - M - 24) / rows
    c.setStrokeColorRGB(0.62, 0.66, 0.7)
    c.setLineWidth(1.2)
    for r in range(rows + 1):
        c.line(x0, y1 - r * gh, x0 + cols * gw, y1 - r * gh)
    for col in range(cols + 1):
        c.line(x0 + col * gw, y1, x0 + col * gw, y1 - rows * gh)
    for i, (a, b) in enumerate(problems):
        cx = x0 + (i % cols) * gw + gw / 2
        cy = y1 - (i // cols) * gh - gh / 2
        c.setFont("Helvetica-Bold", 19)
        c.setFillColorRGB(0.12, 0.12, 0.12)
        c.drawCentredString(cx, cy + 12, f"{a} + {b} =")
        if answers:
            c.setFont("Helvetica-Bold", 17)
            c.setFillColorRGB(0.82, 0.13, 0.13)
            c.drawCentredString(cx, cy - 14, str(a + b))
        else:
            c.setStrokeColorRGB(0.75, 0.75, 0.75)
            c.setLineWidth(0.8)
            c.line(cx - 28, cy - 18, cx + 28, cy - 18)

def build_pack():
    sheets = []
    for lname, gen in LEVELS:
        for n in range(1, 6):
            sheets.append((f"Addition Practice — {lname} {n}",
                           "Solve each problem and show your work.",
                           [gen() for _ in range(20)]))
    c = canvas.Canvas("tpt-addition-pack-15-worksheets.pdf", pagesize=letter)
    c.setTitle("Grade 2 Addition Practice — 15 Worksheets")
    for title, sub, probs in sheets:
        draw_skeleton(c, title, sub)
        draw_grid(c, probs)
        c.showPage()
    c.save()
    k = canvas.Canvas("tpt-addition-pack-answer-keys.pdf", pagesize=letter)
    k.setTitle("Grade 2 Addition Practice — Answer Keys")
    for title, sub, probs in sheets:
        draw_skeleton(k, title, "Answer key — do not distribute to students.", key=True)
        draw_grid(k, probs, answers=True)
        k.showPage()
    k.save()
    return sheets

def build_cover():
    c = canvas.Canvas("tpt-pack-cover.pdf", pagesize=letter)
    c.setFillColorRGB(0.06, 0.09, 0.16)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColorRGB(1, 0.867, 0)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W / 2, H - 2.1 * inch, "2ND GRADE")
    c.drawCentredString(W / 2, H - 2.8 * inch, "ADDITION")
    c.setFillColorRGB(1, 1, 1)
    c.drawCentredString(W / 2, H - 3.5 * inch, "WORKSHEETS")
    c.setFont("Helvetica-Bold", 18)
    c.setFillColorRGB(0.78, 0.81, 0.87)
    c.drawCentredString(W / 2, H - 4.3 * inch, "15 pages  ·  3 levels  ·  answer keys  ·  no prep")
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.6, 0.6, 0.65)
    c.drawCentredString(W / 2, 1.0 * inch, "Genius Junkie Resources")
    c.showPage()
    c.save()

def build_preview(sheets):
    c = canvas.Canvas("tpt-pack-preview.pdf", pagesize=letter)
    c.setTitle("Preview — Grade 2 Addition Pack")
    for title, sub, probs in [sheets[0], sheets[5], sheets[10]]:
        draw_skeleton(c, title, sub)
        draw_grid(c, probs)
        c.saveState()
        c.translate(W / 2, H / 2)
        c.rotate(35)
        c.setFont("Helvetica-Bold", 90)
        c.setFillColorRGB(0.91, 0.12, 0.55, alpha=0.22)
        c.drawCentredString(0, 0, "PREVIEW")
        c.restoreState()
        c.showPage()
    c.save()

if __name__ == "__main__":
    sheets = build_pack()
    build_cover()
    build_preview(sheets)
    print("pack built: 15 worksheets + keys + cover + preview")
