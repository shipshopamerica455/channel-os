# `gj` — the Genius Junkie production pipeline

One command per stage, resumable, and **it can never make a video public**.
Uploads land as private drafts with the publish date pre-set; you watch the
video and flip it yourself.

```bash
node pipeline/gj.mjs <command> <slug> [--force] [--dry-run] [--title A|B|C]
```

## The loop

```
gj brief <slug>     →  you (or Claude) write script.md
gj build <slug>     →  voice · align · timeline · images
                       you (or Claude) build the scenes in remotion/src/shots/<shotDir>
gj qa <slug>        →  contact sheets — READ THEM
gj ship <slug>      →  render · master · product · commerce · publish · notify
```

`gj all <slug>` runs build + qa and then stops at the QA gate.
`gj status` prints where every video stands.

## What each stage does

| stage | does | output |
|---|---|---|
| `brief` | reads the next unticked row of `VIDEOS.md`, computes the word budget from the measured speech rate, scaffolds `video.json` | `brief.md`, `video.json` |
| `voice` | Kokoro `bm_fable` for every `## SNN` section in `script.md`; warns if the projected runtime is near the 8:00 mid-roll gate | `vo/*.mp3` |
| `align` | local Whisper `small.en`, word-level | `words.json` |
| `timeline` | section offsets + global word list; stages audio into `media/projects/<project>/vo`; records the ad-break windows | `shots/<shotDir>/vo.gen.ts`, `video.json.timeline` |
| `images` | Flow cutaways from `video.json → images[]` (warns below 4 — the cutaway rule) | `media/projects/<project>/images/*.png` |
| `qa` | 16 evenly-spaced frames → 6-up contact sheets | `remotion/out/qa/SHEET-<slug>-*.png` |
| `render` | the long-form, every promo Short, and the thumbnail | `remotion/out/*.mp4` |
| `master` | mutes the designed ad windows, 2-pass loudnorm to −14 LUFS / −1.5 dBTP, **verifies the silence actually landed**, masters the Shorts | `final.mp4`, `shorts/*.mp4`, `thumbnail-A.png` |
| `product` | runs `product/make_*.py`, uploads the PDFs to the server | `content/files/<kit-base>/<folder>/` |
| `commerce` | creates the Stripe product/price/payment-link **on the server** (the key never leaves it), publishes the Ghost landing + thank-you pages | live pages + `video.json.product.stripe` |
| `publish` | picks the next free slot (≥2 days after the latest scheduled video, 17:00 UTC), uploads long-form + Shorts as **private** drafts with `publishAt` | YouTube drafts |
| `notify` | writes the hand-off checklist | `NEXT-ACTIONS.md` |

## `video.json` — the manifest

```jsonc
{
  "slug": "wall-art-etsy",
  "shotDir": "long-8",              // remotion/src/shots/<shotDir>
  "project": "gj-long-8",           // media/projects/<project>
  "composition": "Long8Art",
  "thumb": "GJThumb8",
  "promos": ["PromoArtDpi", "PromoArtRatios"],
  "promoNames": { "PromoArtDpi": "promo-dpi-trap" },
  "adAfter": ["05-design", "09-packaging"],   // VO stems the 1.4s gap follows
  "images": [{ "name": "gallery-wall", "prompt": "…" }],
  "product": {
    "name": "Wall Art Starter Pack", "amount": 499, "currency": "gbp",
    "folder": "wallart", "slug": "wall-art-starter-pack",
    "description": "…"
  },
  "pages": { "landing": "landing.html", "thankYou": "thanks.html" },
  "publishAt": null                 // null ⇒ auto-pick the next free slot
}
```

## Calibration (re-measure if the voice changes)

Measured over videos 5–7 with Kokoro `bm_fable`:

- **3.24 words/sec** (3.158 / 3.314 / 3.255)
- **+17.7 s** of pads, ad gaps and end screen on top of the raw VO
- ⇒ an 8:40 target = **~1,627 words**

Both live in `lib/util.mjs → CONFIG`. If you change voice, re-measure — an
8 % error here is the difference between two mid-rolls and none.

## Safety

- The uploader is channel-guarded to `UCz8eVGSEicfswKIe4XAp7Kw`; it aborts on
  any other channel.
- `publish` always sets `privacyStatus: private` + `publishAt`. There is no
  code path in this pipeline that sets a video public.
- `master` fails loudly if a declared ad window isn't actually silent —
  YouTube refuses manual mid-rolls over continuous narration.
- Every stage is idempotent; re-running is cheap and `--force` is explicit.
