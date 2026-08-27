#!/usr/bin/env node
/**
 * Cover plates — the A/B challenger to the thumb-plates the channel ships today.
 *
 * The case for trying something else is in the CTR. Every thumbnail built on
 * thumb-plates + thumbs_v3.py sits between 0.5% and 2.3%, across roughly 28,000
 * impressions and fifteen videos. That is a real sample and it is a poor number;
 * ambient channels of this kind run several times higher. The catalogue is being
 * shown and not clicked.
 *
 * The one thumbnail on the channel that clicks well — 6.7%, though on only four
 * clicks, so treat it as a lead and not a finding — is "Moonlit Reflections Vol 2",
 * made before the relaunch. It is an album cover: a composer at a piano by
 * moonlight, gold serif type, the whole frame a scene you look into.
 *
 * The current plates cannot produce that image, by construction. Their prompt ends
 * "No people, no faces, no hands", and reserves the left third as an empty dark
 * panel for a duration label to sit on. The result reads as a utility banner —
 * accurate about the runtime, silent about the music.
 *
 * So these plates invert both rules:
 *
 *   · A PERSON is the subject — a musician mid-performance, seen in the room.
 *     Faces are the oldest lever in thumbnail design and the current system
 *     forbids them.
 *   · The composition is CENTRED and full-bleed, because the type that goes on
 *     top is a title, not a label — no dead panel to reserve.
 *
 * These are a hypothesis under test, not a replacement. Keep gen-thumb-plates.mjs
 * shipping the current look until Studio's Test & compare returns a verdict.
 *
 *   node gen-cover-plates.mjs          # all
 *   node gen-cover-plates.mjs sleep    # one group
 */
import fs from "fs";
import path from "path";
import { loadEnv } from "../video-forge/lib/env.mjs";
import { flowImage } from "../video-forge/lib/flow.mjs";

loadEnv();

const OUT = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES/brand/cover-plates";
fs.mkdirSync(OUT, { recursive: true });

const BASE = `Painterly cinematic image in the style of a classical music album cover.
Rich, warm and inviting, with real depth and glow — amber candlelight and lamplight
against a deep blue night. Old master painting quality: golden light modelling the
face and hands, deep shadow elsewhere, saturated colour, visible brushwork feel.

The subject is a MUSICIAN, shown playing, absorbed in the music and not looking at
the camera. The face is clearly lit and readable. This is the focal point.

COMPOSITION: subject centred, full bleed to all edges, framed so the upper fifth and
lower fifth of the image stay simple enough for a title to sit over them. It must
read at 200 pixels wide, so keep one clear subject and strong contrast.

NO text, letters, numbers, signage, watermarks or logos. No modern clothing, no
screens, no instruments held incorrectly. No lens flare.`;

const PLATES = {
  sleep: [
    ["a-pianist-moonlight", `An 18th-century composer in a dark velvet coat playing a grand piano
      by moonlight in an ornate candlelit room. Tall arched window behind showing a full moon over
      a formal garden. Candelabra glowing warm gold on the piano. He is absorbed, head slightly
      bowed, hands on the keys.`],
    ["b-cellist-window", `A cellist playing alone in a warm candlelit room at night, deep blue
      moonlight through a tall window behind her, the cello's varnish catching gold light. Eyes
      closed, mid-phrase, bow drawn across the strings.`],
    ["c-pianist-firelight", `A pianist at an upright piano in a panelled room, firelight from a
      hearth to one side throwing warm amber across his face and hands, the rest of the room deep
      blue shadow. Sheet music lit by a single candle.`],
    // Same subject, pushed right of centre. The current type system reserves the left
    // third for a duration label, and over a centred plate that label lands on the
    // face — which would make the A/B a test of covering a face rather than of the
    // artwork. This plate lets the current type keep its layout and still be judged
    // fairly against the new one.
    ["d-pianist-moonlight-right", `An 18th-century composer in a dark velvet coat playing a grand
      piano by moonlight in an ornate candlelit room, positioned in the RIGHT HALF of the frame.
      The LEFT THIRD of the image is quiet, darker room — panelling and deep shadow, no subject.
      Candelabra glowing warm gold on the piano, tall moonlit window behind him.`],
  ],
  focus: [
    ["a-violinist-library", `A violinist playing in a candlelit private library at night,
      floor-to-ceiling books in warm shadow behind, gold light on her face and the violin's
      scroll. Focused, mid-phrase.`],
    ["b-harpsichord-study", `A baroque musician at a harpsichord in a candlelit study, quill and
      manuscript on the desk beside, warm gold candlelight on his hands and face, deep blue night
      through a leaded window.`],
  ],
};

const want = process.argv[2];
const groups = want ? { [want]: PLATES[want] } : PLATES;
if (want && !PLATES[want]) {
  console.error(`unknown group "${want}" — pick from: ${Object.keys(PLATES).join(", ")}`);
  process.exit(1);
}

let made = 0, skipped = 0;
for (const [group, items] of Object.entries(groups)) {
  console.log(`\n── ${group} ──`);
  for (const [name, idea] of items) {
    const out = path.join(OUT, `${group}-${name}.png`);
    if (fs.existsSync(out)) { console.log(`  ${name} … exists, skipped`); skipped++; continue; }
    process.stdout.write(`  ${name} … `);
    try {
      await flowImage(`${idea.replace(/\s+/g, " ").trim()}\n\n${BASE}`, out, { aspectRatio: "16:9" });
      console.log("ok");
      made++;
    } catch (e) {
      console.log(`FAILED — ${e.message.slice(0, 110)}`);
    }
  }
}
console.log(`\n${made} generated, ${skipped} already present → ${OUT}`);
