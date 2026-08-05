#!/usr/bin/env node
/**
 * Day-arc plates and clips — the thing that puts this channel in its own lane.
 *
 * Everyone in this category loops one scene for six hours. The video is wallpaper and
 * it tells you nothing. This instead moves the visual THROUGH the session it is named
 * for: the NYSE video opens before dawn, lightens through the morning, sits flat at
 * midday, warms through the afternoon and closes at dusk.
 *
 * So the video becomes a clock. Glance up and you know roughly where you are in your
 * own session without checking anything. It pairs with the session-length titles —
 * a 6h30m video that IS the trading day, not a 6h30m loop.
 *
 *   node gen-arc.mjs --plates            # stills only (free)
 *   node gen-arc.mjs --animate 4         # Veo the first 4 stages (10 credits each)
 *
 * Veo credits replenish to 50/day, so animate in daily batches; plates cache and
 * stages already animated are skipped.
 */
import fs from "fs";
import path from "path";
import { loadEnv } from "../video-forge/lib/env.mjs";
import { flowImage, flowImageToVideo } from "../video-forge/lib/flow.mjs";

loadEnv();

const ROOT = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/loops/arc";
fs.mkdirSync(ROOT, { recursive: true });

const BASE = `Cinematic photograph from the SAME fixed high window in the SAME room, looking
out over the same city skyline. Identical camera position, identical framing, identical
foreground every time — only the light and weather change between images.

Rich and inviting, with strong contrast between warm practical light and cool daylight.
Real depth. Saturated colour, deep but never empty blacks. Must read clearly small.

NO text, letters, numbers, signage, watermarks or logos. No screens showing charts,
candlesticks or trading terminals. No people, no faces, no hands. No lens flare.`;

// Ordered through a trading day. Each stage is one plate and one Veo clip.
const STAGES = [
  ["1-premarket", `Deep blue pre-dawn. The city below is still lit with thousands of warm window
    lights, mist low between the towers, the sky black-blue with the faintest cold light on the
    horizon. A warm lamp glows inside the room.`],
  ["2-open", `Sunrise. A brilliant band of gold along the horizon burning into deep blue above,
    the towers catching the first warm light on their east faces, mist glowing. The interior lamp
    is still on but weaker against the daylight.`],
  ["3-morning", `Mid-morning. Clear cool daylight over the city, long soft shadows between the
    towers, the sky a clean pale blue, glass catching bright reflections. The interior lamp is off.`],
  ["4-midday", `Midday under high overcast. Flat even silver light, the city detailed and open,
    the sky bright white-grey, shadows almost gone. Calm and neutral.`],
  ["5-afternoon", `Late afternoon. Low warm gold light raking across the towers from the far side,
    long shadows stretching between buildings, the sky warming towards amber at the horizon.`],
  ["6-close", `Dusk just after sunset. Deep blue settling over the city, the last orange band
    dying on the horizon, window lights coming on across the towers, the interior lamp lit again.`],
];

const args = {};
for (let i = 2; i < process.argv.length; i++) {
  if (process.argv[i].startsWith("--")) {
    const k = process.argv[i].slice(2), n = process.argv[i + 1];
    args[k] = n && !n.startsWith("--") ? process.argv[++i] : true;
  }
}

// ── plates (free) ────────────────────────────────────────────────────────────
if (args.plates || !args.animate) {
  console.log("── plates ──");
  for (const [name, idea] of STAGES) {
    const out = path.join(ROOT, `${name}.png`);
    if (fs.existsSync(out)) { console.log(`${name} … cached`); continue; }
    process.stdout.write(`${name} … `);
    try {
      await flowImage(`${BASE}\n\n${idea.replace(/\s+/g, " ").trim()}`, out, { aspectRatio: "16:9" });
      console.log("ok");
    } catch (e) { console.log(`failed: ${e.message.slice(0, 120)}`); }
  }
}

// ── clips (10 credits each) ──────────────────────────────────────────────────
if (args.animate) {
  const budget = Number(args.animate) || 4;
  console.log(`\n── clips (up to ${budget}, ~${budget * 10} credits) ──`);
  let spent = 0;
  for (const [name] of STAGES) {
    if (spent >= budget) break;
    const img = path.join(ROOT, `${name}.png`);
    const out = path.join(ROOT, `${name}.mp4`);
    if (!fs.existsSync(img)) { console.log(`${name} … no plate, skipping`); continue; }
    if (fs.existsSync(out)) { console.log(`${name} … cached`); continue; }
    process.stdout.write(`${name} … `);
    try {
      await flowImageToVideo({
        imagePath: img,
        // Weather and light only. A moving camera would break the illusion that these
        // are six views of one continuous day from one fixed window.
        prompt: `Only the sky and light change. Clouds and mist drift very slowly across the
          city. Window lights flicker almost imperceptibly. The camera is completely locked off
          and does not move, pan, zoom or drift at all. No people, no vehicles, no birds.`
          .replace(/\s+/g, " ").trim(),
        duration: 8, aspectRatio: "16:9", outPath: out,
      });
      console.log("ok");
      spent++;
    } catch (e) { console.log(`failed: ${e.message.slice(0, 140)}`); }
  }
  console.log(`\n${spent} clips generated (~${spent * 10} credits)`);
}

console.log(`\n→ ${ROOT}`);
