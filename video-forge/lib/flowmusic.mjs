/**
 * Google Flow Music via the useapi.net wrapper — the audio sibling of lib/flow.mjs,
 * driving YOUR linked Google account. Same USEAPI_TOKEN, different bot.
 *
 *   flowMusic({ prompt, outPath })        → one generated track (mp3)
 *   flowMusicEdit({ clip, operation })    → cover | remix | extend | replace | effect | stems
 *   musicBed({ prompt, minutes, outPath }) → a long ambient bed built from N tracks
 *
 * The music is generated, so it is yours: no Content ID claim, no revenue diverted
 * to a rights holder. That is the whole reason to use this instead of "curated"
 * recordings on a music channel that needs to monetize.
 *
 * Auth/setup (from video-forge/.env or ../remotion-shorts/.env):
 *   USEAPI_TOKEN              useapi.net API token — the SAME one lib/flow.mjs uses
 *   USEAPI_FLOWMUSIC_ACCOUNT  the Gmail linked to Flow Music (falls back to
 *                             USEAPI_FLOW_ACCOUNT if you linked the same account)
 *
 * Linking is a one-time manual step — see flowMusicLink() and the README.
 * Schema matched to useapi's FlowMusic v1 docs, 2026-07. Endpoints and field names
 * are centralized in CONFIG so a future API change stays a one-line fix.
 * Validate with `node scripts/flowmusic-smoke.mjs`.
 */
import fs from "fs";
import path from "path";
import { assembleBed } from "./musicbed.mjs";

const CONFIG = {
  base: process.env.USEAPI_BASE || "https://api.useapi.net/v1",
  accountsPath: "/flowmusic/accounts",
  accountPath: (email) => `/flowmusic/accounts/${encodeURIComponent(email)}`,
  usagePath: "/flowmusic/accounts/usage",
  musicPath: "/flowmusic/music",
  editPath: "/flowmusic/music/edit",
  downloadPath: "/flowmusic/music/download",
  // Poll at /jobs/{jobid} — verified live 2026-07-26. The docs imply /music/{jobid},
  // but that returns 400 "Wrong GET url"; /music/ is the list-and-create route only.
  // The id is passed RAW: it contains colons and an @, and the endpoint 400s on a
  // percent-encoded id.
  jobPaths: (id) => [`/flowmusic/jobs/${id}`, `/flowmusic/music/${id}`],
  // A Flow Music generation runs ~2 minutes; always go async rather than holding
  // an HTTP connection open that long.
  pollTimeoutMs: 8 * 60_000,
  pollIntervalMs: 6000,
};

function token() {
  const t = (process.env.USEAPI_TOKEN || "").trim();
  if (!t) throw new Error("USEAPI_TOKEN not set — add it to video-forge/.env (useapi.net API token).");
  return t;
}

/** Flow Music may be linked to a different Gmail than Flow; fall back to Flow's. */
function email() {
  const e = (process.env.USEAPI_FLOWMUSIC_ACCOUNT || process.env.USEAPI_FLOW_ACCOUNT || "").trim();
  if (!e) throw new Error("USEAPI_FLOWMUSIC_ACCOUNT not set — add the Gmail linked to Flow Music in video-forge/.env.");
  return e;
}

async function api(pathname, { method = "GET", json, expectBinary } = {}) {
  const headers = { authorization: `Bearer ${token()}` };
  let body;
  if (json) { headers["content-type"] = "application/json"; body = JSON.stringify(json); }
  if (!expectBinary) headers.accept = "application/json";
  const res = await fetch(`${CONFIG.base}${pathname}`, { method, headers, body });
  if (expectBinary) {
    if (!res.ok) throw new Error(`useapi ${method} ${pathname} → ${res.status}`);
    return Buffer.from(await res.arrayBuffer());
  }
  const text = await res.text();
  let data; try { data = text ? JSON.parse(text) : {}; } catch { data = { raw: text }; }
  if (!res.ok) throw new Error(`useapi ${method} ${pathname} → ${res.status}: ${text.slice(0, 300)}`);
  return data;
}

const statusOf = (r) => (r?.status || "").toLowerCase();
const clipsOf = (r) => r?.clips ?? r?.response?.clips ?? [];

/** Submit a music job and return its completed clips[]. */
/**
 * Submit with retry. The endpoint intermittently 500s on submit — observed as a
 * server-side `Command 2 [ JSON.SET ] failed` on a prompt that succeeded
 * unchanged moments later. It's their flakiness, not ours, so retry the submit
 * rather than losing a whole render at the score stage.
 */
async function submitWithRetry(pathname, jsonBody, tries = 3) {
  let last;
  for (let i = 1; i <= tries; i++) {
    try {
      return await api(pathname, { method: "POST", json: jsonBody });
    } catch (e) {
      last = e;
      if (!/→ 5\d\d:/.test(e.message) || i === tries) throw e;
      const wait = 3000 * i;
      console.warn(`  [flowmusic] submit ${i}/${tries} failed (${e.message.slice(0, 80)}) — retrying in ${wait / 1000}s`);
      await new Promise((r) => setTimeout(r, wait));
    }
  }
  throw last;
}

async function runJob(pathname, jsonBody) {
  const r = await submitWithRetry(pathname, jsonBody);
  if (statusOf(r) === "completed" && clipsOf(r).length) return clipsOf(r);
  if (statusOf(r) === "failed") throw new Error(`generation failed: ${r.error || JSON.stringify(r).slice(0, 200)}`);
  const jobId = r.jobid || r.jobId || r.id;
  if (!jobId) {
    if (clipsOf(r).length) return clipsOf(r);
    throw new Error(`no jobid / clips in response: ${JSON.stringify(r).slice(0, 300)}`);
  }
  const started = Date.now();
  let paths = CONFIG.jobPaths(jobId);
  while (Date.now() - started < CONFIG.pollTimeoutMs) {
    await new Promise((res) => setTimeout(res, CONFIG.pollIntervalMs));
    let j;
    for (const p of paths) {
      // A wrong route answers 400/403/404 — keep trying the others, but let a real
      // failure (500, auth) surface instead of being masked as a routing miss.
      try { j = await api(p); paths = [p]; break; } catch (e) { if (!/→ 40[034]/.test(e.message)) throw e; }
    }
    if (!j) throw new Error(`job ${jobId}: no reachable poll endpoint (tried ${CONFIG.jobPaths(jobId).join(", ")})`);
    const st = statusOf(j);
    if (st === "completed") {
      const clips = clipsOf(j);
      if (!clips.length) throw new Error(`job ${jobId} completed but returned no clips`);
      return clips;
    }
    if (st === "failed") {
      const why = typeof j.error === "string" ? j.error : JSON.stringify(j.error || j).slice(0, 240);
      const err = new Error(`job ${jobId} failed: ${why}`);
      err.jobFailed = true;   // distinguishes a duff generation from a broken link
      throw err;
    }
  }
  throw new Error(`job ${jobId} timed out after ${Math.round(CONFIG.pollTimeoutMs / 1000)}s`);
}

/**
 * Clips carry public URLs; fall back to the authenticated download endpoint.
 * Prefer `wav_url` — these get faded and re-encoded during bed assembly, and starting
 * from lossy m4a would stack a second generation of compression artefacts onto
 * material people listen to for hours.
 */
async function downloadClip(clip, outPath) {
  for (const url of [clip.wav_url, clip.audio_url].filter(Boolean)) {
    const res = await fetch(url);
    if (res.ok) { fs.writeFileSync(outPath, Buffer.from(await res.arrayBuffer())); return outPath; }
  }
  const buf = await api(`${CONFIG.downloadPath}?id=${encodeURIComponent(clip.clip)}`, { expectBinary: true });
  fs.writeFileSync(outPath, buf);
  return outPath;
}

// ── account management ───────────────────────────────────────────────────────

/** All Flow Music accounts linked to this useapi token. `{}` means none yet. */
export const flowMusicAccounts = () => api(CONFIG.accountsPath);

/** Token + credit usage for one account. */
export const flowMusicUsage = (addr = email()) =>
  api(`${CONFIG.usagePath}?email=${encodeURIComponent(addr)}`);

/**
 * Link a Google account for Flow Music. `refreshToken` comes from the browser
 * session of the Google account on labs.google — useapi's setup page walks
 * through extracting it. One-time, manual, and it needs your own login, so this
 * is exposed as a helper rather than run automatically.
 */
export const flowMusicLink = (refreshToken, { maxJobs } = {}) =>
  api(CONFIG.accountsPath, {
    method: "POST",
    json: { refresh_token: refreshToken, ...(maxJobs ? { maxJobs } : {}) },
  });

// ── generation ───────────────────────────────────────────────────────────────

/**
 * Generate. Returns the clip records — note ONE generation yields **two** clips, so
 * take counts should be planned in twos; ignoring the second halves your credit yield.
 *
 * No `seed`: the docs list it as an optional field but the live endpoint rejects it
 * outright ("Parameter seed not supported", 400), and returned clips carry
 * `seed: null`. Verified 2026-07-26. Repeated calls with the same prompt vary on their
 * own, which is what distinct takes need anyway.
 */
/**
 * useapi's FlowMusic endpoint 500s on a prompt containing newlines — it fails
 * server-side in a Redis JSON.SET with "invalid character 'a' looking for
 * beginning of value", which reads like a bug in this file rather than in
 * theirs. Collapse all whitespace before sending.
 */
const flatten = (s) => String(s).replace(/\s+/g, " ").trim();

export async function flowMusicGenerate(prompt, { refAudio, refImage } = {}) {
  return runJob(CONFIG.musicPath, {
    email: email(), prompt: flatten(prompt), mode: "async",
    ...(refAudio ? { refAudio1: refAudio } : {}),
    ...(refImage ? { refImage1: refImage } : {}),
  });
}

/** Generate and write the first clip. Convenience wrapper for one-offs. */
export async function flowMusic(prompt, outPath, opts = {}) {
  const clips = await flowMusicGenerate(prompt, opts);
  if (outPath) await downloadClip(clips[0], outPath);
  return clips[0];
}

/** Write every clip of a generation to `dir` as <prefix>-a.wav, -b.wav, … */
export async function downloadClips(clips, dir, prefix) {
  const out = [];
  for (let i = 0; i < clips.length; i++) {
    const f = path.join(dir, `${prefix}-${String.fromCharCode(97 + i)}.wav`);
    if (!fs.existsSync(f)) await downloadClip(clips[i], f);
    out.push(f);
  }
  return out;
}

/**
 * Edit an existing clip. `operation` is one of:
 *   effect | extend | replace | cover | remix | stems
 * Operation-specific fields pass straight through in `fields`.
 */
export async function flowMusicEdit({ clip, operation, outPath, ...fields }) {
  const clipId = typeof clip === "string" ? clip : clip?.clip;
  if (!clipId) throw new Error("flowMusicEdit needs a clip id (or a clip record).");
  const clips = await runJob(CONFIG.editPath, { email: email(), clip: clipId, operation, ...fields });
  if (outPath && clips[0]) await downloadClip(clips[0], outPath);
  return clips;
}

/** List previously generated clips, most recent first. */
export const flowMusicList = ({ limit = 20, offset = 0 } = {}) =>
  api(`${CONFIG.musicPath}?email=${encodeURIComponent(email())}&limit=${limit}&offset=${offset}`);

// ── long-form bed assembly ───────────────────────────────────────────────────

/**
 * Generate `takes` tracks and assemble them into a bed of `minutes`.
 *
 * Assembly itself lives in lib/musicbed.mjs and is provider-agnostic — the same
 * function backs beds built from downloads. This wrapper only adds generation.
 *
 * Each generation returns two clips, so this runs ceil(takes/2) generations and keeps
 * both. Takes are cached on disk by generation index, so re-running for a longer bed
 * costs nothing, and raising `takes` only generates the shortfall.
 */
export async function musicBed({
  prompt, minutes = 60, takes = 16, outPath, fade = 4, workDir,
}) {
  if (!outPath) throw new Error("musicBed needs an outPath.");
  const dir = workDir || path.join(path.dirname(outPath), "bed-parts");
  fs.mkdirSync(dir, { recursive: true });

  const gens = Math.ceil(takes / 2);
  const files = [];
  for (let g = 0; g < gens; g++) {
    const prefix = `gen-${String(g + 1).padStart(2, "0")}`;
    // A take counts as already generated if EITHER its raw download survives or its
    // faded mp3 does. assembleBed only reads the raw file when the faded one is
    // missing, so once a take has been faded the download is dead weight — and it is
    // big: a slot's raw wavs run 1.3 GB against 161 MB of faded mp3, 89% of the folder.
    //
    // Before this, the check was `endsWith(".wav")` alone, so reclaiming that space
    // made the assembler believe the takes had never been generated and silently
    // respend Flow Music credits regenerating audio that was already on disk.
    const entries = fs.readdirSync(dir);
    const raw = entries.filter((f) => f.startsWith(`${prefix}-`) && /\.(wav|flac)$/i.test(f));
    const fadedOnly = entries
      .filter((f) => f.startsWith(`${prefix}-`) && f.endsWith("-faded.mp3"))
      .map((f) => f.replace(/-faded\.mp3$/, ".wav"))        // notional source name
      .filter((n) => !raw.includes(n));
    const existing = [...raw, ...fadedOnly];
    if (existing.length) {
      files.push(...existing.map((f) => path.join(dir, f)));
      continue;
    }
    process.stdout.write(`  [flowmusic] generation ${g + 1}/${gens} … `);
    // A single duff generation used to abort the whole bed — one server-side failure
    // on take 3 of 8 threw away the two good takes before it and the six after. The
    // job either succeeds or it doesn't, so just ask again; only a broken auth chain
    // is worth surrendering to, because every subsequent attempt would fail the same way.
    let written = null;
    for (let attempt = 1; attempt <= 3 && !written; attempt++) {
      try {
        const clips = await flowMusicGenerate(prompt);
        written = await downloadClips(clips, dir, prefix);
      } catch (e) {
        if (/refresh_token_already_used|refresh chain broken/.test(e.message)) throw e;
        if (attempt === 3) throw e;
        process.stdout.write(`retry ${attempt}/3 … `);
        await new Promise((r) => setTimeout(r, 4000 * attempt));
      }
    }
    console.log(`${written.length} clips`);
    files.push(...written);
  }

  return assembleBed({ files: files.slice(0, takes), minutes, outPath, fade, workDir: dir });
}

export { CONFIG as flowMusicConfig };
