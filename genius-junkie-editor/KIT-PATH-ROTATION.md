# Paid-kit path rotation — 3 Nov 2026

## Why

The 25 `*-thank-you` pages deliver the £4.99 kits, and the kit PDFs sat at
`/content/files/club/`. Those URLs were public, permanently cacheable and listed
in `sitemap-pages.xml`, so anyone could reach the paid files without paying.

A noindex was deployed first (nginx `X-Robots-Tag` on the delivery paths). That
stops the URLs being *indexed*; it does not stop anyone who already has one.
This rotation retires the URLs themselves.

## What changed

**On the server**
- `/var/www/ghost/content/files/club/` → `/var/www/ghost/content/files/club-<16 hex>/`
  (132 files, 6.6 MB). The old directory is retired, not deleted, at
  `/home/ubuntu/club-retired-20261103/`.
- nginx noindex map widened from `~*^/content/files/club/` to
  `~*^/content/files/club(-|/)`, so the rotated prefix is covered too.
  Backup: `/etc/nginx/sites-available/geniusjunkie.net.conf.bak-*`.

**In Ghost** — 26 pages repointed, 140 links: the 25 thank-you pages (132) and
`/library/`, the Club tier page (8). Edited as **lexical**, never
`?source=html`, which flattens html cards. The 26 `canva.link` URLs were
re-counted afterwards and are unchanged, so the round-trip was lossless.

**In this repo**
- The prefix lives in `pipeline/kit-base.json` **only**, and that file is
  gitignored. `kitBase()` in `pipeline/lib/util.mjs` reads it, lazily, and
  throws rather than falling back — a wrong prefix would republish the kits on a
  public path.
- `thanks.html` sources now use the `KIT_BASE` placeholder, resolved at publish
  time by `commerce()` in `ship.mjs` alongside `STRIPE_LINK` and `CANVA_LINK`.
- `product()` uploads to the rotated prefix.

**Why the prefix is not in git:** this repo's remote,
`github.com/shipshopamerica455/channel-os`, is **PUBLIC**. It does not currently
contain `genius-junkie-editor/` (last pushed 12 Jul 2026, 56 files), but a
blanket `git add -A` would have published the kit paths *and* the `canva.link`
URLs, which are the product itself.

**The Canva links followed on 7 Nov 2026.** All 27 template share links — which
were spread across 39 files: 17 `video.json` products, two `thanks.html`
literals, six `SEO.md`, two `packaging.json`, four product docs, two PDF makers
and `VIDEOS.md` — now live only in gitignored `pipeline/canva-links.json`, read
by `canvaLinks()` / `canvaPlaceholders()` in `util.mjs`. Page sources carry
`CANVA_LINK` and, where a kit has two templates, `CANVA_LINK_DESKTOP` /
`CANVA_LINK_LETTER`; docs carry a `canva.link/<slug.key>` marker naming the
store entry. `commerce()` resolves longest placeholder first, because
`CANVA_LINK` is a prefix of `CANVA_LINK_DESKTOP` and the short one would
otherwise eat the suffix and publish a dead link.

**The product files were the next trap, and are now ignored too (7 Nov 2026).**
With the secrets out, `git add genius-junkie-editor` would still have staged
1,308 files and 1.1 GB — including the **153 paid kit PDFs**, which are the very
thing the path rotation hides, and 581 voice mp3s plus six 94-100 MB music beds
(at or over GitHub's per-file limit). No secret scanner would have flagged any
of it, because they are files, not credentials. `.gitignore` now excludes
`videos/**/product/*.pdf`, `product/*.png`, `vo/*.mp3`, `bed.wav`,
`voice-bakeoff/` audio and `__pycache__`, which takes the folder to **568 files
and 66 MB**, nothing over 1.3 MB. The kit makers (`product/*.py`, `*.md`) stay
tracked — they are the source and regenerate the PDFs. `videos/*/free/*.pdf` is
deliberately kept: the free rung is a giveaway.

Verified: every plan file, script, SEO note, description, thank-you page, anchor
image and pipeline module still stages; the paid PDFs, voice audio and both
secret stores do not.

**What is left is a judgement call, not a leak.** `VIDEOS.md`,
`SLATE-EVIDENCE.md` and the SEO notes carry channel strategy, revenue per video
and competitor research. None of it is a credential, but it is not obviously
something to publish either. Decide that before pushing.

## Still outstanding

1. **Purge the Cloudflare cache.** The old PDF URLs still return 200 publicly
   from the edge — `cf-cache-status: HIT`, `max-age=31536000`. Origin 404s all
   132, so the purge is what actually retires them. Until then this rotation is
   only half done.
2. **Set `canonical_url` on the 25 thank-you pages** in Ghost admin to drop them
   from `sitemap-pages.xml` — that sitemap listing was the discovery path.

Items 1 and 2 are now **checked automatically** — `gj-health-check.mjs` fails on
both until they are done:

```bash
node remotion-shorts/gj-health-check.mjs --only=kits
```

That `PAID KITS` section was added 3 Nov 2026 to close the blind spot that let
this run unnoticed: the check had only ever tested the FREE checklists' gating.
It discovers the delivery pages from Ghost rather than from a slug list, and
verifies every kit file downloads, the retired path is dead *publicly*, every
public delivery page sends `noindex` and none is left in `sitemap-pages.xml` —
plus, in the other direction, that the three real blog posts with "thank-you" in
their slug are not caught by the nginx regex.

## Rollback

```
ssh geniusjunkie 'sudo mv /home/ubuntu/club-retired-20261103 /var/www/ghost/content/files/club && sudo chown -R ghost:ghost /var/www/ghost/content/files/club'
```
Then re-run the repoint with OLD/NEW swapped. Both paths can serve at once —
that is how this was done with no downtime.

## Verified after the change

- 132/132 files serve on the new path at origin, all carrying `noindex`.
- 132/132 old paths 404 at origin.
- All 25 thank-you pages return 200 publicly, with 0 stale links and 132/132
  kit links resolving.
- `/library/` still leaks nothing anonymously; the upgrade CTA still renders.
- The homepage and other pages still send no `X-Robots-Tag`.
