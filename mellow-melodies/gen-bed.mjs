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
const bed = BEDS[key];
if (!bed) {
  console.error(`unknown --bed "${key}". Pick one of: ${Object.keys(BEDS).join(", ")}`);
  process.exit(1);
}

const minutes = Number(args.minutes || 120);
const takes = Number(args.takes || 16);
const tag = String(args.tag || key);
const root = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/beds";
const outPath = path.join(root, String(args.out || `bed-${tag}-${minutes}m.mp3`));
fs.mkdirSync(root, { recursive: true });

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
