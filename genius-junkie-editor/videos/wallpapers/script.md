# Phone & Desktop Wallpapers in Canva — the size everybody gets wrong

## Facts verified 2026-08-25

**THE TRAP — a sixteen-by-nine wallpaper loses about a fifth of its width on a
modern phone.**

Canva's own wallpaper page (`canva.com/create/wallpapers`) still says, verbatim:

> "Common sizes for desktop wallpaper are 1024 x 768, 1280 x 1024 and 1920 x
> 1080 pixels."

and

> "Standard wallpaper has a resolution of 1024 x 768 and a screen ratio of 4:3."

That is monitor advice from the CRT era. Four-by-three on a widescreen monitor is
either pillarboxed with grey bars or cropped.

Canva's **phone** wallpaper template page publishes **no pixel dimension at all**
— it promises "Every template looks sharp on any device" and mentions "4K phone
wallpaper quality", but never states a size. The size the community defaults to,
and the one most third-party Canva wallpaper templates ship at, is
**1080 × 1920** — sixteen by nine.

**Real phones are not sixteen by nine:**

| Device | Resolution | Ratio |
|---|---|---|
| iPhone 16 Pro | 1206 × 2622 | 19.5 : 9 |
| Galaxy S25 | 1080 × 2340 | 19.5 : 9 |
| Galaxy S25+ / S25 Ultra | 1440 × 3120 | 19.5 : 9 |

**The maths (this is arithmetic, not a citation).** Sixteen by nine is 1.78.
Nineteen-and-a-half by nine is 2.17. The OS scales a wallpaper to *fill* the
screen, so it matches the height and lets the width overhang.

- On a Galaxy S25: 2340 ÷ 1920 = 1.219. Your 1080-wide image becomes 1316 wide.
  The screen is 1080. **236 pixels get cropped — about 18% of the width, 9% off
  each edge** — and everything left is upscaled 22%, so it is softer too.
- On an iPhone 16 Pro: 2622 ÷ 1920 = 1.366. 1080 becomes 1475 against a
  1206-wide screen. **269 pixels gone — 18% again.**

So the number is consistent: **design at sixteen by nine and you lose roughly a
fifth of the width, on every modern phone, before anyone sees it.**

**THE FIX:** design at **1440 × 3120** and let the phone downscale. Downscaling
is lossless-looking; upscaling never is. For desktop, design at **3840 × 2160**
— it divides cleanly to 2560 × 1440 and 1920 × 1080.

**THE SECOND TRAP — the licence, for anyone planning to sell these.**
Canva's Content Licence, via their help centre:

> "You can't sell any Canva content on a standalone basis."

and

> "you can't sell standalone prints of Canva content, such as a printout of a
> stock photo without any other design elements."

An original design means "using Canva Content with a combination of design
elements … and editing techniques to make a 'new' creative work." A stock photo
exported at wallpaper size is not that. Say this plainly — a lot of this audience
wants to sell wallpaper packs on Etsy.

---

## S01 — HOOK (~130 words)

> You make a wallpaper in Canva. It looks great on the screen in front of you.
> You send it to your phone, you set it, and the thing you spent forty minutes
> centring is now touching the edge, or half gone. Nothing is broken. Your
> phone did exactly what it is supposed to do. The wallpaper was the wrong
> shape, and the phone fixed that the only way it can, by blowing it up until
> it fills the screen and throwing away whatever hangs off the sides. On a
> current phone that is about a fifth of the width, gone. And it comes back
> softer than you made it. Today we build one properly, at the size that
> survives, for the phone and for the desktop, and I will show you the maths so
> you never have to guess again.

## S02 — WHY IT CROPS (~145 words)

> Two numbers explain everything in this video. Sixteen by nine, the shape of
> nearly every wallpaper template you will find, is one point seven eight. The
> shape of a current phone screen, nineteen and a half by nine, is two point one
> seven. Your phone will never letterbox a wallpaper. It will not put grey bars
> at the top and bottom of your lock screen. It scales the image until the
> height matches, and it accepts that the width now overhangs, and it crops the
> overhang. So the taller the screen, the more of your width disappears. This is
> the whole problem, and once you see it you cannot unsee it. Everything else we
> do today is a consequence of those two numbers.

## S03 — THE SIZES THAT ACTUALLY WORK (~165 words)

> Here is the size, and I want you to write it down. Phone: fourteen forty by
> thirty one twenty. That is the native resolution of a Galaxy S twenty five
> Ultra, and it is nineteen and a half by nine, so it is the right shape for
> current iPhones too. Design there and every phone downscales it. Downscaling
> is the safe direction. Upscaling is the one that costs you sharpness.
> Desktop: thirty eight forty by twenty one sixty. That is four K, and it
> divides cleanly in half to nineteen twenty by ten eighty, and neatly to
> twenty five sixty by fourteen forty, so one file covers every common monitor.
> Now, Canva's own wallpaper page will tell you that standard wallpaper is ten
> twenty four by seven sixty eight at four by three. That advice is older than
> most of the monitors you own. Do not use it.

## S04 — SETTING UP THE CANVAS (~145 words)

> Open Canva, top right, Create a design, and then Custom size — not the
> wallpaper preset, custom size. Change the unit to pixels first, because it
> defaults to something else and this catches everyone. Then fourteen forty
> wide, thirty one twenty tall. Create. What you are looking at now is a canvas
> the shape of a real phone, which means what you see is what you get, and that
> is the entire point. While we are here, do the desktop one as well, in the
> same account, so you are not hunting for it later. Custom size again, pixels
> again, thirty eight forty by twenty one sixty. Two canvases, correct shapes,
> and we have already avoided the thing that ruins most of these.

## S05 — BUILDING THE PHONE ONE (~200 words)

> Background first. I am going to use a flat colour rather than a photo, and I
> will tell you why in a minute when we get to the licence. Click the canvas,
> colour picker, and pick something with a bit of depth to it. Now Elements,
> and search for a gradient or a soft shape. Drop it in, and then drag it out
> past the edges of the canvas on purpose, so it bleeds off. Wallpapers should
> never have a visible border, because the moment there is a border you can see
> the crop happening. Now the focal thing, whatever the wallpaper is actually
> about. A shape, a word, a small illustration. Put it in and then leave it
> alone for a second, because where it goes matters more than what it is, and
> that is the next section. If you are using text, size it up more than feels
> right. A wallpaper is read at arm's length, past a layer of app icons, in
> daylight. What looks bold on your laptop looks apologetic on a phone.

→ **AD BREAK 1**

## S06 — THE SAFE ZONE (~180 words)

> This is the part nobody tells you, and it is the reason home-made wallpapers
> look home-made. Your phone screen is not empty. There is a clock and a date
> across the top third, and on iOS that clock is enormous. There is a row of
> app icons everywhere else, and a dock along the bottom. So there is exactly
> one band of your wallpaper that is reliably visible, and it is the middle. Not
> the top, the clock owns that. Not the bottom, the dock owns that. The middle.
> So take your focal element and move it into that band, and give it room. Here
> is the check, and it takes ten seconds: add a rectangle over the top quarter
> and the bottom fifth, set it to half transparent, and look at what is left.
> That is your real canvas. Everything important lives inside it. Delete the
> rectangles before you export. This one habit is the difference between a
> wallpaper that looks designed and one that looks like a photo you cropped.

## S07 — EXPORTING IT (~150 words)

> Share, Download, and now the format. For anything with flat colour, a
> gradient, or type — which is most wallpapers — choose PNG. JPEG compresses
> smooth gradients into visible bands, and on an OLED phone in a dark room you
> will see them. If your wallpaper is a photograph, JPEG is fine and the file
> will be much smaller. Ignore the DPI box entirely. DPI means nothing on a
> screen. A screen has pixels, and we already set the pixels when we made the
> canvas at fourteen forty by thirty one twenty. Do not tick "compress file" if
> it offers it. Download it, and get it onto your phone however you normally
> do — AirDrop, Google Photos, emailing it to yourself, all fine. The file that
> lands should be fourteen forty by thirty one twenty. Check that. If it is
> not, you exported the wrong page.

## S08 — THE DESKTOP VERSION, WITHOUT REBUILDING IT (~160 words)

> Now the trick that saves the second half of the job. You do not rebuild this
> for desktop. Open the phone design, File, and then Resize — on the free plan
> this is Resize and Magic Switch, and it will ask you to upgrade, so if you are
> on free, just copy the elements across to the four K canvas we made earlier
> by hand. It takes two minutes. If you do have Resize, choose Custom, thirty
> eight forty by twenty one sixty, and tick "copy and resize" so you keep the
> original. What comes out will be wrong, and that is expected. Everything that
> was stacked vertically for a tall screen is now floating in a wide one. So
> spread it out. The focal element moves off-centre — left third or right third
> — because on a desktop the middle is where your icons and your windows live.
> Same principle as the phone, different furniture.

## S09 — IF YOU PLAN TO SELL THESE (~160 words)

> Quick and important, because a lot of people watching this want to sell a
> wallpaper pack. Canva's content licence says you cannot sell Canva content on
> a standalone basis. Their own wording: you cannot sell standalone prints of
> Canva content, such as a printout of a stock photo without any other design
> elements. A stock photo exported at wallpaper size is exactly that. What you
> are allowed to sell is an original design — their words again — Canva content
> combined with other design elements and editing techniques to make a new
> creative work. So: a photograph you licensed elsewhere, or your own; type you
> set; shapes and gradients you built; a layout that is yours. That is a
> product. One of Canva's stock images at thirty eight forty by twenty one sixty
> is not, no matter how much you paid for Pro. This is the rule that gets Etsy
> shops taken down, so know it before you list.

→ **AD BREAK 2**

## S10 — MAKING IT A SET (~150 words)

> One wallpaper is a craft project. A set is a product, and it is barely more
> work. Duplicate the page — the little plus-and-page icon, or command D — and
> change only the colour. Same layout, same focal element, new palette. Do that
> five times and you have a set of six that obviously belong together, which is
> what makes people keep them. If you want them to feel intentional rather than
> random, pull the colours from one source: a photo you like, dropped into
> Canva, then use the colour picker on it. Every shade you pull will already
> agree with the others because they came from the same image. For a seasonal
> set, do the same thing with a seasonal photo. It is the cheapest way to make
> six things look like a collection instead of six things.

## S11 — SETTING IT, AND WHAT STILL GOES WRONG (~145 words)

> Two last things that catch people at the final step. First, when you set the
> wallpaper your phone may still offer to zoom or reposition it. If we sized it
> right there is nothing to fix, so pinch it back until it snaps and leave it.
> If it will not snap, your file is the wrong shape — go back and check the
> export. Second, on iOS the lock screen may put your subject behind the clock
> using the depth effect, or refuse to. It is not a setting you control
> directly; it depends on the picture having a clear subject with space around
> it. If it matters to you, leave a clean gap under the clock and it usually
> behaves. If it does not, move the subject lower. That is genuinely the whole
> fix.

## S12 — THE CHECKLIST (~115 words)

> Everything in one place. Phone, fourteen forty by thirty one twenty. Desktop,
> thirty eight forty by twenty one sixty. Custom size, in pixels, never the old
> preset. Bleed your background past the edges so there is no border to crop.
> Keep everything that matters in the middle band, away from the clock at the
> top and the dock at the bottom. Export PNG for flat and gradient work, JPEG
> only for photographs. Ignore DPI, it does not exist on a screen. Check the
> exported file is the size you asked for. And if you are selling, it has to be
> an original design, not a stock image at wallpaper size.

## S13 — THE PACK (~90 words)

> If you would rather start from something correct than set it up yourself, I
> have put the whole thing in a kit. Two editable Canva templates already at the
> right sizes — the phone one at fourteen forty by thirty one twenty and the
> desktop one at four K — with the safe zones marked as guides you delete before
> you export. Plus the size cheat sheet for every current phone, the export
> settings, the palette recipes for building a set, and a plain-English page on
> what the licence does and does not let you sell. Link below.

## S14 — OUTRO (~80 words)

> The short version, if you take nothing else: your phone crops the width, not
> the height, and it crops about a fifth of it. Design tall, keep it central,
> and the problem never happens. If you want the next one, the video on screen
> now is where I would go — it is the same idea applied to something you can
> actually charge for. Thanks for watching, and I will see you in the next one.

---

## Product sketch — Wallpaper Kit (£4.99)

**Canva templates (2):**
1. Phone — 1440 × 3120, safe-zone guide layers (clock band, dock band) on a
   separate deletable page-level group, one built example + five recolours.
2. Desktop — 3840 × 2160, icon-zone guide, same treatment.

**PDFs (6):**
1. `01-size-cheat-sheet.pdf` — every current phone and monitor, native
   resolution, ratio, and what to design at. The 18%-crop maths shown once.
2. `02-safe-zone-map.pdf` — the clock band, the icon grid, the dock, drawn to
   scale for iOS and Android, with the middle band marked.
3. `03-export-settings.pdf` — PNG vs JPEG decision tree, the DPI myth, the
   check-your-file step.
4. `04-palette-recipes.pdf` — six palettes with hex codes, plus the
   pull-from-one-photo method for building a set.
5. `05-set-planner.pdf` — the twelve-month recolour grid, so one layout becomes
   a year of wallpapers.
6. `06-licence-plain-english.pdf` — what Canva's content licence allows and
   forbids when selling wallpapers, quoted and then translated.
