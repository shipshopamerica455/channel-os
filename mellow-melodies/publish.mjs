#!/usr/bin/env node
/**
 * One command per video: music → visual → upload → publish.
 *
 *   node publish.mjs --slot w2tue           # dry run: shows the plan, changes nothing
 *   node publish.mjs --slot w2tue --go      # actually run it
 *   node publish.mjs --status               # what is done and what is pending
 *
 * Reads calendar.json. Every stage is RESUMABLE — a bed, video or take that already
 * exists on disk is reused, so a run that dies halfway (or a machine that sleeps
 * mid-upload) is fixed by running the same command again, not by starting over.
 *
 * Nothing publishes without --go. This uploads public video to a real channel; a typo
 * in a slot name should print a plan, not broadcast something.
 */
import fs from "fs";
import path from "path";
import { execFile, spawnSync } from "child_process";
import { promisify } from "util";
import { fileURLToPath } from "url";

const execFileP = promisify(execFile);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, "..");
const CHANNEL = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES";
const CAL = path.join(__dirname, "calendar.json");

const args = {};
for (let i = 2; i < process.argv.length; i++) {
  if (process.argv[i].startsWith("--")) {
    const k = process.argv[i].slice(2), n = process.argv[i + 1];
    args[k] = n && !n.startsWith("--") ? process.argv[++i] : true;
  }
}

// launchd runs with a minimal PATH that has no /opt/homebrew/bin, so a bare "node"
// spawn fails with ENOENT. process.execPath is the absolute binary already running us.
const NODE = process.execPath;

const cal = JSON.parse(fs.readFileSync(CAL, "utf8"));
const inChannel = (p) => (path.isAbsolute(p) ? p : path.join(CHANNEL, p));

/** Stream child output live AND capture it, so the upload's video id can be recovered. */
async function run(cmd, cmdArgs, cwd) {
  const p = execFileP(cmd, cmdArgs, { cwd, maxBuffer: 1 << 28 });
  let buf = "";
  p.child.stdout?.on("data", (d) => { buf += d; process.stdout.write(d); });
  p.child.stderr?.on("data", (d) => { buf += d; process.stderr.write(d); });
  await p;
  return buf;
}

/**
 * A file that exists is not a file that finished.
 *
 * Every stage writes its output in place, so an ffmpeg killed mid-render — a sleeping
 * machine, a cancelled batch — leaves a plausible mp4 with no moov atom. `existsSync`
 * reuses that forever, which means the slot can never recover on its own: it skips the
 * build, uploads a corrupt file, and the only fix is a human noticing and deleting it.
 * That is what happened to five slots. Probe instead — if it will not play, it is not a
 * build result, and the build re-runs (ffmpeg -y overwrites, so nothing is deleted here).
 */
function seconds(p) {
  if (!fs.existsSync(p)) return null;
  const r = spawnSync("ffprobe",
    ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
    { encoding: "utf8" });
  const d = parseFloat(r.stdout);
  return r.status === 0 && d > 0 ? d : null;
}
const finished = (p) => seconds(p) !== null;

/** Record the id in calendar.json so a re-run refuses to publish a duplicate. */
function recordPublished(slot, videoId) {
  const cal = JSON.parse(fs.readFileSync(CAL, "utf8"));
  cal[slot].published = videoId;
  fs.writeFileSync(CAL, JSON.stringify(cal, null, 2) + "\n");
}

/**
 * Refuse to publish when the words contradict the media.
 *
 * Three of these shipped or nearly shipped: a 3-hour thumbnail on a 90-minute video, a
 * "Black Screen" title over a fireplace loop, a thumbnail built for an entirely different
 * slot. The cause is structural, not carelessness — a slot's title, thumbnail and visual
 * are independent fields, so nothing forces them to agree, and every check is a human
 * remembering. These are the claims that are mechanically checkable; make the machine do it.
 */
function contradictions(slot, s) {
  const out = [];
  const title = s.title || "";
  const mins = Number(s.minutes) || 0;

  // "6.5 Hours", "90 Minutes", "10 Hours" in the title must match `minutes`
  const h = title.match(/(\d+(?:\.\d+)?)\s*hours?\b/i);
  const m = title.match(/(\d+)\s*minutes?\b/i);
  const claimed = h ? Math.round(parseFloat(h[1]) * 60) : m ? Number(m[1]) : null;
  if (claimed !== null && mins && Math.abs(claimed - mins) > 5) {
    out.push(`title claims ${claimed} min but calendar says ${mins} min`);
  }

  // A "black screen" promise is broken by any actual imagery
  if (/black\s*screen/i.test(title) && (s.visual?.image || s.visual?.clip || s.visual?.arc)) {
    out.push(`title promises "black screen" but a visual is set`);
  }

  // The thumbnail should belong to this slot, not one that happens to exist
  const thumb = path.basename(s.thumbnail || "");
  const th = thumb.match(/(\d+(?:\.\d+)?)h\b/i);
  if (th && mins && Math.abs(Math.round(parseFloat(th[1]) * 60) - mins) > 5) {
    out.push(`thumbnail "${thumb}" names a different length than ${mins} min`);
  }

  // The render must be as long as the title says. `minutes` is a claim in a JSON file;
  // the file on disk is the thing viewers get, and the two drifted once already — a
  // half-length arc uploaded under an "8 Hours" title because both said 480.
  const vid = path.join(CHANNEL, `${title.split(" \u2014 ")[0]}.mp4`);
  const secs = seconds(vid);

  // YouTube's ceiling is 12 hours, and it enforces it AFTER accepting the bytes: the
  // upload returns a video id, then the video quietly never appears. publish.mjs wrote
  // that id into calendar.json as a success and the slot looked done for a video that
  // did not exist. A 12-hour slot could never have worked \u2014 beds assemble a minute or
  // two long, so every render in the September run overran its target; only the one
  // sitting on the ceiling was killed by it.
  const LIMIT = 12 * 3600;
  if (secs !== null && secs >= LIMIT) {
    out.push(`render is ${(secs / 3600).toFixed(2)}h \u2014 YouTube's limit is 12h, and it ` +
             `accepts the upload then discards the video. Trim below 11h58m first.`);
  }
  if (mins * 60 >= LIMIT) {
    out.push(`slot targets ${(mins / 60).toFixed(2)}h \u2014 keep it under 12h, allowing a ` +
             `few minutes because beds assemble longer than their target`);
  }

  if (secs !== null && mins && Math.abs(secs / 60 - mins) > 5) {
    out.push(`render is ${(secs / 60).toFixed(0)} min but calendar/title say ${mins} min`);
  }

  // Every referenced file must exist — a missing plate fails late and expensively
  for (const [what, rel] of [["thumbnail", s.thumbnail],
                             ["visual image", s.visual?.image],
                             ["visual clip", s.visual?.clip]]) {
    if (rel && !fs.existsSync(inChannel(rel))) out.push(`${what} not found: ${rel}`);
  }
  return out;
}

// ── status ───────────────────────────────────────────────────────────────────
if (args.status) {
  console.log("slot     bed              video            published");
  for (const [slot, s] of Object.entries(cal)) {
    if (slot.startsWith("_")) continue;
    const bed = path.join(CHANNEL, "beds", `${slot}.mp3`);
    const vid = path.join(CHANNEL, `${s.title.split(" — ")[0]}.mp4`);
    console.log(
      slot.padEnd(9) +
      (finished(bed) ? "ok  " : fs.existsSync(bed) ? "partial" : "—   ").padEnd(17) +
      (finished(vid) ? "ok  " : fs.existsSync(vid) ? "partial" : "—   ").padEnd(17) +
      (s.published && s.published !== "pending" ? `https://youtu.be/${s.published}` : s.published || "—")
    );
  }
  process.exit(0);
}

/**
 * --next picks the earliest unpublished slot due within `--lead` days. That is what the
 * scheduler calls: it never needs to know which video is next, so adding a row to
 * calendar.json is the only thing required to queue another upload.
 */
let slot = args.slot;
if (args.next) {
  const lead = Number(args.lead || 2) * 86400_000;
  const due = Object.entries(cal)
    .filter(([k, v]) => !k.startsWith("_") && v.publishAt &&
      (!v.published || v.published === "pending") &&
      Date.parse(v.publishAt) - Date.now() < lead)
    .sort((a, b) => Date.parse(a[1].publishAt) - Date.parse(b[1].publishAt));
  if (!due.length) {
    console.log(`Nothing due within ${args.lead || 2} days. Nothing to do.`);
    process.exit(0);
  }
  slot = due[0][0];
}

const s = slot && cal[slot];
if (!s) {
  console.error(`--slot or --next required. Available: ${Object.keys(cal).filter(k => !k.startsWith("_")).join(", ")}`);
  process.exit(1);
}

const bedPath = path.join(CHANNEL, "beds", `${slot}.mp3`);
const videoPath = path.join(CHANNEL, `${s.title.split(" — ")[0]}.mp4`);
const GO = !!args.go;

console.log(`slot      ${slot}`);
console.log(`title     ${s.title}`);
console.log(`bed       ${s.bed.toUpperCase()} · ${s.minutes}min · ${s.takes} takes` +
            (finished(bedPath) ? "  [exists, will reuse]" : `  [~${Math.ceil(s.takes / 2) * 10} credits]`));
console.log(`visual    ${s.visual.arc ? "day arc" : s.visual.clip ? `clip ${s.visual.clip}` : `still ${path.basename(s.visual.image)}`}` +
            (finished(videoPath) ? "  [video exists, will reuse]" : fs.existsSync(videoPath) ? "  [unfinished file — will rebuild]" : ""));
console.log(`thumbnail ${path.basename(s.thumbnail)}`);
console.log(`publish   ${s.publishAt ? `scheduled ${s.publishAt}` : "immediately (no publishAt in calendar.json)"}`);
console.log(`published ${s.published && s.published !== "pending" ? s.published : "not yet"}`);

if (s.publishAt && Date.parse(s.publishAt) < Date.now()) {
  console.log(`\n⚠  publishAt is in the past — YouTube will publish immediately.`);
}

const problems = contradictions(slot, s);
if (problems.length) {
  console.error(`\n❌ ${problems.length} contradiction(s) in slot "${slot}":`);
  problems.forEach((p) => console.error(`   · ${p}`));
  console.error(`\n   Fix calendar.json, or pass --force to publish anyway.`);
  if (!args.force) process.exit(1);
  console.error(`   --force given; continuing.`);
} else if (!GO) {
  console.log(`\nchecks    ok — title, thumbnail and visual agree`);
}

if (!GO) { console.log(`\nDRY RUN — add --go to run it.`); process.exit(0); }
if (s.published && s.published !== "pending") {
  console.error(`\nAlready published as ${s.published}. Clear the "published" field in calendar.json to re-run.`);
  process.exit(1);
}

// ── 1. music ─────────────────────────────────────────────────────────────────
if (!finished(bedPath)) {
  console.log(`\n── bed ──`);
  await run(NODE, ["gen-bed.mjs", "--bed", s.bed, "--tag", s.tag,
    "--minutes", String(s.minutes), "--takes", String(s.takes),
    "--out", `${slot}.mp3`], __dirname);
} else console.log(`\n── bed ── reusing ${path.basename(bedPath)}`);

// ── 2. visual ────────────────────────────────────────────────────────────────
if (!finished(videoPath)) {
  console.log(`\n── video ──`);
  if (s.visual.arc) {
    await run(NODE, ["build-video-arc.mjs", "--audio", `beds/${slot}.mp3`,
      "--out", path.basename(videoPath)], __dirname);
  } else if (s.visual.clip) {
    await run(NODE, ["build-video.mjs", "--audio", `beds/${slot}.mp3`,
      "--clip", s.visual.clip, "--slow", String(s.visual.slow || 1),
      "--out", path.basename(videoPath)], __dirname);
  } else {
    await run(NODE, ["build-video.mjs", "--audio", `beds/${slot}.mp3`,
      "--image", s.visual.image, "--loop", String(s.visual.loop || 60),
      "--out", path.basename(videoPath)], __dirname);
  }
} else console.log(`\n── video ── reusing ${path.basename(videoPath)}`);

// ── 3. upload ────────────────────────────────────────────────────────────────
console.log(`\n── upload ──`);
const outLog = await run(NODE, ["mellow-upload.mjs", "--video", videoPath, "--slot", slot,
  ...(s.publishAt ? ["--at", s.publishAt] : ["--privacy", "public"])],
  path.join(REPO, "remotion-shorts"));

const id = (outLog.match(/youtu\.be\/([\w-]{11})/) || [])[1];
if (id) {
  recordPublished(slot, id);
  console.log(`\n✅ ${slot} → https://youtu.be/${id}  (recorded in calendar.json)`);
} else {
  console.error(`\n⚠  Upload finished but no video id was found in the output.\n` +
    `   calendar.json was NOT updated — set "${slot}".published by hand, or the next\n` +
    `   --next run will publish this slot a second time.`);
  process.exit(1);
}
