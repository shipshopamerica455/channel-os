# Mellow Melodies — Automated Pipeline

> **Decision, 2026-07-26: music comes from Google Flow Music — it is included in Ultra.**
> Confirmed on the account page: `ethishmlofar@gmail.com` shows **Tier: Member** (the top
> tier) with **30,530 credits**, 30,000 granted that day. Nothing extra to pay, and it is
> the same Gmail already linked for Flow.
>
> Public pricing pages list Starter $8 / Plus $24 / Member $64 and say nothing about the
> Ultra grant, which is what sent this the wrong way initially. **Check the account page,
> not the pricing page.**
>
> Suno Pro stays as a paid fallback. Bed assembly is provider-agnostic, so Suno downloads
> work with no code change — see [Building a bed from downloads](#building-a-bed-from-downloads).
> But Suno has no public API (partner-only as of July 2026) and useapi does not wrap it,
> so Suno means manual generation. Flow Music is fully automatable and is the default.

## Flow Music

**Short answer: yes.** One useapi.net subscription ($15/mo) and one token drive both
Google Flow (images + Veo video) and Google Flow Music (audio). Verified against your
live token on 2026-07-25.

This is a better fit here than on any other channel in the portfolio. A long-form
ambient music channel is *almost entirely* generated assets — music, visuals, and a
title — with no script, no voiceover, and no research stage. It is the most
automatable format you run.

---

## Status of your account, right now

| | State |
|---|---|
| `USEAPI_TOKEN` | ✅ valid — authenticates against both `/google-flow` and `/flowmusic` |
| Google **Flow** account | ✅ linked — `ethishmlofar@gmail.com`, health `OK` |
| Google **Flow Music** account | ❌ **none linked** — `GET /v1/flowmusic/accounts` returns `{}` |

Flow and Flow Music are linked **separately**, even on the same token and the same
Gmail. Flow working tells you nothing about Flow Music. This is the one blocker.

---

## The one manual step

**Flow Music is a separate product at [flowmusic.app](https://www.flowmusic.app) — not
labs.google**, and it links by *refresh token*, not by the cookie extraction you did for
Flow. It needs your own Google login, so it cannot be automated from here.

1. Sign in to **flowmusic.app** with Google. Use a **dedicated** account, not your
   personal Gmail — useapi drives this session, and it will conflict with your own use.
2. Generate one song, and upload one image and one audio file. This clears the consent
   dialogs that would otherwise block API calls later.
3. **Sign out completely.**
4. Open DevTools (F12) → **Network** tab. Click **Login** and sign in with Google again.
5. Filter for `sb.flowmusic.app/auth/v1/token`, click the **`token?grant_type=pkce`**
   request, open **Response**, and copy the `refresh_token` value.
6. Register it:

```bash
cd video-forge && node scripts/flowmusic-link.mjs
```

The token is read from a hidden prompt — never pass it as a CLI argument, which would
put a live credential into shell history and the process list.

**Then clear flowmusic.app's cookies in that browser. Do NOT sign out.** Signing out
revokes the refresh token and kills the API link immediately; continuing to use Flow
Music there rotates the session and breaks it the same way. This is the single most
common way this setup fails.

useapi also offers a guided browser tool that does the extraction for you — worth trying
before the manual route.

Once linked, add to `video-forge/.env`:

```
USEAPI_FLOWMUSIC_ACCOUNT=the-gmail-you-linked@gmail.com
```

Omit it and the code falls back to `USEAPI_FLOW_ACCOUNT`, which is correct if you link
the same Gmail.

Then confirm:

```bash
cd video-forge && node scripts/flowmusic-smoke.mjs
```

It checks accounts *before* attempting generation, because an unlinked account returns
an opaque 4xx from the generate endpoint that is easy to misread as broken code.

---

## What was built

### `video-forge/lib/flowmusic.mjs`

The audio sibling of `lib/flow.mjs`, same house shape — endpoints centralized in a
`CONFIG` block so an API change stays a one-line fix.

| Export | Purpose |
|---|---|
| `flowMusicAccounts()` | list linked accounts |
| `flowMusicLink(refreshToken)` | the one-time link call above |
| `flowMusic(prompt, outPath, {seed})` | generate one track → mp3 |
| `flowMusicEdit({clip, operation})` | `cover` · `remix` · `extend` · `replace` · `effect` · `stems` |
| `flowMusicList()` | previously generated clips |
| `musicBed({prompt, minutes, variants, outPath})` | **the important one** — a multi-hour bed |
| `flowMusicUsage()` | token/credit usage |

Generation goes **async and polls** (a track takes ~2 min; holding an HTTP connection
that long is asking for trouble). Job polling tries `/music/{jobid}` then `/jobs/{jobid}`,
so either routing works.

### `musicBed()` — turning 3-minute songs into 3-hour videos

Flow Music returns songs of a few minutes. A sleep video needs hours. `musicBed()`:

1. generates `variants` distinct takes of one prompt (different seeds), **cached on
   disk** so a rerun costs nothing;
2. fades each take once;
3. repeats the set, **rotating the order every pass** so the same two tracks never sit
   adjacent twice;
4. joins in a **single concat pass**.

The obvious implementation — one long crossfade chain — re-encodes an ever-growing file
and is quadratic; at 160 joins for an 8-hour bed it is unusable. Fading each piece once
and concatenating is linear, and a short fade to silence between pieces is the normal
texture for this format anyway. It is the same move as the `sox fade t 2.5 0 4` step in
your existing hymn SOP.

```bash
node scripts/flowmusic-smoke.mjs --bed 20     # 20-minute bed from 4 takes
```

More `variants` = less perceptible looping, more credits. For a 3-hour upload, 12–20
takes is the sensible range.

### `video-forge/scripts/flowmusic-smoke.mjs`

`(no args)` checks the account link · `--generate` one track · `--bed N` an N-minute bed.

---

## Building a bed from downloads

The fallback path, for Suno or any other source. With Flow Music linked, `musicBed()`
does generation *and* assembly in one call and none of this is needed.

**1. Generate in Suno.** For each bed, produce **12–20 takes** of one prompt. Two settings
are not optional:

- **Instrumental ON.** Suno adds vocals by default. A voice is fatal here — the entire
  product is music you can think over.
- **Same style prompt across all takes**, varying only the seed. The bed has to sound
  like one continuous piece, not a playlist.

Prompts are in [CALENDAR-30-DAY.md](CALENDAR-30-DAY.md) — Bed A (session focus),
Bed B (decompression), Bed C (emotional regulation).

**2. Download** the takes into one folder per bed, e.g. `~/Music/mellow/bed-a-deepwork/`.

**3. Assemble:**

```bash
cd video-forge
node scripts/build-bed.mjs --dir ~/Music/mellow/bed-a-deepwork --minutes 120 \
  --out "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/beds/deepwork-2h.mp3"
```

It reports each source track, the repetition factor, and warns below 8 tracks — under
that the loop becomes audible, and the people most likely to notice are the ones leaving
it on for hours, which is exactly the watch time you are trying to earn.

Assembly lives in [`lib/musicbed.mjs`](../video-forge/lib/musicbed.mjs) and is
provider-agnostic: fade each track once, rotate the order every pass so the same two
tracks never sit adjacent twice, then a single concat pass. A long crossfade chain would
re-encode an ever-growing file — quadratic, and unusable at ~160 joins for 8 hours.

**Reuse the takes.** The same 16 takes assemble into a 2-hour, a 6.5-hour and an 8-hour
bed at no extra credit cost. Generate once per pillar, not once per video.

## The full loop, once linked

```
niche-scout report        → the micro-niche + title list
FlowMusic musicBed()      → 1–8 hours of original, unclaimable music
Flow (Nano Banana Pro)    → the still / key frames
Flow (Veo 3.1 i2v)        → slow moving visual, looped to length
ffmpeg                    → mux, chapter markers, fade in/out
upload-to-youtube.mjs     → publish on schedule
```

**The music being generated is the commercial point, not a shortcut.** It is yours: no
Content ID claim, no revenue diverted to a rights holder. Bach's *compositions* are
public domain; every *recording* of them is not. A channel built on other people's
Bach recordings cannot monetize regardless of how many watch hours it earns.

## Where automation must stop

Two places, both deliberate:

1. **Visuals must move and vary.** A single still looped for three hours is the exact
   profile YouTube's inauthentic-content policy screens for. Spend the Veo credits.
2. **Sequencing is an editorial act, not a shuffle.** Track order and pacing across a
   3-hour bed is the human contribution — and per [PLAN.md](PLAN.md) §5, it is part of
   what separates the channels that pass review from the ones that do not.

Automate the production. Do not automate the judgement.
