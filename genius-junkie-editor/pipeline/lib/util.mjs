// Shared paths, config and helpers for the Genius Junkie pipeline.
import { execFileSync, execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const ROOT = path.resolve(__dirname, '../../..');            // Kimi Extension v1
export const EDITOR = path.join(ROOT, 'genius-junkie-editor');
export const SHORTS = path.join(ROOT, 'genius-junkie-shorts');
export const REMOTION = path.join(SHORTS, 'remotion');
export const MEDIA = path.join(SHORTS, 'media', 'projects');
export const UPLOADER = path.join(ROOT, 'remotion-shorts', 'upload-geniusjunkie.mjs');
export const FORGE = path.join(ROOT, 'video-forge');

export const CONFIG = {
  channelId: 'UCz8eVGSEicfswKIe4XAp7Kw',
  // Kokoro bm_fable — measured per video: 3.158 / 3.314 / 3.255 (v5-7),
  // then 3.44 / 3.54 / 3.65 (v8-10), 3.55 (v11), 3.70 (v12). The rate drifts
  // UP, and a rate higher than assumed makes the real runtime SHORTER than
  // projected — the direction that costs mid-rolls. Track the fastest
  // observed, not the mean.
  wordsPerSecond: 3.70,
  // pads + ad gaps + end screen add a near-constant tail (17.5 / 18.0 / 17.5)
  overheadSec: 17.7,
  targetRuntimeSec: 520,          // 8:40 — clears the 8-min mid-roll gate with margin
  voice: 'bm_fable',
  kokoroPython: `${process.env.HOME}/.venvs/tts-bakeoff/bin/python`,
  // PINNED, not 'python3'. On 22 Oct 2026 Homebrew moved python3 to 3.15, which has
  // none of whisper / numpy / scipy / reportlab — align, music and every PDF maker
  // broke at once with ModuleNotFoundError. Everything the pipeline needs lives
  // under 3.14; reinstall there (or move all of it) before changing this.
  python: '/opt/homebrew/bin/python3.14',
  whisperPython: '/opt/homebrew/bin/python3.14',
  whisperModel: 'small.en',
  // timeline
  lead: 1.2, pad: 0.5, adGap: 1.4, endScreen: 8.0,
  // publishing cadence
  longFormUTC: '17:00', shortUTC: '12:00', daysBetweenLongForm: 2,
  // Shorts ladder. FOUR shorts per long-form at ONE slot a day cannot fit a
  // 2-day long-form cadence — consecutive videos always collide on days +3
  // and +4. Two slots a day is what the channel actually publishes on.
  shortSlotsUTC: ['12:00', '19:00'],
  // audio master
  loudness: { I: -14, TP: -1.5, LRA: 11 },
  server: 'geniusjunkie',
  site: 'https://geniusjunkie.net',
  // Handovers go where Annieth actually works, not into the repo. A
  // NEXT-ACTIONS.md buried in videos/<slug>/ is a file nobody opens; the
  // channel's 00_Handovers folder is the one she already keeps HANDOFF.md and
  // the workflow notes in. Per-video filename, or each release overwrites the
  // last one's outstanding tasks.
  handovers: '/Users/admin/Documents/YOUTUBE CHANNELS/GENIUS JUNKIE YT CHANNEL/00_Handovers',
};

/**
 * The paid-kit PDFs sit under an unguessable path prefix, rotated on 3 Nov 2026
 * after the old /content/files/club/ URLs turned out to be publicly indexable
 * and listed in sitemap-pages.xml. That prefix is the only thing protecting
 * them, and this repo has a PUBLIC GitHub remote, so it lives in
 * pipeline/kit-base.json, which is gitignored.
 *
 * Lazy, not a CONFIG key: a missing file must break `gj product` / `gj commerce`
 * loudly rather than every other command at import time. Never fall back to a
 * default -- a wrong prefix would re-publish the kits on a public path.
 */
let _kitBase;
export function kitBase() {
  if (_kitBase) return _kitBase;
  const f = path.join(EDITOR, 'pipeline', 'kit-base.json');
  if (!fs.existsSync(f)) {
    throw new Error(`missing ${f} — it holds the paid-kit path prefix and is deliberately not in git. ` +
      `Recover it from the server: ssh ${CONFIG.server} ls /var/www/ghost/content/files/`);
  }
  const { kitBase: k } = JSON.parse(fs.readFileSync(f, 'utf8'));
  if (!/^club-[0-9a-f]{16}$/.test(k || '')) throw new Error(`kit-base.json: kitBase is not a rotated prefix (${k})`);
  _kitBase = k;
  return k;
}

/**
 * The Canva template share links, which ARE the paid product — holding one
 * gets you the editable template for nothing, and rotating one in Canva breaks
 * every past buyer. They live only in gitignored pipeline/canva-links.json;
 * page sources carry CANVA_LINK placeholders instead.
 *
 * Lazy and throwing for the same reason as kitBase(): a missing store must stop
 * `gj commerce`, not every command, and must never fall back to publishing a
 * page with the placeholder still in the href.
 */
let _canva;
export function canvaLinks(slug) {
  if (!_canva) {
    const f = path.join(EDITOR, 'pipeline', 'canva-links.json');
    if (!fs.existsSync(f)) {
      throw new Error(`missing ${f} — it holds the Canva template links and is deliberately not in git. ` +
        `Recover each one from Canva: open the design > Share > Template link > Copy.`);
    }
    _canva = JSON.parse(fs.readFileSync(f, 'utf8')).links || {};
  }
  const links = _canva[slug] || {};
  for (const [k, v] of Object.entries(links)) {
    if (!/^https:\/\/canva\.link\/[A-Za-z0-9_-]+$/.test(v)) {
      throw new Error(`canva-links.json: ${slug}.${k} is not a canva.link template URL`);
    }
  }
  return links;
}

/**
 * The same links keyed by the placeholder a page source uses: `canvaTemplate`
 * is CANVA_LINK, `canvaTemplateDesktop` is CANVA_LINK_DESKTOP. Two templates in
 * one kit (wallpapers, digital-scrapbooking, kdp-book-cover) each get their own.
 */
export function canvaPlaceholders(slug) {
  return Object.fromEntries(Object.entries(canvaLinks(slug)).map(([k, v]) => {
    const suffix = k.slice('canvaTemplate'.length);
    return [suffix ? `CANVA_LINK_${suffix.toUpperCase()}` : 'CANVA_LINK', v];
  }));
}

export const c = {
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
  bold: (s) => `\x1b[1m${s}\x1b[0m`,
  green: (s) => `\x1b[32m${s}\x1b[0m`,
  yellow: (s) => `\x1b[33m${s}\x1b[0m`,
  red: (s) => `\x1b[31m${s}\x1b[0m`,
  cyan: (s) => `\x1b[36m${s}\x1b[0m`,
};

export const log = {
  step: (s) => console.log(`\n${c.cyan('▸')} ${c.bold(s)}`),
  ok: (s) => console.log(`  ${c.green('✓')} ${s}`),
  skip: (s) => console.log(`  ${c.dim('•')} ${c.dim(s + ' (exists — use --force to redo)')}`),
  warn: (s) => console.log(`  ${c.yellow('!')} ${s}`),
  info: (s) => console.log(`  ${c.dim(s)}`),
};

export function sh(cmd, opts = {}) {
  return execSync(cmd, { encoding: 'utf8', stdio: opts.quiet ? 'pipe' : 'inherit', cwd: opts.cwd, maxBuffer: 1 << 28 });
}
/** Run a Python snippet by writing it to a temp file — `python -c` mangles newlines. */
export function runPy(python, code, opts = {}) {
  const f = path.join(process.env.TMPDIR || '/tmp', `gj-${Date.now()}-${Math.random().toString(36).slice(2)}.py`);
  fs.writeFileSync(f, code);
  try { return sh(`${python} ${f}${opts.filter ? ` 2>&1 | ${opts.filter}` : ''}`, opts); }
  finally { try { fs.unlinkSync(f); } catch {} }
}

export function shOut(cmd, opts = {}) {
  return execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'], cwd: opts.cwd, maxBuffer: 1 << 28 }).trim();
}

export function videoDir(slug) { return path.join(EDITOR, 'videos', slug); }
export function manifestPath(slug) { return path.join(videoDir(slug), 'video.json'); }

export function readManifest(slug) {
  const p = manifestPath(slug);
  if (!fs.existsSync(p)) throw new Error(`No video.json in videos/${slug} — run: gj init ${slug}`);
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}
export function writeManifest(slug, m) {
  fs.writeFileSync(manifestPath(slug), JSON.stringify(m, null, 2) + '\n');
}

export function exists(p) { return fs.existsSync(p); }
export function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }

export function duration(file) {
  return parseFloat(shOut(`ffprobe -v error -show_entries format=duration -of csv=p=0 "${file}"`));
}

/** Parse the `> quoted` VO body out of a script.md section. */
/**
 * Split script.md into sections, taking EVERY quoted line in each one.
 *
 * This used to match a CONTIGUOUS run of `>` lines, so any non-quoted line
 * inside a section silently ended it and the rest of that section's narration
 * was dropped with no warning. An `<!-- AD BREAK -->` comment placed mid-section
 * cost the thank-you-cards video 114 words of S08 — the actual fix in that
 * section — and nothing said so; it only showed up as an 11-second section in
 * the timeline. Take the whole block up to the next heading, then collect the
 * quoted lines out of it.
 */
export function parseScript(scriptPath) {
  const src = fs.readFileSync(scriptPath, 'utf8');
  const out = [];
  // Split on the headings rather than matching a body pattern. Two regexes
  // have now silently eaten script content here, so this deliberately does
  // the dumbest possible thing:
  //   v1 matched a CONTIGUOUS run of `>` lines, so any non-quoted line inside
  //      a section ended it (an <!-- AD BREAK --> comment cost one video 114
  //      words of its most important section).
  //   v2 used `(?=^## |\Z)` as a terminator — but JavaScript HAS NO \Z. It is
  //      a literal "Z", and with the /i flag it matched any "z", so every
  //      section was cut at its first letter z. One section came back as 17
  //      words of 148, and the build happily carried on.
  // Splitting on headings cannot truncate a body at all.
  for (const part of src.split(/^## /m).slice(1)) {
    const head = part.match(/^(S\d+b?) — ([^\n(]*)/);
    if (!head) continue;
    const text = part.split('\n').filter((l) => /^>/.test(l))
      .map((l) => l.replace(/^>\s?/, '').trim()).join(' ')
      .replace(/\[VISUAL:[\s\S]*?\]/g, '').replace(/\s+/g, ' ').trim();
    if (!text) continue;
    out.push({ id: head[1], title: head[2].trim(), text, words: text.split(/\s+/).filter(Boolean).length });
  }
  return out;
}

/** Next free long-form slot: >= daysBetween after the latest scheduled video. */
export function nextSlot(afterISO) {
  const base = afterISO ? new Date(afterISO) : new Date();
  const d = new Date(base);
  d.setUTCDate(d.getUTCDate() + CONFIG.daysBetweenLongForm);
  const [h, mi] = CONFIG.longFormUTC.split(':').map(Number);
  d.setUTCHours(h, mi, 0, 0);
  if (d <= new Date()) { d.setUTCDate(d.getUTCDate() + CONFIG.daysBetweenLongForm); }
  return d.toISOString();
}
export function plusDaysAt(iso, days, hhmm) {
  const d = new Date(iso);
  d.setUTCDate(d.getUTCDate() + days);
  const [h, mi] = hhmm.split(':').map(Number);
  d.setUTCHours(h, mi, 0, 0);
  return d.toISOString();
}

/**
 * Every slot already taken, asked of YOUTUBE rather than of local files.
 *
 * packaging.json records what the pipeline INTENDED. Anything rescheduled by
 * hand leaves it stale — on 2 Oct 2026 four entries were already wrong — and
 * scheduling against stale data is exactly how two videos end up in the same
 * minute. Falls back to the local files only if the API cannot be reached, and
 * says so loudly, because a silent fallback to wrong data is the worse failure.
 */
export function occupiedSlots() {
  const script = path.join(ROOT, 'remotion-shorts', 'gj-scheduled-slots.mjs');
  try {
    const out = execFileSync('node', [script], { encoding: 'utf8', timeout: 180_000, stdio: ['ignore', 'pipe', 'pipe'] });
    const slots = out.split('\n').map((s) => s.trim()).filter(Boolean);
    return { slots: new Set(slots.map((s) => new Date(s).toISOString())), source: 'youtube' };
  } catch (e) {
    log.warn(`could not read the live schedule (${String(e.message || e).slice(0, 60)}) — falling back to local packaging.json, WHICH MAY BE STALE`);
    const slots = new Set();
    const dir = path.join(EDITOR, 'videos');
    for (const slug of fs.readdirSync(dir)) {
      const p = path.join(dir, slug, 'packaging.json');
      if (!fs.existsSync(p)) continue;
      try {
        const pkg = JSON.parse(fs.readFileSync(p, 'utf8'));
        if (pkg.publishAt) slots.add(new Date(pkg.publishAt).toISOString());
        for (const sh of Object.values(pkg.shorts || {}))
          if (sh.publishAt) slots.add(new Date(sh.publishAt).toISOString());
      } catch { /* ignore malformed */ }
    }
    return { slots, source: 'local (stale risk)' };
  }
}

/**
 * Place `count` shorts in the first FREE slots after the long-form, walking
 * the daily ladder (12:00, 19:00, next day 12:00, …). Throws rather than
 * double-booking — a collision is silent on upload and only shows up when two
 * videos publish into the same minute.
 */
export function freeShortSlots(longformISO, count, occupied, maxDays = 30) {
  const picked = [];
  // A slot that has already passed is not a free slot. The ladder starts at the
  // long-form's publishAt, so any release that runs LATE — which is every
  // release while the scheduled tasks are not firing — was being handed dates
  // in the past. YouTube treats a publishAt in the past as "publish now", so
  // the Shorts would have gone public the moment they finished uploading,
  // against the one rule this pipeline is not allowed to break. Require a
  // minimum lead time so the upload has processed before its moment arrives.
  const LEAD_MIN = 60;
  const earliest = Date.now() + LEAD_MIN * 60_000;
  for (let day = 1; day <= maxDays && picked.length < count; day++) {
    for (const hhmm of CONFIG.shortSlotsUTC) {
      if (picked.length >= count) break;
      const iso = plusDaysAt(longformISO, day, hhmm);
      if (occupied.has(iso)) continue;
      if (new Date(iso).getTime() < earliest) continue;
      picked.push(iso);
      occupied.add(iso);               // so this run does not collide with itself
    }
  }
  if (picked.length < count)
    throw new Error(`could not place ${count} shorts in ${maxDays} days after ${longformISO} — the queue is full`);
  return picked;
}

/** Latest publishAt across every shipped video, so the cadence never collides. */
export function latestScheduled() {
  const dir = path.join(EDITOR, 'videos');
  let latest = null;
  for (const slug of fs.readdirSync(dir)) {
    const p = path.join(dir, slug, 'packaging.json');
    if (!fs.existsSync(p)) continue;
    try {
      const pub = JSON.parse(fs.readFileSync(p, 'utf8')).publishAt;
      if (pub && (!latest || new Date(pub) > new Date(latest))) latest = pub;
    } catch { /* ignore malformed */ }
  }
  return latest;
}
