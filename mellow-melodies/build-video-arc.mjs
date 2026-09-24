#!/usr/bin/env node
/**
 * Assemble a DAY-ARC video: the visual moves through the session rather than looping.
 *
 *   node build-video-arc.mjs --audio beds/w2tue.mp3 --out "NYSE Session 6.5h.mp4"
 *
 *   --audio   the bed (required)
 *   --out     output filename inside the channel folder
 *   --arc     folder of ordered stage clips (default loops/arc)
 *   --xfade   crossfade between stages, seconds (default 6)
 *
 * Stage clips are the numbered mp4s in the arc folder (1-premarket, 2-open, …). Each
 * one covers an equal share of the runtime, so a 6h30m video over 6 stages spends ~65
 * minutes in each — dark before the open, bright by mid-morning, dusk at the close.
 *
 * The cost model is the same as build-video.mjs: encode short, copy long. Each stage is
 * palindromed once into a seamless cycle, then stream-looped to fill its share with
 * `-c:v copy`. Only the few seconds of crossfade between stages are ever re-encoded, so
 * a 6.5-hour arc costs about as much CPU as a 60-second one.
 */
import fs from "fs";
import path from "path";
import { execFile } from "child_process";
import { promisify } from "util";

const execFileP = promisify(execFile);
const CHANNEL = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES";

const args = {};
for (let i = 2; i < process.argv.length; i++) {
  if (process.argv[i].startsWith("--")) {
    const k = process.argv[i].slice(2), n = process.argv[i + 1];
    args[k] = n && !n.startsWith("--") ? process.argv[++i] : true;
  }
}

if (!args.audio) {
  console.error("usage: node build-video-arc.mjs --audio <bed.mp3> [--out name.mp4] [--arc loops/arc] [--xfade 6]");
  process.exit(1);
}

const resolve = (p) => (path.isAbsolute(p) ? p : path.join(CHANNEL, p));
const audio = resolve(String(args.audio));
const out = resolve(String(args.out || "arc-output.mp4"));
const arcDir = resolve(String(args.arc || "loops/arc"));
const xfade = Number(args.xfade || 6);

if (!fs.existsSync(audio)) { console.error(`no such audio: ${audio}`); process.exit(1); }

const stages = fs.readdirSync(arcDir).filter((f) => f.endsWith(".mp4")).sort()
  .map((f) => path.join(arcDir, f));
if (stages.length < 2) {
  console.error(`need at least 2 stage clips in ${arcDir} — found ${stages.length}`);
  process.exit(1);
}

const work = path.join(CHANNEL, ".arc-work");
fs.mkdirSync(work, { recursive: true });

const durationOf = async (f) => {
  const { stdout } = await execFileP("ffprobe", ["-v", "error", "-show_entries",
    "format=duration", "-of", "csv=p=0", f]);
  return parseFloat(stdout.trim()) || 0;
};
// Same reasoning as build-video.mjs: the cycles and crossfades here are stills and
// slow drifts, CRF 20 was archival overkill, and YouTube re-encodes the upload anyway.
const CRF = "26";

const ff = (a) => execFileP("ffmpeg", ["-y", "-v", "error", ...a], { maxBuffer: 1 << 28 });

/**
 * Intermediates are cached by filename, and this work dir is shared by every arc build.
 * An ffmpeg killed mid-write — a full disk, a sleeping machine — leaves a truncated
 * cycle or segment behind, and `existsSync` reuses it on the next run: the build "succeeds"
 * and quietly emits a short arc. That shipped a 4-hour video under an 8-hour title.
 * Probe the cache instead; anything that will not play is rebuilt.
 */
const usable = async (f) => {
  if (!fs.existsSync(f)) return false;
  try { return (await durationOf(f)) > 0; } catch { return false; }
};

const total = await durationOf(audio);
const per = total / stages.length;
console.log(`audio  : ${(total / 3600).toFixed(2)}h`);
console.log(`stages : ${stages.length} × ${(per / 60).toFixed(1)}min  (${path.basename(arcDir)})`);

// 1. palindrome each stage into a seamless cycle — encoded once
const cycles = [];
for (const [i, src] of stages.entries()) {
  const cyc = path.join(work, `cycle-${i}.mp4`);
  if (!await usable(cyc)) {
    process.stdout.write(`  cycle ${i + 1}/${stages.length} … `);
    await ff(["-i", src, "-filter_complex",
      "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=24,split[a][b];" +
      "[b]reverse[r];[a][r]concat=n=2:v=1:a=0[v]",
      "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", CRF,
      "-pix_fmt", "yuv420p", cyc]);
    console.log("ok");
  }
  cycles.push(cyc);
}
const cycleDur = await durationOf(cycles[0]);

// 2. fill each stage's share by looping its cycle — copy, no re-encode.
//    Every stage but the last is shortened by the crossfade it hands into.
const parts = [];
for (const [i, cyc] of cycles.entries()) {
  const isLast = i === cycles.length - 1;
  const span = isLast ? per : per - xfade;
  const seg = path.join(work, `seg-${i}.mp4`);
  if (!await usable(seg)) {
    process.stdout.write(`  fill ${i + 1}/${cycles.length} (${(span / 60).toFixed(1)}min) … `);
    await ff(["-stream_loop", "-1", "-i", cyc, "-t", String(span.toFixed(3)),
      "-c:v", "copy", seg]);
    console.log("ok");
  }
  parts.push(seg);

  // 3. crossfade into the next stage — the only re-encoded video in the whole build
  if (!isLast) {
    const tr = path.join(work, `xf-${i}.mp4`);
    if (!await usable(tr)) {
      process.stdout.write(`  blend ${i + 1}→${i + 2} … `);
      await ff(["-ss", String(Math.max(cycleDur - xfade, 0).toFixed(3)), "-i", cyc,
        "-t", String(xfade), "-i", cycles[i + 1],
        "-filter_complex", `[0:v][1:v]xfade=transition=fade:duration=${xfade}:offset=0,fps=24[v]`,
        "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", CRF,
        "-pix_fmt", "yuv420p", "-t", String(xfade), tr]);
      console.log("ok");
    }
    parts.push(tr);
  }
}

// 4. concat the whole visual track, then mux the bed over it — both stream copies
const listFile = path.join(work, "arc.txt");
fs.writeFileSync(listFile, parts.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join("\n"));
const visual = path.join(work, "visual.mp4");
process.stdout.write(`  joining … `);
await ff(["-f", "concat", "-safe", "0", "-i", listFile, "-c:v", "copy", visual]);
console.log("ok");

process.stdout.write(`  muxing to ${(total / 3600).toFixed(2)}h … `);
await ff(["-i", visual, "-i", audio, "-map", "0:v", "-map", "1:a",
  "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
  "-movflags", "+faststart", out]);
console.log("ok");

/**
 * The mux uses -shortest, so a visual track that came up short silently trims the bed
 * instead of failing — the output looks fine and is simply the wrong length. Assert the
 * result matches the audio it was built from; a build that cannot honour the runtime
 * must fail loudly, before anything uploads it under a title naming that runtime.
 */
const got = await durationOf(out);
if (Math.abs(got - total) > 60) {
  console.error(`\n\u274c arc is ${(got / 3600).toFixed(2)}h but the bed is ${(total / 3600).toFixed(2)}h ` +
    `(${((got / total) * 100).toFixed(0)}% of it).`);
  console.error(`   Leaving ${work} in place for inspection; delete it to force a clean rebuild.`);
  process.exit(1);
}

fs.rmSync(work, { recursive: true, force: true });
const mb = (fs.statSync(out).size / 1048576).toFixed(0);
console.log(`\n✅ ${(total / 3600).toFixed(2)}h  ${mb} MB\n   ${out}`);
