#!/usr/bin/env node
/**
 * Animate brand plates into Veo clips (Google Flow) for use as video loops.
 *
 *   node gen-veo.mjs                 # all scenes
 *   node gen-veo.mjs skyline         # one scene
 *
 * Motion is deliberately near-nil. These play for hours behind someone's work; any
 * camera move noticeable once is unbearable by the fortieth repetition. The prompts
 * therefore describe what moves *within* the frame and explicitly pin the camera.
 *
 * Veo caps at 8s here, so clips get palindromed into a seamless cycle by
 * build-video.mjs rather than being generated long.
 */
import fs from "fs";
import path from "path";
import { loadEnv } from "../video-forge/lib/env.mjs";
import { flowImageToVideo } from "../video-forge/lib/flow.mjs";

loadEnv();

const CHANNEL = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES";
const PLATES = path.join(CHANNEL, "LOGO REBRAND ASSETS");
const OUT = path.join(CHANNEL, "loops");
fs.mkdirSync(OUT, { recursive: true });

const SCENES = {
  skyline: {
    image: "d39eb5f5-80ee-4feb-9f30-5af25ea25aaf.png",
    prompt: `The city lights twinkle almost imperceptibly. Low mist drifts very slowly across
      the buildings. The sky brightens by the faintest amount. The camera does not move at all.
      Extremely subtle, calm, no action, no people, no vehicles.`,
  },
  hall: {
    image: "add32068-2483-43b7-ae71-d2877eaa0cc5.png",
    prompt: `Dust drifts slowly through the single beam of stage light. The light flickers by a
      barely perceptible amount. Everything else is completely still. The camera does not move
      at all. No people, no motion in the seats.`,
  },
  desk: {
    image: "200e805e-4bc9-401c-85cb-6080046e2078.png",
    prompt: `The lamp light wavers by the faintest amount and dust drifts slowly through it. The
      city lights beyond the window twinkle very slightly. Nothing else moves. The camera does
      not move at all. No people, no hands.`,
  },
  line: {
    image: "d4a1a3cb-605a-4c8d-aaa0-19b076af009d.png",
    prompt: `The band of warm light pulses very slowly and gently, brightening and dimming by a
      small amount, with a faint shimmer along its length. The background stays pure darkness.
      The camera does not move at all.`,
  },
};

const want = process.argv[2];
const scenes = want ? { [want]: SCENES[want] } : SCENES;
if (want && !SCENES[want]) {
  console.error(`unknown scene "${want}" — pick from: ${Object.keys(SCENES).join(", ")}`);
  process.exit(1);
}

for (const [name, s] of Object.entries(scenes)) {
  const outPath = path.join(OUT, `${name}.mp4`);
  if (fs.existsSync(outPath)) { console.log(`${name} … cached`); continue; }
  process.stdout.write(`${name} … `);
  try {
    await flowImageToVideo({
      imagePath: path.join(PLATES, s.image),
      prompt: s.prompt.replace(/\s+/g, " ").trim(),
      duration: 8,
      aspectRatio: "16:9",
      outPath,
    });
    console.log(`ok → ${path.basename(outPath)}`);
  } catch (e) {
    console.log(`failed: ${e.message.slice(0, 200)}`);
  }
}
console.log(`\n→ ${OUT}`);
