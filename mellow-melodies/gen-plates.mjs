#!/usr/bin/env node
/**
 * Build a library of loop-ready visual plates via Flow (Nano Banana Pro).
 *
 *   node gen-plates.mjs              # everything not already on disk
 *   node gen-plates.mjs session      # one pillar: session | market | sleep
 *
 * Stills are effectively unlimited on Ultra — only Veo image-to-video spends the Flow
 * credit pool, which is the scarce one. So generate the library now and animate from
 * it later as credits allow: each plate is a finished still that build-video.mjs can
 * drift over today, and a Veo first-frame the moment there is budget.
 *
 * Unlike PROMPTS.md's thumbnail plates, these are composed for FULL FRAME — nothing is
 * overlaid on them, so there is no keep-clear zone and they can be properly composed.
 */
import fs from "fs";
import path from "path";
import { loadEnv } from "../video-forge/lib/env.mjs";
import { flowImage } from "../video-forge/lib/flow.mjs";

loadEnv();

const OUT = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/loops/plates";
fs.mkdirSync(OUT, { recursive: true });

const BASE = `Cinematic photograph, shallow depth of field, nocturnal or low-light. Deep
near-black navy dominates, lit by a single warm amber source. Muted, restrained,
expensive. Calm and still. Rich enough to hold attention for hours without demanding it.
High quality, realistic, not illustrated, not a 3D render.

NO text, letters, numbers, signage, watermarks or logos. No screens showing charts,
candlesticks, graphs or trading terminals. No people, no faces, no hands. No neon, no
teal-and-orange grade, no lens flare.`;

const PLATES = {
  session: [
    ["desk-rain-window", `A wooden desk beneath a tall window at night, rain running down the
      glass, a single warm desk lamp lit. City lights soft and unfocused beyond. Quiet, enclosed.`],
    ["desk-library-lamp", `A dark study lined with old books, one brass lamp pooling warm light
      on a leather desktop. Deep shadow in the corners. Still and scholarly.`],
    ["rain-glass-macro", `Extreme close crop of rain beading and running down dark glass at
      night, warm amber light refracted through the droplets, everything beyond fully abstract.`],
    ["candle-desk", `A single candle burning on a dark wooden table, wax pooling, the flame
      steady. Everything beyond falls into deep shadow. Intimate and quiet.`],
    ["window-dawn-room", `An empty room before dawn seen from inside, one tall window admitting
      the first cold blue light, a warm lamp still burning in the corner.`],
  ],
  market: [
    ["skyline-predawn", `A city skyline in the last hour before dawn seen from high up, scattered
      warm window lights, low mist between towers, a thin band of orange on the horizon.`],
    ["skyline-fog-roll", `A dense sea of low cloud rolling between city towers at first light,
      only the tallest buildings emerging. Blue and grey, one warm accent.`],
    ["harbour-night", `A still harbour at night, dark water mirroring a distant line of warm
      city lights, no boats moving, long calm reflections.`],
    ["bridge-mist", `A long suspension bridge at dawn half-buried in mist, warm lamps receding
      into the distance, water flat and grey below.`],
    ["rooftop-dusk", `An empty rooftop at blue hour overlooking a vast city, one warm light
      fitting glowing nearby, clouds moving slowly overhead.`],
  ],
  sleep: [
    ["lake-night", `A perfectly still lake at night under low cloud, a single warm point of light
      on the far shore reflected in the water. Almost monochrome deep blue-black.`],
    ["forest-moonlight", `An ancient forest at night, thin moonlight falling between tall trunks,
      low mist across the forest floor, one warm glow deep among the trees.`],
    ["fireplace-embers", `A slow-burning fire reduced to glowing embers in a stone hearth, deep
      warm amber against near-black. Nothing else in frame.`],
    ["snow-window-night", `Snow falling steadily past a dark window at night, a warm interior
      light spilling faintly onto the sill. Silent and soft.`],
    ["night-sky-clouds", `A deep night sky with slow thin cloud drifting across a scatter of
      stars, the faintest warm glow along the lower horizon. No moon disc.`],
    ["ocean-longexposure", `A calm dark ocean at night under heavy cloud, long-exposure water
      smoothed to soft texture, one distant warm light on the horizon.`],
  ],
};

const want = process.argv[2];
const groups = want ? { [want]: PLATES[want] } : PLATES;
if (want && !PLATES[want]) {
  console.error(`unknown pillar "${want}" — pick from: ${Object.keys(PLATES).join(", ")}`);
  process.exit(1);
}

let made = 0, skipped = 0, failed = 0;
for (const [pillar, items] of Object.entries(groups)) {
  console.log(`\n── ${pillar} ──`);
  for (const [name, idea] of items) {
    const out = path.join(OUT, `${pillar}-${name}.png`);
    if (fs.existsSync(out)) { console.log(`${name} … cached`); skipped++; continue; }
    process.stdout.write(`${name} … `);
    try {
      await flowImage(`${BASE}\n\n${idea.replace(/\s+/g, " ").trim()}`, out, { aspectRatio: "16:9" });
      console.log("ok");
      made++;
    } catch (e) {
      console.log(`failed: ${e.message.slice(0, 120)}`);
      failed++;
    }
  }
}
console.log(`\n${made} new, ${skipped} cached, ${failed} failed → ${OUT}`);
