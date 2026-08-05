#!/usr/bin/env node
/**
 * Thumbnail plates — generated for CONTRAST, not for taste.
 *
 * The channel's video plates are prompted "muted, restrained, expensive… deep near-black
 * navy dominates". That is the right direction for something playing behind six hours of
 * work, and the wrong one for a 200px tile competing in a feed. Austere reads as empty at
 * thumbnail size, and dark is the first thing lost.
 *
 * So these are prompted for the opposite: strong warm/cool contrast — amber practical
 * light against deep blue night — with visible glow, real depth, and somewhere a viewer
 * actively wants to be. Cosy rather than severe.
 *
 * Composition keeps the LEFT THIRD dark and simple, because thumbs_v2.py puts the type
 * there behind a gradient. The subject sits right of centre.
 *
 *   node gen-thumb-plates.mjs           # all
 *   node gen-thumb-plates.mjs deepwork  # one
 */
import fs from "fs";
import path from "path";
import { loadEnv } from "../video-forge/lib/env.mjs";
import { flowImage } from "../video-forge/lib/flow.mjs";

loadEnv();

const OUT = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/brand/thumb-plates";
fs.mkdirSync(OUT, { recursive: true });

const BASE = `Cinematic photograph at night, RICH and INVITING, not austere. The image is
built on a strong contrast between WARM AMBER practical light — lamps, candles, fire,
window glow — and a DEEP BLUE night. The warm sources actually glow and bloom softly.

Real depth: something in the foreground, a clear lit subject in the middle, and a soft
glowing background. Colour is saturated and full, blacks are deep but never empty, and
the lit areas are genuinely bright. It must still read clearly when shrunk to 200 pixels
wide, so keep contrast high and the composition simple.

Somewhere a person would actively want to be: warm, calm, expensive, inviting.

COMPOSITION: the LEFT THIRD of the frame stays darker and visually simple — large text
goes there. The lit subject sits right of centre.

NO text, letters, numbers, signage, watermarks or logos. No screens showing charts,
candlesticks or trading terminals. No people, no faces, no hands. No lens flare.`;

const PLATES = {
  deepwork: [
    ["a-desk-glow", `A handsome dark wood desk by a tall window at night. A brass lamp with a warm
      glowing shade throws a strong pool of amber light across the desktop and an open notebook.
      Beyond the rain-flecked glass, a deep blue city glitters softly out of focus.`],
    ["b-library-fire", `A private library at night: floor-to-ceiling books in warm shadow, a fire
      glowing amber in a stone hearth to the right, a deep leather armchair catching the light.
      Blue moonlight falls through a tall window on the left.`],
    ["c-cafe-window", `A quiet corner table in a warm-lit café at night seen from inside, a small
      glowing lamp and a cup on the table, big windows showing a deep blue rainy street with
      soft bokeh lights beyond.`],
  ],
  market: [
    ["a-skyline-goldblue", `A city skyline from a high window in the last minutes before sunrise.
      A brilliant band of warm gold along the horizon against a deep blue sky, thousands of tiny
      warm window lights in the towers below, low mist catching the light.`],
    ["b-window-desk-city", `A dark room high above a city at night. A warm amber lamp glowing on a
      desk in the right foreground, floor-to-ceiling glass behind it showing a vast deep blue
      cityscape glittering with warm lights far below.`],
  ],
  // The legacy catalogue is all morning/Bach content, so the night plates above are
  // simply wrong for it. Same contrast principle, different key: low golden sun against
  // cool shadow instead of lamplight against night.
  morning: [
    ["a-desk-sunrise", `A wooden writing desk by a tall window at sunrise. Low golden light floods
      across the desk, an open book and a cup catching it, long soft shadows. The room's left side
      is still in cool blue morning shadow.`],
    ["b-coffee-window", `A cup of coffee steaming on a windowsill in early morning light, golden sun
      flaring softly through the glass, a garden green and cool beyond. Warm, quiet, unhurried.`],
    ["c-garden-path", `A formal garden path at sunrise, clipped hedges and stone urns, low golden
      light raking across the gravel, long shadows, cool blue mist at the far end.`],
    ["d-spring-blossom", `Spring blossom on a branch backlit by low golden morning sun, petals glowing
      translucent, the background a soft cool green blur. Fresh and luminous.`],
    ["e-forest-path", `A path through tall trees at sunrise, shafts of golden light cutting through
      morning mist between the trunks, cool blue-green shadow beneath. Still and clear.`],
    ["f-fountain-courtyard", `A stone fountain in an old courtyard at early morning, water catching
      golden light, warm stone walls, deep cool shadow along the left side.`],
  ],
  // An INSTRUMENT has to be in frame on the sleep tiles. The first sleep thumbnail was
  // a fireplace, and YouTube duly filed the video next to "Rainy Night in a Cozy Cabin"
  // and other fireplace-ambience channels — 92% suggested traffic, 1.3% CTR, and viewers
  // arriving expecting crackle and getting baroque strings. The plate has to promise
  // music, not room tone.
  sleepmusic: [
    ["a-piano-moonlight", `A grand piano in a dark room at night, its lid raised, cool blue
      moonlight falling across the keys from a tall window behind. One small warm lamp glowing
      softly at the edge of the frame. Still, elegant, quiet.`],
    ["b-piano-keys-lamp", `Close on the keys of an old piano lit by a single warm lamp, the rest
      of the room falling into deep blue darkness, sheet music just out of focus. Intimate.`],
    ["c-cello-window", `A cello resting on its stand beside a tall window at night, deep blue
      moonlight on its varnish, a warm lamp glowing low behind it. Calm and unhurried.`],
  ],
  sleep: [
    ["a-embers-hearth", `A stone hearth filled with glowing amber embers and low flame, radiating
      warm light into a dark blue room. A soft blanket and cushion catch the glow on the right.
      Deep, cosy, enveloping.`],
    ["b-cabin-snow", `A warm-lit wooden cabin window seen from just outside at night, golden light
      spilling out onto deep blue snow, heavy snowflakes falling, dark pines behind.`],
    ["c-lake-moon-cabin", `A still lake at night under a deep blue sky, a small cabin on the far
      shore with warm golden windows, its light making a long reflection across the black water.`],
  ],
};

const want = process.argv[2];
const groups = want ? { [want]: PLATES[want] } : PLATES;
if (want && !PLATES[want]) {
  console.error(`unknown group "${want}" — pick from: ${Object.keys(PLATES).join(", ")}`);
  process.exit(1);
}

let made = 0;
for (const [group, items] of Object.entries(groups)) {
  console.log(`\n── ${group} ──`);
  for (const [name, idea] of items) {
    const out = path.join(OUT, `${group}-${name}.png`);
    if (fs.existsSync(out)) { console.log(`${name} … cached`); continue; }
    process.stdout.write(`${name} … `);
    try {
      await flowImage(`${BASE}\n\n${idea.replace(/\s+/g, " ").trim()}`, out, { aspectRatio: "16:9" });
      console.log("ok");
      made++;
    } catch (e) {
      console.log(`failed: ${e.message.slice(0, 120)}`);
    }
  }
}
console.log(`\n${made} generated → ${OUT}`);
