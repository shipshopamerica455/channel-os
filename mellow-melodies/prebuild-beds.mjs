#!/usr/bin/env node
/**
 * Bank every missing music bed in the calendar, in one go.
 *
 *   node prebuild-beds.mjs            # plan only
 *   node prebuild-beds.mjs --go       # generate them
 *   node prebuild-beds.mjs --go --only w2sun,w3tue
 *
 * Why this exists: Flow Music authenticates with a SINGLE-USE refresh token that useapi
 * rotates on every call. Anything that touches flowmusic.app in a browser consumes it
 * and the chain breaks — "refresh_token_already_used" — with no way for us to renew it.
 * It broke once already and silently killed a scheduled build overnight.
 *
 * Generating beds at build time therefore makes a fragile credential a hard dependency
 * of every upload. Generating them ahead of time makes it a soft one: if the link dies,
 * the scheduler keeps shipping from banked audio and you re-link at leisure.
 *
 * Run this whenever the link is known-good. Beds are cached by slot, so re-running only
 * fills gaps and costs nothing for what already exists.
 */
import fs from "fs";
import path from "path";
import { execFile } from "child_process";
import { promisify } from "util";
import { fileURLToPath } from "url";

const execFileP = promisify(execFile);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CHANNEL = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES";
const CAL = path.join(__dirname, "calendar.json");
const NODE = process.execPath;

const args = {};
for (let i = 2; i < process.argv.length; i++) {
  if (process.argv[i].startsWith("--")) {
    const k = process.argv[i].slice(2), n = process.argv[i + 1];
    args[k] = n && !n.startsWith("--") ? process.argv[++i] : true;
  }
}

const cal = JSON.parse(fs.readFileSync(CAL, "utf8"));
const only = args.only ? String(args.only).split(",").map((s) => s.trim()) : null;

const pending = Object.entries(cal).filter(([slot, s]) => {
  if (slot.startsWith("_")) return false;
  if (only && !only.includes(slot)) return false;
  if (s.published && s.published !== "pending") return false;
  return !fs.existsSync(path.join(CHANNEL, "beds", `${slot}.mp3`));
});

if (!pending.length) {
  console.log("Every unpublished slot already has a bed. Nothing to do.");
  process.exit(0);
}

const totalMin = pending.reduce((n, [, s]) => n + s.minutes, 0);
const totalTakes = pending.reduce((n, [, s]) => n + s.takes, 0);
console.log(`${pending.length} beds to bank — ${(totalMin / 60).toFixed(1)}h of audio, ` +
            `~${totalTakes} takes, ~${Math.ceil(totalTakes / 2) * 10} credits\n`);
for (const [slot, s] of pending) {
  console.log(`  ${slot.padEnd(7)} bed ${s.bed.toUpperCase()}  ${String(s.minutes).padStart(4)}min  ${s.takes} takes   ${s.title.slice(0, 44)}`);
}

if (!args.go) { console.log(`\nPlan only — add --go to generate.`); process.exit(0); }

// Sequential, not parallel: useapi caps concurrent jobs per account (maxJobs 8) and a
// burst of long generations is the surest way to trip the rate limiter mid-batch.
let done = 0, failed = [];
for (const [slot, s] of pending) {
  console.log(`\n── ${slot} ─────────────────────────────────`);
  try {
    await execFileP(NODE, ["gen-bed.mjs", "--bed", s.bed, "--tag", s.tag,
      "--minutes", String(s.minutes), "--takes", String(s.takes),
      "--out", `${slot}.mp3`], { cwd: __dirname, maxBuffer: 1 << 28 })
      .then((r) => process.stdout.write(r.stdout.split("\n").slice(-3).join("\n")));
    done++;
  } catch (e) {
    const broken = /refresh_token_already_used|refresh chain broken/.test(e.message);
    console.error(`  FAILED${broken ? " — Flow Music link is broken" : ""}: ${e.message.slice(0, 160)}`);
    failed.push(slot);
    if (broken) {
      console.error(`\n  Stopping: every remaining bed would fail the same way.\n` +
        `  Re-link with:  cd ../video-forge && node scripts/flowmusic-link.mjs`);
      break;
    }
  }
}

console.log(`\n${done} banked${failed.length ? `, ${failed.length} failed (${failed.join(", ")})` : ""}`);
