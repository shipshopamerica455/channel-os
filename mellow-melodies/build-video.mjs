#!/usr/bin/env node
/**
 * Assemble a long-form Mellow Melodies video: a seamless visual loop + a music bed.
 *
 *   node build-video.mjs --audio beds/deepwork-2h.mp3 --image <plate.png> \
 *     --out "Deep Work 2h.mp4"
 *
 *   --audio   the bed (required)
 *   --image   still to drift over  |  --clip  a video loop (e.g. Veo) instead
 *   --out     output filename inside the channel folder
 *   --loop    seconds per visual cycle (default 60)
 *
 * Why a loop rather than hours of unique video: a 2-hour 1080p encode is enormous and
 * slow, and nothing on screen changes anyway. So the visual is encoded ONCE as a short
 * seamless cycle, then repeated against the audio with `-c:v copy` — no re-encode, so a
 * 2-hour file builds in seconds instead of an hour and stays small.
 *
 * The still path drifts in for half the cycle and back out for the other half, ending
 * exactly where it started, so the repeat has no visible seam. Slowly enough that it
 * reads as breathing rather than motion — this plays for hours behind someone's work,
 * and any movement noticeable once is unbearable by the fortieth repetition.
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

if (!args.audio || (!args.image && !args.clip)) {
  console.error("usage: node build-video.mjs --audio <bed.mp3> (--image <still.png> | --clip <loop.mp4>) [--out name.mp4] [--loop 60]");
  process.exit(1);
}

const resolve = (p) => (path.isAbsolute(p) ? p : path.join(CHANNEL, p));
const audio = resolve(String(args.audio));
const out = resolve(String(args.out || "output.mp4"));
const loopSecs = Number(args.loop || 60);

// The whole video is this one loop stream-copied for hours, so this single number sets
// the file size of every render. It was CRF 20 — near-archival, and far more than a slow
// drift over a still needs. Measured on a sleep plate: CRF 20 gives 896 kbit/s and a
// 3.7 GB ten-hour file; CRF 26 gives 373 kbit/s and 1.5 GB, at SSIM 0.985 against it,
// which is past the point where the difference is visible. And YouTube re-encodes every
// upload regardless, so the extra bitrate is discarded before any viewer sees it — it
// was only ever costing disk, and upload time on 8 GB files.
//
// Raise it back for material with real motion; this is tuned for stills and slow loops.
const CRF = String(args.crf || 26);

if (!fs.existsSync(audio)) { console.error(`no such audio: ${audio}`); process.exit(1); }

const durationOf = async (f) => {
  const { stdout } = await execFileP("ffprobe",
    ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]);
  return parseFloat(stdout.trim()) || 0;
};

const audioSecs = await durationOf(audio);
console.log(`audio : ${(audioSecs / 3600).toFixed(2)}h  ${path.basename(audio)}`);

const work = path.join(CHANNEL, "beds", ".video-work");
fs.mkdirSync(work, { recursive: true });
const loopFile = path.join(work, `loop-${loopSecs}s.mp4`);

// ── 1. build the seamless visual cycle (encoded once) ────────────────────────
if (args.clip) {
  const clip = resolve(String(args.clip));
  if (!fs.existsSync(clip)) { console.error(`no such clip: ${clip}`); process.exit(1); }
  const slow = Number(args.slow || 1);

  // Two things happen here, both necessary for hours-long use.
  //
  // SLOW: Veo interprets even "the camera does not move at all" fairly liberally, and
  // an 8s clip with visible weather in it is far too animated to sit behind someone's
  // work. Stretching PTS by `slow` and re-interpolating back to 24fps turns it into
  // genuine ambient drift, and costs no credits — much cheaper than re-prompting.
  //
  // PALINDROME: forward then reversed, so the end frame IS the start frame and the
  // repeat has no jump. It also makes weather breathe in and out rather than snapping
  // back, which is the single biggest tell of a looped background.
  const pre = slow > 1
    ? `setpts=${slow}*PTS,minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1,`
    : "";
  console.log(`visual: ${path.basename(clip)} (${slow > 1 ? `${slow}x slower, ` : ""}forward + reverse)`);
  await execFileP("ffmpeg", ["-y", "-i", clip,
    "-filter_complex",
    `[0:v]${pre}scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=24,split[a][b];` +
    "[b]reverse[r];[a][r]concat=n=2:v=1:a=0[v]",
    "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", CRF,
    "-pix_fmt", "yuv420p", loopFile], { maxBuffer: 1 << 26 });
} else {
  const img = resolve(String(args.image));
  if (!fs.existsSync(img)) { console.error(`no such image: ${img}`); process.exit(1); }
  console.log(`visual: ${path.basename(img)} (${loopSecs}s drift, in and back out)`);
  const fps = 24, frames = loopSecs * fps;
  // Zoom 1.00 → 1.06 over the first half, back to 1.00 over the second. Ends exactly
  // where it began, so the cycle repeats invisibly.
  const z = `if(lte(on,${frames / 2}),1+0.06*on/${frames / 2},1.06-0.06*(on-${frames / 2})/${frames / 2})`;
  await execFileP("ffmpeg", ["-y", "-loop", "1", "-i", img,
    "-vf", `scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,` +
           `zoompan=z='${z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${frames}:s=1920x1080:fps=${fps}`,
    "-t", String(loopSecs), "-an", "-c:v", "libx264", "-preset", "medium", "-crf", CRF,
    "-pix_fmt", "yuv420p", loopFile], { maxBuffer: 1 << 26 });
}
console.log(`loop  : ${(await durationOf(loopFile)).toFixed(1)}s encoded`);

// ── 2. repeat it against the audio, no video re-encode ───────────────────────
console.log(`muxing to ${(audioSecs / 3600).toFixed(2)}h …`);
await execFileP("ffmpeg", ["-y",
  "-stream_loop", "-1", "-i", loopFile,
  "-i", audio,
  "-map", "0:v", "-map", "1:a",
  "-c:v", "copy",
  "-c:a", "aac", "-b:a", "192k",
  "-shortest", "-movflags", "+faststart",
  out], { maxBuffer: 1 << 26 });

const finalSecs = await durationOf(out);
const mb = (fs.statSync(out).size / 1e6).toFixed(0);
console.log(`\n✅ ${(finalSecs / 3600).toFixed(2)}h  ${mb} MB\n   ${out}`);
