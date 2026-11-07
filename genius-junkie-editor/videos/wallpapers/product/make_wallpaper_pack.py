#!/usr/bin/env python3
"""Wallpaper Kit — the reference sheets that ship with the two editable Canva
wallpaper templates (phone 1440 x 3120, desktop 3840 x 2160).

The arithmetic on the cheat sheet is COMPUTED, not typed, so the crop
percentages cannot drift from the device table above them.

Device resolutions checked 2026-08-25 (Apple tech specs / GSMArena / Samsung).
The Canva licence quotes are from Canva's own Help Centre, and the source is
printed on the sheet so a buyer can verify it.

Outputs (all US Letter):
  01-size-cheat-sheet.pdf        every current phone and monitor + the maths
  02-safe-zone-map.pdf           clock band, icon grid, dock — drawn to scale
  03-export-settings.pdf         PNG vs JPEG, the DPI myth, the final check
  04-palette-recipes.pdf         six palettes + the pull-from-one-photo method
  05-set-planner.pdf             the twelve-month recolour grid
  06-licence-plain-english.pdf   what Canva's licence does and does not allow
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

# ---------------------------------------------------------------- devices ---
# (name, native width, native height). Ratio and crop are DERIVED below.
PHONES = [
    ("iPhone 16 Pro Max", 1320, 2868),
    ("iPhone 16 Pro", 1206, 2622),
    ("iPhone 16 / 15", 1179, 2556),
    ("Galaxy S25 Ultra", 1440, 3120),
    ("Galaxy S25+", 1440, 3120),
    ("Galaxy S25", 1080, 2340),
    ("Pixel 9 Pro", 1280, 2856),
    ("Pixel 9", 1080, 2424),
]

MONITORS = [
    ("4K / UHD", 3840, 2160),
    ("1440p / QHD", 2560, 1440),
    ("1080p / FHD", 1920, 1080),
    ("MacBook Pro 14\"", 3024, 1964),
    ("Ultrawide 21:9", 3440, 1440),
]

OLD_W, OLD_H = 1080, 1920          # what most wallpaper templates ship at
DESIGN_W, DESIGN_H = 1440, 3120    # what this kit designs at


def crop_pct(dev_w, dev_h, src_w=OLD_W, src_h=OLD_H):
    """How much of a src-shaped image's WIDTH is lost filling a dev screen."""
    scale = dev_h / src_h                 # fill the height
    filled_w = src_w * scale
    if filled_w <= dev_w:
        return 0.0
    return (filled_w - dev_w) / filled_w * 100


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


# -------------------------------------------------------------- 1 · sizes ---
def pdf_sizes():
    c = pdfcanvas.Canvas(os.path.join(OUT, "01-size-cheat-sheet.pdf"), pagesize=letter)
    y = page(c, "Wallpaper sizes that survive", "genius junkie · wallpaper kit")

    y = para(c, y, "Design once, at the biggest and tallest, and let every device "
                   "scale DOWN. Downscaling looks clean. Upscaling never does.")
    y -= 6
    y = callout(c, y, "THE TWO NUMBERS", [
        f"Phone   {DESIGN_W} x {DESIGN_H} px   (19.5:9 — fits current iPhones and Android flagships)",
        "Desktop  3840 x 2160 px   (4K — divides cleanly to 2560x1440 and 1920x1080)",
    ], col=GREEN)

    y = heading(c, y, "Why the usual 1080 x 1920 fails")
    y = para(c, y, "1080 x 1920 is 16:9 — ratio 1.78. A current phone is 19.5:9 — "
                   "ratio 2.17. Your phone will not letterbox a wallpaper: it scales "
                   "the image until the HEIGHT matches, lets the width overhang, and "
                   "crops the overhang. So you lose width, not height.")
    y -= 4

    rows = []
    for name, dw, dh in PHONES:
        pct = crop_pct(dw, dh)
        rows.append([name, f"{dw} x {dh}", f"{dh/dw:.2f} : 1", f"{pct:.0f}%"])
    y = table(c, y, ["device", "native pixels", "tall : wide", "width lost*"],
              rows, [150, 130, 110, 90])
    y = body(c, y, ["* how much of a 1080 x 1920 wallpaper's width is cropped on that screen."],
             size=8.5, col=GREY)
    y -= 12

    y = heading(c, y, "Monitors")
    rows = [[n, f"{dw} x {dh}", f"{dw/dh:.2f} : 1"] for n, dw, dh in MONITORS]
    y = table(c, y, ["display", "native pixels", "wide : tall"], rows, [180, 150, 120])
    y -= 6
    y = callout(c, y, "CANVA'S OWN PAGE IS OUT OF DATE", [
        'canva.com/create/wallpapers still says: "Standard wallpaper has a resolution',
        'of 1024 x 768 and a screen ratio of 4:3." That is CRT-era advice. A 4:3 image',
        "on a 16:9 monitor is pillarboxed or cropped. Ignore it and use 3840 x 2160.",
    ])
    footer(c)
    c.save()


# ---------------------------------------------------------- 2 · safe zone ---
def phone_diagram(c, x, y, h, label, clock=0.26, dock=0.135):
    """A phone drawn to real 19.5:9 proportion with its furniture."""
    w = h * (DESIGN_W / DESIGN_H)
    c.setStrokeColorRGB(*GREY)
    c.setLineWidth(1.4)
    c.roundRect(x, y, w, h, 10, stroke=1, fill=0)

    # clock band
    c.setFillColorRGB(0.95, 0.90, 0.90)
    c.rect(x + 1, y + h - h * clock, w - 2, h * clock - 1, stroke=0, fill=1)
    c.setFillColorRGB(*PINK)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + w / 2, y + h - h * clock / 2 - 3, "CLOCK + DATE")

    # dock
    c.setFillColorRGB(0.95, 0.90, 0.90)
    c.rect(x + 1, y + 1, w - 2, h * dock, stroke=0, fill=1)
    c.setFillColorRGB(*PINK)
    c.drawCentredString(x + w / 2, y + h * dock / 2 - 3, "DOCK")

    # the safe band
    top = y + h - h * clock
    bot = y + h * dock
    c.setStrokeColorRGB(*GREEN)
    c.setLineWidth(2)
    c.rect(x + 3, bot + 3, w - 6, top - bot - 6, stroke=1, fill=0)
    c.setFillColorRGB(*GREEN)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + w / 2, (top + bot) / 2 - 3, "YOUR BAND")

    c.setFillColorRGB(*BODY)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(x + w / 2, y - 14, label)
    return w


def pdf_safezone():
    c = pdfcanvas.Canvas(os.path.join(OUT, "02-safe-zone-map.pdf"), pagesize=letter)
    y = page(c, "The safe zone", "genius junkie · wallpaper kit")
    y = para(c, y, "A phone screen is never empty. There is a clock and date across the "
                   "top, an app grid through the middle and a dock at the bottom. Only "
                   "one band of your wallpaper is reliably visible — and it is not where "
                   "most people put their focal element.")
    y -= 18

    dy = y - 300
    phone_diagram(c, M + 20, dy, 290, "iOS lock screen")
    phone_diagram(c, M + 200, dy, 290, "iOS home screen", clock=0.15, dock=0.16)
    phone_diagram(c, M + 380, dy, 290, "Android home", clock=0.12, dock=0.14)
    y = dy - 34

    y = heading(c, y, "The ten-second check")
    y = body(c, y, [
        "1 · Add a rectangle over the top quarter of the canvas.",
        "2 · Add a second over the bottom fifth.",
        "3 · Set both to 50% transparency.",
        "4 · What is left is your real canvas. Everything important lives inside it.",
        "5 · Delete both rectangles before you export.",
    ])
    y -= 8
    y = callout(c, y, "iOS DEPTH EFFECT", [
        "On the iOS lock screen your subject can sit IN FRONT of the clock — or refuse to.",
        "It is not a switch you control. It needs a clear subject with space around it.",
        "Leave a clean gap under the clock and it usually behaves. If not, move the",
        "subject lower.",
    ], col=BLUE)
    y = callout(c, y, "DESKTOP IS THE SAME IDEA, DIFFERENT FURNITURE", [
        "On a desktop the middle is where your windows and icons live. Move the focal",
        "element to the LEFT THIRD or RIGHT THIRD instead, and keep the centre quiet.",
    ], col=BLUE)
    footer(c)
    c.save()


# ------------------------------------------------------------- 3 · export ---
def pdf_export():
    c = pdfcanvas.Canvas(os.path.join(OUT, "03-export-settings.pdf"), pagesize=letter)
    y = page(c, "Export settings", "genius junkie · wallpaper kit")

    y = heading(c, y, "File type")
    y = table(c, y, ["your wallpaper is…", "export as", "why"], [
        ["Flat colour / gradient", "PNG", "JPEG bands smooth gradients"],
        ["Type or line art", "PNG", "keeps edges crisp"],
        ["A photograph", "JPG", "far smaller, no visible loss"],
        ["Photo + big flat areas", "PNG", "the flat areas are what band"],
    ], [190, 90, 220])
    y -= 4
    y = para(c, y, "On an OLED phone in a dark room, JPEG banding in a gradient is "
                   "genuinely visible. That is the whole reason for the rule.")
    y -= 10

    y = callout(c, y, "IGNORE THE DPI BOX", [
        "DPI does not exist on a screen. A screen has pixels, and you set those when",
        "you made the canvas. Changing DPI on a screen export changes nothing useful.",
        "Do not tick 'compress file' either.",
    ])

    y = heading(c, y, "The final check — do this every time")
    y = body(c, y, [
        f"[ ]  the downloaded file is {DESIGN_W} x {DESIGN_H} (phone) or 3840 x 2160 (desktop)",
        "[ ]  the background bleeds to all four edges — no border, nothing to crop",
        "[ ]  nothing important in the top quarter or the bottom fifth",
        "[ ]  the safe-zone guide layers are DELETED, not just hidden",
        "[ ]  set it on the phone and it snaps without a zoom prompt",
    ])
    y -= 8
    y = callout(c, y, "IF IT WILL NOT SNAP", [
        "Your file is the wrong shape. Go back and check the export — you have almost",
        "certainly exported the wrong page of the template.",
    ], col=AMBER)
    footer(c)
    c.save()


# ------------------------------------------------------------ 4 · palette ---
PALETTES = [
    ("Deep water", ["#0B1E33", "#123A5C", "#2E7DA8", "#7FC3D9", "#E8F3F6"]),
    ("Warm clay", ["#2B1B16", "#6B3A2C", "#B4694A", "#DFA07A", "#F5E3D6"]),
    ("Moss", ["#12200F", "#2C4423", "#547A3F", "#93B36B", "#E7F0DA"]),
    ("Dusk", ["#170F26", "#3A2350", "#6B3F94", "#A87FD1", "#EDE3F7"]),
    ("Ember", ["#1E0C0C", "#5A1B18", "#9E3324", "#D97644", "#F8E5D2"]),
    ("Slate + sun", ["#14181D", "#2C343D", "#586574", "#C9A227", "#F2EFE7"]),
]


def pdf_palettes():
    c = pdfcanvas.Canvas(os.path.join(OUT, "04-palette-recipes.pdf"), pagesize=letter)
    y = page(c, "Palette recipes", "genius junkie · wallpaper kit")
    y = para(c, y, "Six palettes that already work as a set. Each row is dark to light — "
                   "use the darkest for the background, the lightest for your focal "
                   "element, and let the middle three carry the gradient.")
    y -= 16

    for name, hexes in PALETTES:
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(M, y, name)
        x = M + 120
        for hx in hexes:
            r = int(hx[1:3], 16) / 255
            g = int(hx[3:5], 16) / 255
            b = int(hx[5:7], 16) / 255
            c.setFillColorRGB(r, g, b)
            c.rect(x, y - 8, 62, 26, stroke=0, fill=1)
            c.setFillColorRGB(*BODY)
            c.setFont("Helvetica", 7)
            c.drawCentredString(x + 31, y - 18, hx)
            x += 68
        y -= 44

    y -= 6
    y = callout(c, y, "THE PULL-FROM-ONE-PHOTO METHOD", [
        "Want a set that feels intentional rather than random? Drop ONE photo you like",
        "onto the Canva canvas, then use the colour picker (the eyedropper in the colour",
        "panel) to pull five shades straight off it. Every colour you pull will already",
        "agree with the others, because they came from the same image. For a seasonal",
        "set, use a seasonal photo. Delete the photo when you are done.",
    ], col=GREEN)
    footer(c)
    c.save()


# --------------------------------------------------------------- 5 · sets ---
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def pdf_planner():
    c = pdfcanvas.Canvas(os.path.join(OUT, "05-set-planner.pdf"), pagesize=letter)
    y = page(c, "The twelve-month set planner", "genius junkie · wallpaper kit")
    y = para(c, y, "One layout becomes a year of wallpapers. Keep the geometry identical "
                   "and change only the palette — that is what makes twelve files read as "
                   "one collection instead of twelve unrelated pictures.")
    y -= 16

    cw = (W - 2 * M) / 3
    rh = 96
    for i, mth in enumerate(MONTHS):
        col = i % 3
        row = i // 3
        x = M + col * cw
        yy = y - row * rh
        c.setStrokeColorRGB(*GREY)
        c.setLineWidth(0.8)
        c.rect(x, yy - rh + 14, cw - 12, rh - 18, stroke=1, fill=0)
        c.setFillColorRGB(*BLUE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 10, yy - 6, mth)
        c.setFillColorRGB(*GREY)
        c.setFont("Helvetica", 8)
        c.drawString(x + 10, yy - 24, "palette ______________")
        c.drawString(x + 10, yy - 40, "source photo _________")
        c.drawString(x + 10, yy - 56, "focal element ________")
    y = y - 4 * rh - 8

    y = callout(c, y, "HOW TO BUILD IT IN CANVA", [
        "1 · Finish page one properly — safe zone checked, background bleeding.",
        "2 · Duplicate the page (Cmd/Ctrl + D). Do this eleven times.",
        "3 · On each copy change ONLY the colours. Never move an element.",
        "4 · Export all pages at once: Share > Download > PNG > all pages.",
        "5 · Name the files by month before you upload them anywhere.",
    ], col=GREEN)
    footer(c)
    c.save()


# ------------------------------------------------------------ 6 · licence ---
def pdf_licence():
    c = pdfcanvas.Canvas(os.path.join(OUT, "06-licence-plain-english.pdf"), pagesize=letter)
    y = page(c, "Selling wallpapers: what the licence allows", "genius junkie · wallpaper kit")
    y = para(c, y, "This matters if you plan to sell a wallpaper pack. It is a summary of "
                   "Canva's own published terms, not legal advice — read the source and "
                   "decide for yourself.")
    y -= 8

    y = callout(c, y, "CANVA'S WORDS", [
        '"You can\'t sell any Canva content on a standalone basis."',
        '"You can\'t sell standalone prints of Canva content, such as a printout of a',
        'stock photo without any other design elements."',
        "Source: Canva Help Centre, 'Use Canva to design digital and physical products",
        "for sale' — canva.com/help/licenses-copyright-legal-commercial-use/",
    ])

    y = heading(c, y, "What that means for a wallpaper")
    y = table(c, y, ["what you are selling", "allowed?"], [
        ["A Canva stock photo exported at 3840 x 2160", "No"],
        ["A Canva stock photo with a filter on it", "No"],
        ["Your own photo, your type, your layout", "Yes"],
        ["Canva shapes + gradients you composed + your type", "Yes"],
        ["A photo you licensed elsewhere + your design work", "Yes"],
        ["A Canva template resold as a template", "No"],
    ], [330, 90])
    y -= 6

    y = para(c, y, "Canva's test is whether you made a new creative work: their content "
                   "\"with a combination of design elements ... and editing techniques\". "
                   "One stock element, lightly changed, is not that. Your own composition "
                   "using their shapes and fonts is.")
    y -= 10

    y = callout(c, y, "THE PRACTICAL RULE", [
        "If someone could get the same result by downloading one stock asset, you are",
        "selling their asset, not your design. Add your own type, your own layout and",
        "your own colour work — and if a photograph is the whole product, use one you",
        "shot or licensed yourself.",
    ], col=GREEN)
    y = callout(c, y, "ALSO CHECK", [
        "Fonts: most Canva fonts are fine in a flattened image. Do not redistribute the",
        "font file itself. And a wallpaper of a recognisable brand, logo, character or",
        "person is a different problem entirely — that is trademark and likeness, which",
        "no Canva licence covers.",
    ], col=AMBER)
    footer(c)
    c.save()


if __name__ == "__main__":
    pdf_sizes()
    pdf_safezone()
    pdf_export()
    pdf_palettes()
    pdf_planner()
    pdf_licence()
    print("wrote 6 PDFs")
