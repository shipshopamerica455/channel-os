# Mellow Melodies — 30-Day Launch Calendar

**Positioning: functional focus music for traders and high-stakes work.**
Sleep and relaxation stay as the back catalogue, not the lead.

Grounded in the validated outlier data in [NICHE.md](NICHE.md). Every title below is
shaped for search intent, not brand voice — this category is found, not browsed.

---

## The format nobody is running: session-length alignment

The single ownable idea here. Every competitor publishes round numbers — 1 hour,
2 hours, 4 hours. **Nobody matches the video length to the actual work session.**

| Video length | Why that number |
|---|---|
| **6h 30m** | The NYSE cash session, 9:30–16:00 ET, exactly |
| **8h 00m** | The London session, 8:00–16:00 UK |
| **3h 00m** | The London/New York overlap — the highest-volume window of the day |
| **1h 30m** | The opening range, where most damage is done |

This does three things at once. It is a genuine differentiator in a copycat category.
It gives you titles that are self-explaining and searchable. And it is the most direct
possible attack on your actual problem — **a video whose length matches the viewer's
real session gets left running for that whole session**, which is exactly the average
view duration that turns 4,000 views into 4,000 watch hours.

You are not competing on music quality here. You are competing on *fit to a moment*.

---

## Cadence

**Three uploads a week — Tuesday, Thursday, Sunday.** Thirteen videos in 30 days.

Tuesday and Thursday are functional (the traffic and the CPM). Sunday is long-form
decompression/sleep (the watch-hour engine, and the bridge to the existing catalogue).

Publish 30–60 minutes before the session the video is named for. A "London Open" video
posted at 14:00 UK has missed its own audience.

---

## The calendar

### Week 1 — the proven core

Lead with the exact format that is already breaking out for sub-20k channels, so the
first videos land in a query with demonstrated demand rather than a query you invented.

| Day | Length | Title |
|---|---|---|
| **Tue 1** | 2h 00m | Deep Work Music for Traders — Stay Sharp and Calm Through the Session |
| **Thu 3** | 2h 00m | Focus Music for Chart Analysis — Calm Baroque for Clear Decisions |
| **Sun 6** | 8h 00m | 8 Hours of Calm Baroque for Sleep — Decompress After the Close |

### Week 2 — the session-length hook

| Day | Length | Title |
|---|---|---|
| **Tue 8** | **6h 30m** | The Full NYSE Session — 6.5 Hours of Focus Music, Open to Close |
| **Thu 10** | 1h 30m | The Opening Range — 90 Minutes of Low-Cortisol Focus Music |
| **Sun 13** | 8h 00m | Baroque for Deep Sleep — 8 Hours, No Ads, No Interruptions |

### Week 3 — the pain point

Volatility, tilt, and revenge trading are what this audience actually suffers. Name it.

| Day | Length | Title |
|---|---|---|
| **Tue 15** | 3h 00m | London–New York Overlap — 3 Hours of Focus for the Busiest Window |
| **Thu 17** | 2h 00m | Music to Stop Revenge Trading — Calm Strings for Emotional Control |
| **Sun 20** | 6h 00m | Sunday Reset — 6 Hours of Quiet Piano Before the Week Opens |

### Week 4 — duration and repetition

Repeat the winners at greater length. In this category the second, longer cut of a
video that worked routinely outperforms the first.

| Day | Length | Title |
|---|---|---|
| **Tue 22** | **8h 00m** | The Full London Session — 8 Hours of Deep Work Music |
| **Thu 24** | 4h 00m | 60 BPM Baroque for Linear Thinking — 4 Hour Deep Work Block |
| **Sun 27** | 10h 00m | 10 Hours of Calm Classical for Sleep — Black Screen, No Ads |
| **Tue 29** | 2h 00m | Pre-Market Focus — 2 Hours to Prepare Before the Bell |

---

## Production — FlowMusic prompts

Three beds cover the whole calendar. Generate 12–20 takes per bed and reuse across
videos; `musicBed()` caches takes on disk, so only the first build of each costs credits.

**Bed A — session focus** (Tue/Thu functional videos)

> Slow baroque-influenced strings and harpsichord at roughly 60 BPM, steady and even,
> no dynamic swells, no dramatic resolution, no percussion, no vocals. Warm and
> uncluttered, sitting low in the mix. Music to think clearly to for several hours
> without noticing it.

**Bed B — decompression** (Sunday long-form)

> Slow solo piano with soft room reverb, unhurried, sparse, no melody hooks that draw
> attention, no percussion, no vocals. Warm and dark. Calm background music for sleep.

**Bed C — emotional regulation** (the tilt/volatility videos)

> Sustained low strings and cello, very slow, no crescendo, no tension, no resolution
> to strain toward. Steady and grounding. Music to lower a raised heart rate.

```bash
cd video-forge
node -e "
import('./lib/flowmusic.mjs').then(async m => {
  await m.musicBed({
    prompt: '<Bed A text>',
    minutes: 390,            // 6h30m — the NYSE session
    variants: 16,
    outPath: '/path/to/nyse-session.mp3',
  });
});
"
```

**Set `variants` by length**: 12 for videos up to 2h, 16 up to 6h, 20 beyond. Too few
and the loop becomes audible, which is the fastest way to lose a long-session viewer.

## Visuals

Per [AUTOMATION.md](AUTOMATION.md), a single still looped for six hours is the exact
profile YouTube's inauthentic-content policy screens for. Generate a Veo clip and loop
it long, rather than holding a frame.

Subject matter that fits the positioning and does not date: rain on a window at night,
a quiet desk lit by one lamp, a city skyline before dawn, slow cloud over a still lake.
**No charts, no candlesticks, no tickers** — the audience is trying to look away from a
screen full of those, and a green candle in the corner of the frame is an emotional
stimulus in a video sold on emotional regulation.

## Thumbnails

Readable at 200px, because most of this traffic arrives on mobile search.

- Duration in the largest element on the tile — **6.5 HOURS**. It is the primary
  buying decision in this category.
- The function underneath, in two or three words — *NYSE SESSION*, *DEEP WORK*,
  *SLEEP*.
- One consistent colour treatment across all uploads so the channel reads as a set.
- Drop the AI Bach portraits. They signal "classical music channel," which is the
  positioning you are leaving.

---

## What to measure, and when

Judge nothing before day 30 — search-driven long-form takes weeks to settle.

At day 30, the number that matters is **average view duration**, not views. AVD tells
you whether the format fits the session; views only tell you whether the title works.
A video with 200 views and 90-minute AVD is worth more than 2,000 views at 4 minutes,
both toward the gate and as a signal of what to make next.

Target after 30 days: **150–250 watch hours**. That is ~4% of the gate and sounds
discouraging, but the curve in this category is not linear — the back catalogue
compounds as each video accumulates search traffic indefinitely, and one video that
catches carries the rest. You currently have 9 hours; 200 would be a 22× improvement
in a month.
