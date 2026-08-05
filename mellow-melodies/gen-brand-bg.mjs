#!/usr/bin/env node
/**
 * Brand backgrounds via Flow (Nano Banana Pro). Prompts mirror PROMPTS.md.
 *
 * Flow supplies depth and atmosphere; all type is drawn in code by build_brand.py,
 * because image models garble rendered lettering and a misspelled channel name on a
 * banner is unrecoverable. Prompts therefore keep the region under the type dark and
 * empty, and forbid text outright.
 *
 *   node gen-brand-bg.mjs              # everything
 *   node gen-brand-bg.mjs banner       # one group: banner | logo | thumb
 */
import fs from "fs";
import path from "path";
import { loadEnv } from "../video-forge/lib/env.mjs";
import { flowImage } from "../video-forge/lib/flow.mjs";

loadEnv();

const OUT = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/brand/bg";
fs.mkdirSync(OUT, { recursive: true });

const BASE = `Cinematic photograph, shallow depth of field, nocturnal. Deep near-black navy
(#0E1420) dominates the frame, lit by a single warm amber light source (#E0A340).
Muted, restrained, expensive. Calm and still — nothing urgent, nothing dramatic.
High quality, realistic, not illustrated, not a 3D render.

NO text, letters, numbers, words, signage, watermarks or logos anywhere in the image.
No screens showing charts, candlesticks, graphs, tickers or trading terminals. No faces
looking at camera, no posed people, no stock-photo styling. No neon, no teal-and-orange
grade, no lens flare.`;

// Keep-clear instruction for anything that gets type composited over it.
const CLEAR_CENTRE = `CRITICAL COMPOSITION: the central horizontal third of the frame must be
dark, plain and almost empty — deep shadow, minimal detail — because large text will be
placed across it. Visual interest belongs at the top and bottom edges only.`;

const GROUPS = {
  banner: [
    ["banner-bg", "16:9",
     `A city seen from a high window in the last hour before dawn. Deep blue-black sky, a
      scatter of small warm window lights far below, low mist between the buildings. Shot
      from inside a dark room so the lower and upper edges fall into heavy shadow.\n\n${CLEAR_CENTRE}`],
    ["banner-bg-alt", "16:9",
     `A grand concert hall at night, empty, seen from the rear of the stalls. Rows of seats
      falling away into darkness, a single warm amber work-light burning on the far stage.
      Dust in the beam. Vast, silent, still.\n\n${CLEAR_CENTRE}`],
  ],
  logo: [
    ["logo-concept-a-steady-line", "1:1",
     `A single horizontal band of warm amber light stretched across a deep near-black field,
      perfectly level and even, softly blurred at both ends. Minimal, symmetrical, centred.
      Nothing else in the frame. Full-bleed dark background to the very edges.`],
    ["logo-concept-b-string", "1:1",
     `Extreme macro of a single piano string in deep shadow, lit by one warm amber highlight
      running along its length. Abstract, almost unreadable as an object. Centred and
      symmetrical, full-bleed dark background.`],
    ["logo-concept-c-arc", "1:1",
     `A slow warm amber arc of light curving through darkness, like a long exposure of a
      single moving point. Simple enough to read at thumbnail size. Centred, full-bleed
      near-black background.`],
  ],
  thumb: [
    ["thumb-bg-deepwork", "16:9",
     `A dark wooden desk lit by one warm amber lamp just out of frame. A closed notebook and
      a pen, deliberately out of focus. No screen, no monitor, no keyboard. Early hours,
      curtains drawn. The centre of the frame is empty desk surface in low light.\n\n${CLEAR_CENTRE}`],
    ["thumb-bg-session", "16:9",
     `Rain running down a tall window at night, a warm amber interior light reflected and
      smeared in the water. The city beyond is soft, dark and unfocused. Quiet and enclosed.
      The centre of the frame is the darkest, plainest area.\n\n${CLEAR_CENTRE}`],
    ["thumb-bg-sleep", "16:9",
     `A still lake at night under low cloud, a single warm point of light on the far shore
      reflected in the water. No moon disc, no stars, no drama. Almost monochrome deep
      blue-black. The centre of the frame is flat, calm water in shadow.\n\n${CLEAR_CENTRE}`],
  ],
};

const want = process.argv[2];
const groups = want ? { [want]: GROUPS[want] } : GROUPS;
if (want && !GROUPS[want]) {
  console.error(`unknown group "${want}" — pick one of: ${Object.keys(GROUPS).join(", ")}`);
  process.exit(1);
}

for (const [group, items] of Object.entries(groups)) {
  console.log(`\n── ${group} ──`);
  for (const [name, aspect, idea] of items) {
    process.stdout.write(`${name} … `);
    try {
      await flowImage(`${BASE}\n\n${idea}`, path.join(OUT, `${name}.png`), { aspectRatio: aspect });
      console.log("ok");
    } catch (e) {
      console.log(`failed: ${e.message.slice(0, 150)}`);
    }
  }
}
console.log(`\n→ ${OUT}`);
