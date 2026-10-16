#!/usr/bin/env node
/**
 * Generate a Mellow Melodies music bed via Flow Music.
 *
 *   node gen-bed.mjs --bed a --minutes 120 --out deepwork-2h.mp3
 *   node gen-bed.mjs --bed b --minutes 480 --takes 20    # 8h sleep
 *
 *   --bed      a (session focus) | b (decompression) | c (emotional regulation)
 *   --minutes  target length (default 120)
 *   --takes    distinct tracks to generate (default 16; each generation yields 1-2)
 *   --tag      names the take folder — use a NEW tag for fresh music (default: the bed)
 *   --out      filename inside the channel's beds/ folder
 *
 * Takes cache under beds/<tag>-parts/. Reusing a tag reuses the takes, so the same
 * material can assemble into a 2-hour, a 6.5-hour and an 8-hour cut for free.
 *
 * But prefer FRESH takes per video. A 2-clip generation costs 10 credits, so a whole
 * bed runs well under 200 — against ~30,000 available, the saving is meaningless, and
 * shipping the same audio rearranged across several uploads is both duller for anyone
 * who subscribes and closer to the "reused content" line than it needs to be.
 */
import path from "path";
import fs from "fs";
import { loadEnv } from "../video-forge/lib/env.mjs";
import { musicBed } from "../video-forge/lib/flowmusic.mjs";

loadEnv();

const BEDS = {
  a: {
    name: "session focus",
    prompt: `Slow baroque-influenced strings and harpsichord at roughly 60 BPM, steady and
even, no dynamic swells, no dramatic resolution, no percussion, no vocals. Warm and
uncluttered, sitting low in the mix. Music to think clearly to for several hours
without noticing it. Instrumental only.`,
  },
  b: {
    name: "decompression",
    prompt: `Slow solo piano with soft room reverb, unhurried, sparse, no melody hooks that
draw attention, no percussion, no vocals. Warm and dark. Calm background music for
sleep. Instrumental only.`,
  },
  c: {
    name: "emotional regulation",
    prompt: `Sustained low strings and cello, very slow, no crescendo, no tension, no
resolution to strain toward. Steady and grounding. Music to lower a raised heart rate.
Instrumental only.`,
  },
};

const args = {};
for (let i = 2; i < process.argv.length; i++) {
  if (process.argv[i].startsWith("--")) {
    const k = process.argv[i].slice(2), n = process.argv[i + 1];
    args[k] = n && !n.startsWith("--") ? process.argv[++i] : true;
  }
}

const key = String(args.bed || "a").toLowerCase();

// Bed P is generated locally instead of through Flow Music — numpy and scipy, no API,
// no credits, about 67x realtime. It is wired in behind the same --bed interface so
// publish.mjs and calendar.json need no change.
//
// FOCUS LANE ONLY, and that limit is the whole point. Its harmony is one four-chord
// progression on a 27-second cycle: ~270 passes across a two-hour focus video, ~1,300
// across a ten-hour sleep one. Measured against the Suno beds it is flatter (±1 dB over
// 90 minutes against 11.7 dB of swing), which suits work music — nothing swells up and
// takes your attention off the page — and is exactly wrong for sleep, where the
// breathing is part of why people leave it on all night. The sleep lane is 87% of the
// channel's genuine watch hours; it is not the place to save credits.
const PROCEDURAL = { name: "procedural focus (local, no credits)", mood: "calm" };
const bed = key === "p" ? PROCEDURAL : BEDS[key];
if (!bed) {
  console.error(`unknown --bed "${key}". Pick one of: ${Object.keys(BEDS).join(", ")}, p`);
  process.exit(1);
}

const minutes = Number(args.minutes || 120);
const takes = Number(args.takes || 16);
const tag = String(args.tag || key);
const root = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/beds";
const outPath = path.join(root, String(args.out || `bed-${tag}-${minutes}m.mp3`));
fs.mkdirSync(root, { recursive: true });

if (key === "p") {
  const { execFile } = await import("child_process");
  const { promisify } = await import("util");
  const execFileP = promisify(execFile);
  const kit = path.join(path.dirname(new URL(import.meta.url).pathname.replace(/%20/g, " ")),
                        "vendor", "procedural-audio");
  const wav = outPath.replace(/\.mp3$/, ".wav");
  console.log(`bed P — ${bed.name}   [mood: ${bed.mood}]`);
  console.log(`target ${minutes} min · no credits, generated locally`);
  console.log(`→ ${outPath}\n`);

  await execFileP("python3", [path.join(kit, "music.py"),
    "--mood", bed.mood, "--dur", String(minutes * 60), "--out", wav],
    { cwd: kit, maxBuffer: 1 << 26 });

  // music.py writes wav; the pipeline downstream expects mp3, same as Flow Music.
  await execFileP("ffmpeg", ["-y", "-v", "error", "-i", wav,
    "-c:a", "libmp3lame", "-b:a", "192k", outPath], { maxBuffer: 1 << 26 });
  fs.rmSync(wav, { force: true });          // the wav is ~10x the mp3 and disk is tight

  const { stdout } = await execFileP("ffprobe",
    ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", outPath]);
  const secs = parseFloat(stdout.trim()) || 0;
  console.log(`\n✅ ${(secs / 3600).toFixed(2)}h  generated locally, 0 credits`);
  console.log(`   ${outPath}`);
  process.exit(0);
}

const gens = Math.ceil(takes / 2);
console.log(`bed ${key.toUpperCase()} — ${bed.name}   [takes: ${tag}]`);
console.log(`target ${minutes} min from ${takes} takes (${gens} generations, ~${gens * 10} credits)`);
console.log(`→ ${outPath}\n`);

const r = await musicBed({
  prompt: bed.prompt.replace(/\s+/g, " ").trim(),
  minutes, takes, outPath,
  workDir: path.join(root, `${tag}-parts`),
});

console.log(`\n✅ ${(r.seconds / 3600).toFixed(2)}h  ${r.sources} sources, ${r.placements} placements`);
console.log(`   ${r.outPath}`);
