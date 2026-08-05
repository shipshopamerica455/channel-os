# Blue-Ocean Run — Relaxing/Classical Music Ecosystem

Run: `niche-scout/out/2026-07-25-21-55/report.md`

```bash
node scout.mjs --niche "relaxing classical music for sleep and study" \
  --min-duration 600 --no-transcripts --llm gemini
```

`--min-duration 600` instead of `--long-only` (180s): in this category a 3-minute
video is still the wrong format. The floor needs to sit above single-track uploads so
only genuine compilations score. `--no-transcripts` because music videos have no
useful captions.

## Data quality — read this before trusting the report

**The Shorts contamination that ruined the health run is gone.** All 150 validated
hits: minimum 10.5 min, median **2.1 hours**, max 23.8 hours. Zero under 3 minutes.
The duration filter worked.

**But two verdicts in the generated report are wrong, and one is wrong in a dangerous
direction:**

1. **`nordic-solitude-piano` was ranked 🔴 on zero data.** The YouTube API daily search
   quota ran out before its queries executed. The report read the missing results as
   *"Zero recent breakout data"* — that is absence of evidence being reported as
   evidence of absence. Verdict is void, not negative.
2. **`acoustic-zen-guitar` and `minimalist-harp-anxiety` got one query each**, not two.
   Half-validated; treat as provisional.

Everything else got full coverage. **The two top picks are on complete data.**

## The #1 pick is half a mirage

The report fused two things into "Monastic Scriptorium". They validate very differently:

**"Monk mode" focus music — genuinely hot, and recent:**

| Outlier | Views | Subs | Length | Age | Channel |
|---|---|---|---|---|---|
| **46.6×** | 811,004 | 17,400 | 2.1h | **65d** | Lock in Focus |
| **22.5×** | 14,129 | **627** | 2.0h | **42d** | Deep Work Studio |

**"Medieval scriptorium" — a stale ASMR niche, not a music one:**

| Outlier | Views | Subs | Age | Channel |
|---|---|---|---|---|
| 17.2× | 1,405,960 | 81,500 | **2,507d** | RPG Ambient Sounds |
| 11.8× | 960,584 | 81,500 | **2,311d** | RPG Ambient Sounds |
| 8.1× | 658,289 | 81,500 | **1,641d** | RPG Ambient Sounds |

Every scriptorium winner is 4½–7 years old, ASMR rather than music, and one channel
owns all three. The aesthetic is not the opportunity; the **"monk mode" productivity
hook** is. And it is cooling as fast as it is heating — of six small channels in that
query, only two broke out; Still Flow (48 subs) got 305 views and Sable Hour (24 subs)
got 270.

## The #2 pick is the stronger one

**Trader / high-stakes focus music** has what #1 only half has — *multiple recent
breakouts by small channels*:

| Outlier | Views | Subs | Length | Age | Channel |
|---|---|---|---|---|---|
| 75.6× | 115,669 | **1,530** | 4.3h | 1,500d | Psycho Micro Futures |
| **64.6×** | 6,459 | **35** | 1.0h | 322d | BlackBat FX |
| **55.4×** | 523,118 | **9,450** | 2.1h | **253d** | Focus Ambient Lab |
| **38.2×** | 724,954 | **19,000** | 2.2h | **265d** | Beat Trade Studio |

Three breakouts inside the last year, all from channels smaller than 20k subs. That is
the strongest buy signal the method recognises, and it is a cleaner read than #1's.

It also carries the one advantage nothing else on this list has: **the audience is
traders**, which is the highest-CPM demographic on YouTube. Watch hours from a finance
audience are worth several times the same hours from a generic sleep audience — and
after monetization, RPM is the entire game.

The bridge from the existing catalogue is real, not a stretch: Mellow Melodies is
already baroque, and *"60 BPM Baroque for linear thinking"* is the same music with a
functional promise attached.

## The catch

It is a **niche-bend away from the channel's stated identity**. "Curated classical for
tranquility" and "low-cortisol audio for traders" are not the same brand. The method
prescribes exactly this move — keep the format, bridge to an adjacent hunger — but it
reshapes what the channel is, and that is a positioning call, not a data call.

## Recommendation

**Lead with trader/deep-work functional music, keep sleep as the back catalogue.**
The functional angle earns the traffic and the CPM; the sleep compilations earn the
watch hours per view. They share a production pipeline entirely.

Before committing, run the report's own checklist: search **"monk mode focus music"**
and **"deep work music for traders"** on YouTube and confirm the small-channel
breakouts are still visible on page one.
