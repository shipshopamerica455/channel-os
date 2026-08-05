#!/usr/bin/env node
/**
 * 24/7 live stream to YouTube — loops a finished video to RTMP, forever.
 *
 *   node stream.mjs --prep "Monk Mode.mp4"     # one-time: make a stream-ready master
 *   node stream.mjs --source "Monk Mode.mp4"   # start streaming (Ctrl-C to stop)
 *   node stream.mjs --source "..." --720       # half the bitrate, if uplink is tight
 *
 * Needs YOUTUBE_STREAM_KEY in remotion-shorts/.env — get it from
 * Studio → Create → Go live → Stream, and reuse the persistent key.
 *
 * WHY A PREP STEP. YouTube wants a keyframe every 2 seconds; our videos are encoded
 * with x264's default ~10-second GOP. Without matching that, the stream either gets
 * re-encoded by YouTube badly or stalls on seek. So --prep re-encodes ONCE with -g 48
 * (24fps × 2s), and the stream itself then runs `-c copy` — near-zero CPU for something
 * that has to run for months. Re-encoding live instead would peg a core indefinitely.
 *
 * Watch hours are the point: live watch time counts toward the 4,000-hour threshold,
 * and a stream holding even a handful of concurrent viewers accrues them continuously
 * rather than per-view. That is why this is worth running properly rather than casually.
 */
import fs from "fs";
import path from "path";
import { spawn } from "child_process";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CHANNEL = "/Users/admin/Documents/YOUTUBE CHANNELS/MELLOW MELODIES";
const STREAM_DIR = path.join(CHANNEL, "stream");

// Reuse the same .env the rest of the pipeline reads.
for (const envPath of [path.join(__dirname, "../remotion-shorts/.env"),
                       path.join(__dirname, "../video-forge/.env")]) {
  if (!fs.existsSync(envPath)) continue;
  for (const line of fs.readFileSync(envPath, "utf8").split("\n")) {
    const m = /^([A-Z_]+)=(.*)$/.exec(line.trim());
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, "");
  }
}

// ffmpeg is resolved absolutely because launchd runs with a minimal PATH that has no
// /opt/homebrew/bin — a bare "ffmpeg" spawn dies with ENOENT the moment this runs
// as a service rather than from a shell.
const FFMPEG = process.env.FFMPEG_PATH || "/opt/homebrew/bin/ffmpeg";

const args = {};
for (let i = 2; i < process.argv.length; i++) {
  if (process.argv[i].startsWith("--")) {
    const k = process.argv[i].slice(2), n = process.argv[i + 1];
    args[k] = n && !n.startsWith("--") ? process.argv[++i] : true;
  }
}

const resolve = (p) => (path.isAbsolute(p) ? p : path.join(CHANNEL, p));
const readyPath = (src) =>
  path.join(STREAM_DIR, `${path.basename(src, ".mp4")}-stream.mp4`);

// ── prep ─────────────────────────────────────────────────────────────────────
if (args.prep) {
  const src = resolve(String(args.prep));
  if (!fs.existsSync(src)) { console.error(`no such video: ${src}`); process.exit(1); }
  fs.mkdirSync(STREAM_DIR, { recursive: true });
  const out = readyPath(src);
  const v720 = !!args["720"];

  console.log(`prep   ${path.basename(src)}`);
  console.log(`  → ${v720 ? "720p @ 3M" : "1080p @ 4.5M"}, keyframe every 2s`);
  console.log(`  this re-encodes once so the stream itself can run at ~0% CPU.\n`);

  const ff = spawn(FFMPEG, [
    "-y", "-i", src,
    "-c:v", "libx264", "-preset", "veryfast",
    "-b:v", v720 ? "3000k" : "4500k", "-maxrate", v720 ? "3000k" : "4500k",
    "-bufsize", v720 ? "6000k" : "9000k",
    ...(v720 ? ["-vf", "scale=1280:720"] : []),
    "-g", "48", "-keyint_min", "48", "-sc_threshold", "0",  // 2s GOP, no scene cuts
    "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
    out,
  ], { stdio: "inherit" });
  ff.on("exit", (c) => {
    if (c === 0) {
      const gb = (fs.statSync(out).size / 1073741824).toFixed(1);
      console.log(`\n✅ stream master ready (${gb} GB)\n   ${out}\n`);
      console.log(`Start it with:\n  node stream.mjs --source "${path.basename(src)}"`);
    }
    process.exit(c ?? 1);
  });
}

// ── stream ───────────────────────────────────────────────────────────────────
else if (args.source) {
  const key = (process.env.YOUTUBE_STREAM_KEY || "").trim();
  if (!key) {
    console.error(`YOUTUBE_STREAM_KEY not set.\n\n` +
      `  Studio → Create → Go live → Stream tab → copy the stream key,\n` +
      `  then add to remotion-shorts/.env:\n\n    YOUTUBE_STREAM_KEY=xxxx-xxxx-xxxx-xxxx\n`);
    process.exit(1);
  }
  const src = resolve(String(args.source));
  const ready = readyPath(src);
  if (!fs.existsSync(ready)) {
    console.error(`No stream master for "${path.basename(src)}".\n` +
      `  Run first:  node stream.mjs --prep "${path.basename(src)}"`);
    process.exit(1);
  }

  const url = `rtmp://a.rtmp.youtube.com/live2/${key}`;
  console.log(`streaming ${path.basename(ready)}`);
  console.log(`  → rtmp://a.rtmp.youtube.com/live2/****  (key hidden)`);
  console.log(`  looping forever · Ctrl-C to stop\n`);

  let restarts = 0;
  const start = () => {
    const ff = spawn(FFMPEG, [
      "-hide_banner", "-loglevel", "warning", "-stats",
      "-re",                 // pace at real time — without this it floods and gets dropped
      "-stream_loop", "-1",  // loop the file forever
      "-i", ready,
      "-c", "copy",          // already stream-shaped by --prep; no re-encode
      "-f", "flv", url,
    ], { stdio: ["ignore", "inherit", "inherit"] });

    ff.on("exit", (code, sig) => {
      if (sig === "SIGINT" || sig === "SIGTERM") return;
      restarts++;
      // Backoff so a persistent fault (revoked key, no network) doesn't hammer YouTube,
      // but a transient blip recovers in seconds. A dropped stream zeroes the concurrent
      // viewer count, so recovering fast genuinely matters.
      const wait = Math.min(5 * 2 ** Math.min(restarts - 1, 5), 300);
      console.error(`\n[stream] ffmpeg exited (${code}). restart #${restarts} in ${wait}s…`);
      setTimeout(start, wait * 1000);
    });
    process.on("SIGINT", () => { ff.kill("SIGINT"); process.exit(0); });
  };
  start();
}

else {
  console.log(fs.readFileSync(new URL(import.meta.url), "utf8")
    .split("*/")[0].replace(/^\/\*\*|^ \* ?/gm, ""));
}
