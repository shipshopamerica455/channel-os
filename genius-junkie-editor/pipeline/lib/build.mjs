// Build stages: brief → voice → align → timeline → images.
import fs from 'fs';
import path from 'path';
import {
  CONFIG, EDITOR, FORGE, MEDIA, SHORTS, REMOTION, c, log, sh, shOut,
  videoDir, readManifest, writeManifest, exists, ensureDir, duration, parseScript, runPy,
} from './util.mjs';

// ---------------------------------------------------------------- brief -----
/** Pull the next unshipped slate row and scaffold the folder + research brief. */
export function brief(slug, opts = {}) {
  const dir = videoDir(slug);
  ensureDir(dir);
  const slate = fs.readFileSync(path.join(EDITOR, 'VIDEOS.md'), 'utf8');
  const next = slate.split('\n').find((l) => /^- \[ \]/.test(l)) || '';
  const topic = opts.topic || next.replace(/^- \[ \]\s*/, '').replace(/ — NEXT\s*$/, '');

  const budget = Math.round((CONFIG.targetRuntimeSec - CONFIG.overheadSec) * CONFIG.wordsPerSecond);
  const briefPath = path.join(dir, 'brief.md');
  if (exists(briefPath) && !opts.force) { log.skip('brief.md'); return briefPath; }

  const body = `# Brief — ${topic}

_Generated ${new Date().toISOString().slice(0, 10)} by \`gj brief\`._

## The job
Write \`script.md\` for this video. When it's done run \`gj build ${slug}\`.

## Hard numbers
- Voice: Kokoro \`${CONFIG.voice}\` — measured **${CONFIG.wordsPerSecond} words/sec**.
- Target runtime **${Math.round(CONFIG.targetRuntimeSec / 60 * 10) / 10} min** ⇒ **~${budget} words** of VO total.
- Must clear **8:00** so two mid-rolls are allowed. Under-writing is the #1 cause of a re-record.
- 13–15 sections. Two DESIGNED AD BREAKS: after the section ending ~40% in, and ~72% in.

## Required shape (each \`## SNN — TITLE (~N words)\` then a \`>\` quoted block)
1. **S01 HOOK** (~110 w) — **NAME THE TRAP OUTRIGHT, inside the first 30 seconds.**
   Not "stay tuned for the mistake everyone makes" — say what breaks and name the
   setting that fixes it, then "here's how to build it so that never happens".
2. **S02** — the free asset, in ONE sentence (~20 w), then the 2–3 principles.
3. **S03–S05** — setup and the main build. S05 is full say-it-show-it.
   → **AD BREAK 1** after S05.
4. **S06** — the trap DEMONSTRATED: show the failure, then the fix on screen.
   S01 made the claim; S06 proves it. TWO of the four Shorts come from here.
5. **S07–S09** — the rules, the polish, the export.
   → **AD BREAK 2** after S09.
6. **S10–S11** — the system/scale play.
7. **S12** checklist · **S13** the £4.99 pack CTA · **S14** outro + end screen.

### Why the trap is named twice
Channel AVD is **~1:16**. A trap first revealed at 3:09 is seen by a minority of
viewers, and a CTA at 8:08 by almost none. S01 must therefore carry the claim and
the free-asset link on its own, as if no one sees another second. S06 keeps the
full demonstration — that is what the Shorts are cut from and what earns the
watch time from people who do stay.

This costs some AVD: some viewers get the answer and leave. That is the correct
trade here — at the £3.23 RPM one £4.99 sale is worth about 1,545 views of ad
money, so a viewer who receives the offer beats a viewer who watches longer.

## Before you code a single scene — LOOK at anchors/
Open \`anchors/\` and actually look at the images. The CANONICAL thumbnail and
scene frames are the standard; prose did not stop videos #16 and #17 shipping
off-brand, side-by-side comparison did. Copy the skeleton, change the content.

## QA is section-aware now — use it
\`gj qa ${slug}\` samples three frames INSIDE every section and tiles them nine
to a sheet, each labelled \`S07 · 4:11\`. READ the sheets before rendering.
Look for: dead space (content only in one corner), and reveals that lag the
narration. Those are the two defects this pipeline actually produces.
\`--per-section N\` for density, \`--uniform\` for the old even sampling.

## Style laws (non-negotiable — see HANDOFF-PRODUCTION.md)
- Say-it-show-it: every instruction must be visible on screen as it's spoken.
- A visual change every 3–6 s. No still frame longer than 6 s.
- Numbers written phonetically ("twelve point five two") — local TTS mangles digits.
- Bright by default; dark only as a deliberate beat.
- Name the real trap. Every video needs one fact competitors get wrong.

## Fact-check before writing
Run these and cite what you find in a "Facts verified" block at the top of script.md:
${(opts.checks || ['<the platform\'s current limits/specs>', '<the pricing or fee that changed>', '<the rule people get wrong>']).map((q) => `- [ ] ${q}`).join('\n')}

## Cutaway budget (HARD RULE)
4–6 Flow photo cutaways placed on **emotional** lines, never over an instruction.
Add them to \`video.json\` → \`images[]\` with a prompt each, then \`gj images ${slug}\`.

## Product
Every video ships a £4.99 pack: an editable Canva template + generated PDFs.
Sketch what's in it at the bottom of script.md so \`make_*_pack.py\` can be written.
`;
  fs.writeFileSync(briefPath, body);
  log.ok(`brief.md — topic: ${c.bold(topic)} · budget ~${budget} words`);

  if (!exists(path.join(dir, 'video.json'))) {
    writeManifest(slug, {
      slug, topic, shotDir: '', project: `gj-${slug}`, composition: '', thumb: '',
      promos: [], adAfter: [], images: [], product: { name: '', price: '£4.99' }, publishAt: null,
    });
    log.ok('video.json scaffold — fill in shotDir/composition once the scenes exist');
  }
  return briefPath;
}

// ---------------------------------------------------------------- voice -----
export function voice(slug, opts = {}) {
  const dir = videoDir(slug);
  const scriptPath = path.join(dir, 'script.md');
  if (!exists(scriptPath)) throw new Error(`No script.md in videos/${slug} — write it first (see brief.md)`);
  const sections = parseScript(scriptPath);
  if (!sections.length) throw new Error('script.md has no "## SNN — TITLE" sections with > quoted VO');

  const voDir = path.join(dir, 'vo');
  ensureDir(voDir);
  const totalWords = sections.reduce((a, s) => a + s.words, 0);
  const projected = totalWords / CONFIG.wordsPerSecond + CONFIG.overheadSec;
  log.info(`${sections.length} sections · ${totalWords} words · projected ${(projected / 60).toFixed(2)} min runtime`);
  if (projected < 495) {
    const short = Math.ceil((495 - projected) * CONFIG.wordsPerSecond);
    log.warn(`projected runtime ${(projected / 60).toFixed(2)} min is too close to the 8:00 gate — add ~${short} words before generating VO`);
  }

  const todo = sections.filter((s) => opts.force || !exists(path.join(voDir, `${fileFor(s)}.mp3`)));
  if (!todo.length) { log.skip(`${sections.length} VO files`); return checkRuntime(slug, sections, voDir, totalWords); }

  const payload = todo.map((s) => ({ file: fileFor(s), text: s.text }));
  const tmp = path.join(dir, '.vo-todo.json');
  fs.writeFileSync(tmp, JSON.stringify(payload));
  const py = `
import json, subprocess, sys, numpy as np, soundfile as sf
from kokoro import KPipeline
todo = json.load(open(${JSON.stringify(tmp)}))
pipe = KPipeline(lang_code='b', repo_id='hexgrad/Kokoro-82M')
for item in todo:
    audio = np.concatenate([a for _, _, a in pipe(item["text"], voice=${JSON.stringify(CONFIG.voice)})])
    wav = ${JSON.stringify(voDir)} + "/" + item["file"] + ".wav"
    mp3 = ${JSON.stringify(voDir)} + "/" + item["file"] + ".mp3"
    sf.write(wav, audio, 24000)
    subprocess.run(["ffmpeg","-y","-i",wav,"-ar","44100","-b:a","192k",mp3], capture_output=True)
    subprocess.run(["rm", wav])
    print("  ok", item["file"], round(len(audio)/24000,1), "s", flush=True)
`;
  runPy(CONFIG.kokoroPython, py, { filter: 'grep -v -i warn || true' });
  fs.unlinkSync(tmp);
  log.ok(`${sections.length} VO files generated`);
  return checkRuntime(slug, sections, voDir, totalWords);
}

/**
 * The projection uses an average rate; Kokoro's real pace swings ±6% with
 * sentence length. This checks the ACTUAL audio — it is the gate that matters,
 * and it runs whether or not the VO was regenerated.
 */
function checkRuntime(slug, sections, voDir, totalWords) {
  const secs = sections.reduce((a, s) => a + duration(path.join(voDir, `${fileFor(s)}.mp3`)), 0);
  const nAds = (readManifest(slug).adAfter || []).length;
  const runtime = CONFIG.lead + secs
    + (sections.length - 1 - nAds) * CONFIG.pad + nAds * CONFIG.adGap + CONFIG.endScreen;
  const rate = totalWords / secs;
  log.info(`VO ${(secs / 60).toFixed(2)} min · measured ${rate.toFixed(2)} w/s · runtime ${(runtime / 60).toFixed(2)} min`);
  if (runtime < 495) {
    const need = Math.ceil((500 - runtime) * rate);
    log.warn(c.bold(`RUNTIME ${(runtime / 60).toFixed(2)} min — UNDER THE 8:00 MID-ROLL GATE`));
    log.warn(`add ~${need} words (one more section), then: gj voice ${slug}`);
    log.warn('do NOT proceed to timeline — you would ship a video with no mid-rolls');
  } else {
    log.ok(`clears the 8:00 mid-roll gate by ${((runtime - 480) / 60).toFixed(2)} min`);
  }
  return sections;
}

/** S04b → "04b-slug" style filenames, stable across reruns. */
function fileFor(s) {
  const n = s.id.replace(/^S/i, '').toLowerCase();
  const word = s.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').split('-').slice(0, 2).join('-');
  return `${n}-${word}`;
}

/**
 * Every section's captions must reach the end of its own audio.
 *
 * Two parser bugs have now silently shipped truncated narration, and neither
 * was visible in any existing output — the build reported a word count and
 * carried on. A video went out with 25 seconds of speech and no captions.
 * Alignment that stops well before the audio does is the symptom both bugs
 * share.
 *
 * Runs on the SKIP path too: the case that actually bit us was a stale
 * words.json next to a regenerated mp3, so a guard that only fires when
 * alignment is rebuilt would have missed it entirely.
 */
export function checkCaptionCoverage(dir, wordsPath) {
  const aligned = JSON.parse(fs.readFileSync(wordsPath, 'utf8'));
  const short = [];
  for (const [file, ws] of Object.entries(aligned)) {
    const mp3 = path.join(dir, 'vo', file);
    if (!exists(mp3)) continue;
    const audio = duration(mp3);
    const to = ws.length ? ws[ws.length - 1].end : 0;
    if (audio - to > 3) short.push([file, to, audio]);
  }
  if (short.length) {
    for (const [file, to, audio] of short)
      log.warn(`${file}: captions stop at ${to.toFixed(1)}s of ${audio.toFixed(1)}s — ${(audio - to).toFixed(1)}s uncaptioned`);
    log.warn('script.md was probably truncated on the way to the VO — do NOT render until this is clean');
  } else {
    log.ok(`words.json — all ${Object.keys(aligned).length} sections captioned to the end`);
  }
  return short;
}

// ---------------------------------------------------------------- align -----
export function align(slug, opts = {}) {
  const dir = videoDir(slug);
  const out = path.join(dir, 'words.json');
  if (exists(out) && !opts.force) { log.skip('words.json'); checkCaptionCoverage(dir, out); return out; }
  const py = `
import json, glob, os, whisper
model = whisper.load_model(${JSON.stringify(CONFIG.whisperModel)})
res = {}
for f in sorted(glob.glob(${JSON.stringify(path.join(dir, 'vo'))} + "/*.mp3")):
    r = model.transcribe(f, word_timestamps=True, language="en")
    ws = []
    for seg in r["segments"]:
        for w in seg.get("words", []):
            ws.append({"w": w["word"].strip(), "start": round(w["start"],3), "end": round(w["end"],3)})
    res[os.path.basename(f)] = ws
    print("  ok", os.path.basename(f), len(ws), "words", flush=True)
json.dump(res, open(${JSON.stringify(out)}, "w"))
`;
  runPy(CONFIG.whisperPython, py, { filter: 'grep -v FP16 || true' });

  checkCaptionCoverage(dir, out);
  return out;
}

// ------------------------------------------------------------- timeline -----
/** Emit vo.gen.ts (section offsets + the global word list) into the shot folder. */
export function timeline(slug, opts = {}) {
  const m = readManifest(slug);
  if (!m.shotDir) throw new Error(`video.json needs "shotDir" (e.g. "long-9") before timeline`);
  const dir = videoDir(slug);
  const voDir = path.join(dir, 'vo');
  const words = JSON.parse(fs.readFileSync(path.join(dir, 'words.json'), 'utf8'));
  const files = fs.readdirSync(voDir).filter((f) => f.endsWith('.mp3')).sort();
  const adAfter = new Set(m.adAfter || []);

  let t = CONFIG.lead;
  const offsets = {}; const all = [];
  for (const f of files) {
    offsets[f] = +t.toFixed(3);
    for (const w of words[f] || []) all.push({ w: w.w, start: +(w.start + t).toFixed(3), end: +(w.end + t).toFixed(3) });
    const stem = f.replace(/\.mp3$/, '');
    t += duration(path.join(voDir, f)) + (adAfter.has(stem) ? CONFIG.adGap : CONFIG.pad);
  }
  const total = +(t - CONFIG.pad + CONFIG.endScreen).toFixed(2);

  const cname = (f) => 'S' + f.split('-')[0].toUpperCase();
  const lines = [
    `// GENERATED by \`gj timeline ${slug}\` — do not hand-edit.`,
    `// Kokoro ${CONFIG.voice}. Ad gaps after: ${[...adAfter].join(', ') || '(none)'}`,
    'export type VoWord = { w: string; start: number; end: number };', '',
    ...files.map((f) => `export const ${cname(f)} = ${offsets[f]}; // ${f} (${duration(path.join(voDir, f)).toFixed(2)}s)`),
    `export const TOTAL = ${total}; // incl. ${CONFIG.endScreen}s end screen`, '',
    'export const VO_WORDS: VoWord[] = [',
    ...all.map((w) => `  { w: ${JSON.stringify(w.w)}, start: ${w.start}, end: ${w.end} },`),
    '];',
  ];
  const shotPath = path.join(REMOTION, 'src', 'shots', m.shotDir);
  ensureDir(shotPath);
  fs.writeFileSync(path.join(shotPath, 'vo.gen.ts'), lines.join('\n') + '\n');

  // stage the audio where Remotion's staticFile() can see it
  const mediaVo = path.join(MEDIA, m.project, 'vo');
  ensureDir(mediaVo);
  for (const f of files) fs.copyFileSync(path.join(voDir, f), path.join(mediaVo, f));

  // ad-break windows, for the master step and the Studio instructions
  const wins = [];
  let acc = CONFIG.lead;
  for (const f of files) {
    acc += duration(path.join(voDir, f));
    if (adAfter.has(f.replace(/\.mp3$/, ''))) { wins.push([+acc.toFixed(2), +(acc + CONFIG.adGap).toFixed(2)]); acc += CONFIG.adGap; }
    else acc += CONFIG.pad;
  }
  m.timeline = { total, offsets, adWindows: wins, sections: files.map((f) => ({ file: f, at: offsets[f] })) };
  writeManifest(slug, m);

  log.ok(`vo.gen.ts → shots/${m.shotDir} · TOTAL ${total}s (${(total / 60).toFixed(2)} min)`);
  if (total < 488) log.warn('under 8:00 + end screen — mid-rolls will be refused');
  wins.forEach(([a, b], i) => log.info(`ad break ${i + 1}: ${fmt(a)} – ${fmt(b)}`));
  return m;
}
const fmt = (s) => `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, '0')}`;

// --------------------------------------------------------------- images -----
/** Generate the Flow cutaways declared in video.json → images[]. */
export function images(slug, opts = {}) {
  const m = readManifest(slug);
  const list = m.images || [];
  if (!list.length) { log.warn('no images[] in video.json — the cutaway rule wants 4–6'); return; }
  if (list.length < 4) log.warn(`only ${list.length} cutaways declared — the rule is 4–6`);
  const out = path.join(MEDIA, m.project, 'images');
  ensureDir(out);
  const todo = list.filter((i) => opts.force || !exists(path.join(out, `${i.name}.png`)));
  if (!todo.length) { log.skip(`${list.length} images`); return; }

  const js = `
import { loadEnv } from "./lib/env.mjs";
loadEnv();
const { flowImage } = await import("./lib/flow.mjs");
const jobs = ${JSON.stringify(todo)};
for (const j of jobs) {
  try { await flowImage(j.prompt, ${JSON.stringify(out)} + "/" + j.name + ".png", { aspectRatio: "16:9" }); console.log("  ok", j.name); }
  catch (e) { console.log("  FAIL", j.name, e.message); }
}
`;
  const tmp = path.join(FORGE, `.gj-flow-${slug}.mjs`);
  fs.writeFileSync(tmp, js);
  try { sh(`node "${tmp}"`, { cwd: FORGE }); } finally { fs.unlinkSync(tmp); }

  // Count what is actually ON DISK, not what we attempted. This printed
  // "✓ 5 Flow cutaways" twice while Flow was failing — once on a reCAPTCHA
  // (4 of 5 landed) and once on a daily quota (0 of 5 landed). A green tick
  // over a missing file is the most expensive kind of wrong.
  const landed = list.filter((i) => exists(path.join(out, `${i.name}.png`)));
  const missing = list.filter((i) => !landed.includes(i)).map((i) => i.name);
  if (missing.length) {
    log.warn(`${landed.length}/${list.length} cutaways on disk — MISSING: ${missing.join(', ')}`);
    if (landed.length < 4) log.warn('under the 4–6 house rule — do NOT render until these exist');
  } else {
    log.ok(`${landed.length} Flow cutaways → media/projects/${m.project}/images`);
  }
}
