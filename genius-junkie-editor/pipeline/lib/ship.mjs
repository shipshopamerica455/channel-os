// Ship stages: qa → render → master → product → commerce → publish.
import fs from 'fs';
import path from 'path';
import {
  CONFIG, EDITOR, REMOTION, ROOT, UPLOADER, c, log, sh, shOut, kitBase, canvaPlaceholders,
  videoDir, readManifest, writeManifest, exists, ensureDir, duration,
  latestScheduled, nextSlot, plusDaysAt, runPy, occupiedSlots, freeShortSlots,
} from './util.mjs';

// ------------------------------------------------------------------ qa ------
/** Contact sheets at even intervals — you must LOOK at these before rendering. */
/**
 * The composition's `M` map must match video.json's timeline.
 *
 * The marks are hand-written into the composition, and after any partial
 * rebuild (regenerating one VO file, say) every offset downstream of it moves.
 * Copying the map from a stale build put two marks 24 s out on the thank-you
 * cards video: a scene ended early, the ad card played over narration, and a
 * whole section's reveals were misaligned. Nothing caught it — the render
 * succeeded and the master's silence check passed, because the SILENCE was
 * right and only the picture was wrong.
 */
export function checkMarks(slug) {
  const m = readManifest(slug);
  const comp = path.join(REMOTION, 'src', 'shots', m.shotDir, `${fs.readdirSync(path.join(REMOTION, 'src', 'shots', m.shotDir)).find((f) => /^Long\d+/.test(f)) || ''}`);
  if (!exists(comp)) { log.warn('composition file not found — mark check skipped'); return; }
  const src = fs.readFileSync(comp, 'utf8');
  const block = src.match(/const M = \{(.*?)\};/s);
  if (!block) { log.warn('no `const M = {...}` in the composition — mark check skipped'); return; }
  const used = Object.fromEntries([...block[1].matchAll(/(\w+):\s*([\d.]+)/g)].map(([, k, v]) => [k, +v]));
  const offs = Object.values(m.timeline?.offsets || {});
  const wins = m.timeline?.adWindows || [];
  const bad = [];
  offs.forEach((v, i) => {
    const key = `c${String(i + 1).padStart(2, '0')}`;
    if (!(key in used)) return;
    const want = i === 0 ? 0 : v;                 // scene 1 always mounts at 0
    if (Math.abs(used[key] - want) > 0.01) bad.push(`${key} ${used[key]} ≠ ${want}`);
  });
  wins.forEach(([a], i) => {
    const key = `ad${i + 1}`;
    if (key in used && Math.abs(used[key] - a) > 0.01) bad.push(`${key} ${used[key]} ≠ ${a}`);
  });
  if ('end' in used && Math.abs(used.end - (m.timeline?.total || 0)) > 0.01)
    bad.push(`end ${used.end} ≠ ${m.timeline?.total}`);
  if (bad.length) {
    log.warn(`composition marks DRIFTED from the timeline: ${bad.join(' · ')}`);
    log.warn('  regenerate the M map from video.json — do not retype it');
  } else {
    log.ok(`composition marks match the timeline (${offs.length} sections)`);
  }
  return bad;
}

export function qa(slug, opts = {}) {
  checkCutaways(slug);
  checkMarks(slug);
  const m = readManifest(slug);
  const total = m.timeline?.total;
  if (!m.composition || !total) throw new Error('need composition + timeline in video.json');
  // Uniform sampling is too coarse to catch what actually goes wrong: a dead
  // half-frame, or a reveal that lags the narration. 16 frames over 8½ minutes
  // is one every ~32 s. Default to sampling INSIDE each section instead —
  // early / middle / late — so every scene is inspected on its own terms.
  // `--uniform` restores the old behaviour; `--frames N` sets the count.
  const sections = m.timeline?.sections || [];
  let marks;
  if (!opts.uniform && sections.length) {
    const per = Number(opts.perSection) || 3;
    const bounds = sections.map((s, i) => [s.at, sections[i + 1]?.at ?? total]);
    marks = bounds.flatMap(([a, b]) => {
      const span = b - a;
      // skip the first ~2 s (fade-in) and the last ~1.5 s (hand-over)
      const lo = a + Math.min(2.2, span * 0.15);
      const hi = b - Math.min(1.5, span * 0.12);
      if (hi <= lo) return [Math.round(((a + b) / 2) * 30)];
      return Array.from({ length: per }, (_, i) =>
        Math.round((lo + (hi - lo) * (per === 1 ? 0.5 : i / (per - 1))) * 30));
    });
  } else {
    const n = Number(opts.frames) || 16;
    marks = Array.from({ length: n }, (_, i) => Math.round((total * 30) * ((i + 0.5) / n)));
  }
  marks = [...new Set(marks)].sort((a, b) => a - b);
  log.info(`qa · ${marks.length} frames${opts.uniform || !sections.length ? '' : ` across ${sections.length} sections`}`);
  // NB: never `remotion render` the composition here — it writes out/<comp>.mp4
  // at --scale, and render() would then skip it and ship a half-size master.
  sh(`node scripts/frames.mjs ${m.composition} ${marks.join(',')} --scale=0.5`, { cwd: REMOTION });
  // Label every tile with its section and timestamp — "S07 · 4:11" is what you
  // need to jump to in the scene file; a bare frame number is not.
  const labels = {};
  for (const f of marks) {
    const t = f / 30;
    const idx = sections.length
      ? Math.max(0, sections.findIndex((s, i) => t >= s.at && t < (sections[i + 1]?.at ?? total)))
      : -1;
    const name = idx > -1 ? `S${String(idx + 1).padStart(2, '0')}` : '';
    labels[f] = `${name} · ${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
  }
  const py = `
from PIL import Image, ImageDraw
import glob, re, os, json
qa = ${JSON.stringify(path.join(REMOTION, 'out', 'qa'))}
labels = json.loads(${JSON.stringify(JSON.stringify(labels))})
keep = set(int(k) for k in labels)
fs_ = sorted(
    (f for f in glob.glob(qa + "/${m.composition}-f*.png")
     if int(re.search(r'f(\\d+)', f).group(1)) in keep),
    key=lambda f: int(re.search(r'f(\\d+)', f).group(1)))
COLS, ROWS, W, H = 3, 3, 640, 360
per = COLS * ROWS
sheets = (len(fs_) + per - 1) // per
for s in range(sheets):
    b = fs_[s*per:(s+1)*per]
    if not b: break
    sheet = Image.new('RGB', (W*COLS, H*ROWS), '#181c22'); d = ImageDraw.Draw(sheet)
    for i, f in enumerate(b):
        im = Image.open(f).resize((W, H)); x, y = (i%COLS)*W, (i//COLS)*H
        sheet.paste(im, (x, y))
        n = int(re.search(r'f(\\d+)', f).group(1))
        tag = labels.get(str(n), str(n))
        d.rectangle([x, y, x+230, y+26], fill='#000')
        d.text((x+8, y+8), tag, fill='#ffdd00')
        d.rectangle([x, y, x+W-1, y+H-1], outline='#2b3340')
    sheet.save(f"{qa}/SHEET-${slug}-{s}.png")
print("sheets:", sheets, "frames:", len(fs_))
`;
  runPy(CONFIG.python, py);
  log.ok(`QA sheets → remotion/out/qa/SHEET-${slug}-*.png ${c.yellow('— READ THEM before render')}`);
}

// -------------------------------------------------------------- render ------
/**
 * Every Flow cutaway that was generated must actually appear in a scene.
 * Three videos shipped with unplaced images before this existed — the photo
 * album went out with three cutaways against a house rule of four to six —
 * because video.json lists the prompts and the scenes are written separately,
 * and nothing compared them.
 */
export function checkCutaways(slug) {
  const m = readManifest(slug);
  const dir = path.join(REMOTION, '..', 'media', 'projects', m.project, 'images');
  if (!exists(dir)) return { used: 0, unused: [] };
  const shots = path.join(REMOTION, 'src', 'shots', m.shotDir);
  const src = fs.readdirSync(shots)
    .filter((f) => f.endsWith('.tsx'))
    .map((f) => fs.readFileSync(path.join(shots, f), 'utf8'))
    .join('\n');
  const imgs = fs.readdirSync(dir).filter((f) => f.endsWith('.png'));
  const unused = imgs.filter((f) => !src.includes(`${m.project}/images/${f}`));
  const used = imgs.length - unused.length;
  if (unused.length) {
    log.warn(`${unused.length} generated cutaway(s) NEVER PLACED in a scene: ${unused.join(', ')}`);
    log.warn(`  only ${used} cutaways in the video — the house rule is 4–6. Place them or drop them from video.json.`);
  } else {
    log.ok(`all ${used} cutaways placed`);
  }
  return { used, unused };
}

export function render(slug, opts = {}) {
  const m = readManifest(slug);
  checkCutaways(slug);
  const raw = path.join(REMOTION, 'out', `${m.composition}.mp4`);
  // a stale half-size file must never be mistaken for a finished master
  // ffprobe prints "1920,\n" here — csv=p=0 leaves a trailing comma, and
  // `-select_streams v` can match more than one stream. Comparing the raw
  // string to '1920' therefore NEVER matched, so `full` was always false and
  // every `gj render` silently re-rendered the finished long-form from
  // scratch (~20 min) behind a "not 1920 wide" warning. Parse the number.
  const probedWidth = exists(raw) ? parseInt(shOut(
    `ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "${raw}"`).trim(), 10) : 0;
  const full = probedWidth === 1920;
  if (full && !opts.force) { log.skip(`${m.composition}.mp4`); }
  else {
    if (exists(raw) && !full) log.warn(`${m.composition}.mp4 is not 1920 wide — re-rendering`);
    sh(`npx remotion render ${m.composition} out/${m.composition}.mp4 --concurrency=8 --log=error`, { cwd: REMOTION });
    log.ok(`rendered ${m.composition}.mp4 (${(fs.statSync(raw).size / 1e6).toFixed(0)} MB)`);
  }
  for (const p of m.promos || []) {
    const f = path.join(REMOTION, 'out', `${p}.mp4`);
    if (exists(f) && !opts.force) { log.skip(`${p}.mp4`); continue; }
    sh(`npx remotion render ${p} out/${p}.mp4 --concurrency=8 --log=error`, { cwd: REMOTION });
    log.ok(`rendered ${p}.mp4`);
  }
  if (m.thumb) {
    sh(`node scripts/frames.mjs ${m.thumb} 0 --scale=1`, { cwd: REMOTION, quiet: true });
    log.ok(`thumbnail ${m.thumb}`);
  }
  return raw;
}


// --------------------------------------------------------------- music ------
/**
 * Render the optional music bed. OPT-IN by construction: nothing changes for
 * a video until `bed.wav` exists in its folder, and `master` only mixes a bed
 * it can find. Published videos are unaffected — a YouTube file cannot be
 * swapped, so this only ever applies to the next render.
 *
 * The generator is procedural and local (numpy/scipy, no API, no licence) —
 * see pipeline/audio/make_bed.py for how the plan is shaped and why it stops
 * dead at both ad windows.
 */
export function music(slug, opts = {}) {
  const dir = videoDir(slug);
  const bed = path.join(dir, 'bed.wav');
  if (exists(bed) && !opts.force) { log.skip('bed.wav'); return bed; }
  const script = path.join(EDITOR, 'pipeline', 'audio', 'make_bed.py');
  sh(`"${CONFIG.python}" "${script}" "${dir}"${opts.audition ? ' --audition' : ''}`);
  log.ok('bed.wav — mix it by re-running `master --force`');
  return bed;
}

// -------------------------------------------------------------- master ------
/** Mute the designed ad windows, normalise, verify the silence actually landed. */
export function master(slug, opts = {}) {
  const m = readManifest(slug);
  const dir = videoDir(slug);
  const raw = path.join(REMOTION, 'out', `${m.composition}.mp4`);
  const out = path.join(dir, 'final.mp4');
  const { I, TP, LRA } = CONFIG.loudness;

  // Skip only the LONG-FORM encode, never the whole stage. This used to be an
  // early `return`, so a master interrupted after writing final.mp4 could never
  // produce its Shorts or thumbnail without a full --force re-encode — which is
  // exactly what happened when a session restart killed it mid-run. The Shorts
  // loop and the thumbnail copy below are already idempotent on their own.
  if (exists(out) && !opts.force) {
    log.skip('final.mp4');
  } else {
    const wins = m.timeline?.adWindows || [];
    const mutes = wins.map(([a, b]) => `volume=enable='between(t,${a},${b})':volume=0`).join(',');
    const af = [mutes, `loudnorm=I=${I}:TP=${TP}:LRA=${LRA}`].filter(Boolean).join(',');

    // A music bed is mixed in ONLY if `gj music <slug>` has made one. The mute
    // and the loudnorm are applied AFTER the mix, never before, so the ad
    // windows are silent in the delivered file whatever the bed is doing —
    // `silencedetect` below is checking the real output, and YouTube refuses
    // manual mid-rolls where the audio is not silent.
    const bed = path.join(dir, 'bed.wav');
    if (exists(bed)) {
      const fc = `[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mix];`
        + `[mix]${af}[a]`;
      sh(`ffmpeg -y -i "${raw}" -i "${bed}" -filter_complex "${fc}" -map 0:v -map "[a]" `
        + `-c:v copy -c:a aac -b:a 192k "${out}" 2>&1 | grep -E "Qavg" || true`);
      log.ok('music bed mixed');
    } else {
      sh(`ffmpeg -y -i "${raw}" -af "${af}" -c:v copy -c:a aac -b:a 192k "${out}" 2>&1 | grep -E "Qavg" || true`);
    }

    // verify each declared ad window is genuinely silent
    const det = shOut(`ffmpeg -i "${out}" -af silencedetect=n=-45dB:d=1.0 -f null - 2>&1 | grep silence_start || true`);
    const starts = [...det.matchAll(/silence_start: ([\d.]+)/g)].map((x) => parseFloat(x[1]));
    let allGood = true;
    wins.forEach(([a], i) => {
      const hit = starts.some((s) => Math.abs(s - a) < 1.2);
      if (hit) log.ok(`ad break ${i + 1} silent at ${a}s`);
      else { log.warn(`ad break ${i + 1} at ${a}s NOT detected as silent — check for SFX bleeding in`); allGood = false; }
    });
    if (!allGood) log.warn('YouTube may refuse manual mid-rolls where the audio is not silent');
  }

  // promo shorts
  const shortsDir = path.join(dir, 'shorts');
  ensureDir(shortsDir);
  (m.promos || []).forEach((p, i) => {
    const name = (m.promoNames || {})[p] || `promo-${i + 1}`;
    const dst = path.join(shortsDir, `${name}.mp4`);
    if (exists(dst) && !opts.force) return;
    sh(`ffmpeg -y -i "${path.join(REMOTION, 'out', `${p}.mp4`)}" -af "loudnorm=I=${I}:TP=${TP}:LRA=${LRA}" -c:v copy -c:a aac -b:a 192k "${dst}" 2>&1 | grep Qavg || true`);
    log.ok(`short → ${name}.mp4`);
  });

  const thumbSrc = path.join(REMOTION, 'out', 'qa', `${m.thumb}-f0000.png`);
  if (exists(thumbSrc)) fs.copyFileSync(thumbSrc, path.join(dir, 'thumbnail-A.png'));
  log.ok(`final.mp4 · ${duration(out).toFixed(1)}s`);
  return out;
}

// ------------------------------------------------------------- product ------
export function product(slug, opts = {}) {
  const m = readManifest(slug);
  const dir = path.join(videoDir(slug), 'product');
  if (!exists(dir)) { log.warn('no product/ folder — skipping'); return; }
  const maker = fs.readdirSync(dir).find((f) => /^make_.*\.py$/.test(f));
  if (maker) { sh(`"${CONFIG.python}" "${path.join(dir, maker)}"`); log.ok(`ran ${maker}`); }
  const pdfs = fs.readdirSync(dir).filter((f) => f.endsWith('.pdf'));
  if (!pdfs.length) { log.warn('no PDFs produced'); return; }
  const remote = `/var/www/ghost/content/files/${kitBase()}/${m.product?.folder || slug}`;
  sh(`ssh ${CONFIG.server} "sudo mkdir -p ${remote} && sudo chown -R ubuntu:ubuntu ${remote}"`, { quiet: true });
  sh(`scp ${pdfs.map((f) => `"${path.join(dir, f)}"`).join(' ')} ${CONFIG.server}:${remote}/ >/dev/null`);
  sh(`ssh ${CONFIG.server} "sudo chown -R ghost:ghost ${remote}"`, { quiet: true });
  log.ok(`${pdfs.length} PDFs → ${remote}`);
}

// ------------------------------------------------------------ commerce ------
/** Stripe product/price/link (key never leaves the server) + Ghost pages. */
export function commerce(slug, opts = {}) {
  const m = readManifest(slug);
  const p = m.product || {};
  if (!p.name) { log.warn('product.name missing in video.json — skipping commerce'); return; }
  if (p.stripe && !opts.force) { log.skip(`Stripe link ${p.stripe}`); }
  else {
    const thanks = `${CONFIG.site}/${p.slug || slug}-thank-you/`;
    const script = `SK=$(sudo mysql -N -B ghost_db -e "SELECT value FROM settings WHERE \\\`key\\\`=\\"stripe_connect_secret_key\\";" | head -1)
PROD=$(curl -s https://api.stripe.com/v1/products -u "$SK:" -d name=${sq(p.name)} -d description=${sq(p.description || p.name)} | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")
PRICE=$(curl -s https://api.stripe.com/v1/prices -u "$SK:" -d product="$PROD" -d unit_amount=${p.amount || 499} -d currency=${p.currency || 'gbp'} | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")
LINK=$(curl -s https://api.stripe.com/v1/payment_links -u "$SK:" -d "line_items[0][price]=$PRICE" -d "line_items[0][quantity]=1" -d "after_completion[type]=redirect" -d "after_completion[redirect][url]=${thanks}" | python3 -c "import sys,json;print(json.load(sys.stdin)['url'])")
echo "$PROD|$PRICE|$LINK"`;
    const res = shOut(`ssh ${CONFIG.server} ${sq(script)}`).trim().split('\n').pop();
    const [prod, price, link] = res.split('|');
    m.product = { ...p, stripeProduct: prod, stripePrice: price, stripe: link };
    writeManifest(slug, m);
    log.ok(`Stripe live — ${link}`);
  }

  for (const page of ['landing', 'thankYou']) {
    const html = (m.pages || {})[page];
    if (!html) { log.warn(`pages.${page} not set in video.json — write the HTML and re-run`); continue; }
    const file = path.join(videoDir(slug), html);
    if (!exists(file)) { log.warn(`missing ${html}`); continue; }
    const slugName = page === 'landing' ? (p.slug || slug) : `${p.slug || slug}-thank-you`;
    const title = page === 'landing' ? p.name : `Your ${p.name} — Downloads`;
    // the pages are written before Stripe/Canva exist — fill the placeholders now
    const prod = readManifest(slug).product || {};
    const raw = fs.readFileSync(file, 'utf8');
    // KIT_BASE keeps the rotated kit prefix out of the page sources, which sit in
    // a repo with a public GitHub remote. It resolves from kit-base.json.
    const kits = `${CONFIG.site}/content/files/${kitBase()}`;
    // The Canva links are the product, so they are not in the page source or in
    // video.json either — they resolve from gitignored canva-links.json.
    const canva = canvaPlaceholders(slug);
    const subs = [['STRIPE_LINK', prod.stripe], ...Object.entries(canva), ['KIT_BASE', kits]]
      // CANVA_LINK is a PREFIX of CANVA_LINK_DESKTOP. Replacing the short one
      // first turns the long one into `<url>_DESKTOP` — a dead link on a page a
      // buyer has already paid for. Longest placeholder always wins.
      .sort((a, b) => b[0].length - a[0].length);
    const missing = subs.filter(([ph, val]) => !val && raw.includes(ph)).map(([ph]) => ph);
    // a CANVA_LINK_* the store has no key for would otherwise survive into the
    // published href, which the check above cannot see
    const unknown = [...new Set(raw.match(/CANVA_LINK[A-Z_]*/g) || [])].filter((ph) => !canva[ph]);
    if (missing.length || unknown.length) {
      // never publish a paid page with a dead link in it
      const what = [...missing, ...unknown].join(' + ');
      log.warn(`NOT publishing ${html} — ${what} unresolved. Stripe links go in video.json → product; ` +
        `Canva links go in pipeline/canva-links.json → links.${slug}. Then: gj commerce ${slug}`);
      continue;
    }
    const body = subs.reduce((s, [ph, val]) => s.replaceAll(ph, val), raw);
    const tmp = path.join(videoDir(slug), `.${page}.resolved.html`);
    fs.writeFileSync(tmp, body);
    // ghost.mjs talks to the admin API straight from this Mac, and Cloudflare
    // has 403'd that path since the zone went live — it took the pattern kit's
    // landing page down mid-commerce. ghost-ssh.mjs runs the same call ON the
    // server with --resolve, which never touches Cloudflare.
    sh(`node "${path.join(EDITOR, 'pipeline', 'lib', 'ghost-ssh.mjs')}" ${slugName} ${sq(title)} "${tmp}"`);
    fs.unlinkSync(tmp);
  }

  // the pages are live — now make sure somebody can actually find them
  checkListed(slug);
}
const sq = (s) => `'${String(s).replace(/'/g, `'\\''`)}'`;

// ------------------------------------------------------------- publish ------
/** Always private + publishAt. Never flips anything public. */
export function publish(slug, opts = {}) {
  const m = readManifest(slug);
  const dir = videoDir(slug);
  if (!exists(path.join(dir, 'final.mp4'))) throw new Error('no final.mp4 — run master first');
  if (!exists(path.join(dir, 'packaging.json'))) throw new Error('no packaging.json — write SEO.md + packaging.json first');
  checkListed(slug);   // never publish a video pointing at an unlisted page

  const when = m.publishAt || nextSlot(latestScheduled());
  const pkg = JSON.parse(fs.readFileSync(path.join(dir, 'packaging.json'), 'utf8'));

  // Shorts used to be placed blindly on the following days at 12:00. With four
  // shorts per video and a 2-day long-form cadence that collides EVERY time on
  // days +3 and +4 — the previous two releases both had to be unpicked by hand.
  // Ask what is actually occupied, then walk the ladder for free slots.
  const { slots: occupied, source } = occupiedSlots();
  log.ok(`schedule read from ${source} — ${occupied.size} slot(s) occupied`);
  if (occupied.has(new Date(when).toISOString()))
    throw new Error(`long-form slot ${when} is ALREADY TAKEN — pick another date`);
  occupied.add(new Date(when).toISOString());

  pkg.publishAt = when;
  const names = Object.keys(pkg.shorts || {});
  const picked = freeShortSlots(when, names.length, occupied);
  names.forEach((n, i) => { pkg.shorts[n].publishAt = picked[i]; });
  picked.forEach((p, i) => log.ok(`  short ${i + 1} → ${p.slice(0, 16).replace('T', ' ')}`));
  fs.writeFileSync(path.join(dir, 'packaging.json'), JSON.stringify(pkg, null, 2) + '\n');
  m.publishAt = when; writeManifest(slug, m);

  if (opts.dryRun) { log.warn(`DRY RUN — would upload, public at ${when}`); return; }
  sh(`node "${UPLOADER}" "${dir}" --publish-at "${when}" --title ${opts.title || 'A'} --shorts`);
  log.ok(`uploaded as PRIVATE drafts · long-form goes public ${when}`);
}

// ------------------------------------------------------------- notify -------
/** The one-click handover: what you still have to do, in order. */
export function notify(slug) {
  const m = readManifest(slug);
  const dir = videoDir(slug);
  const seo = path.join(dir, 'SEO.md');
  const mid = (m.timeline?.adWindows || []).map(([a]) => `${Math.floor(a / 60)}:${(a % 60).toFixed(1).padStart(4, '0')}`);
  // anything the pipeline could not finish on its own, stated plainly
  const blockers = [];
  const p = m.product || {};
  const needsCanva = ['landing', 'thankYou'].some((k) => {
    const f = (m.pages || {})[k];
    return f && exists(path.join(dir, f)) && fs.readFileSync(path.join(dir, f), 'utf8').includes('CANVA_LINK');
  });
  const canvaReady = Boolean(canvaPlaceholders(m.slug).CANVA_LINK);
  if (needsCanva && !canvaReady) {
    blockers.push(`**Create the Canva template link** (Canva UI only): open the design → Share → Template link → Create → Copy.
   Put it in \`pipeline/canva-links.json\` → \`links.${m.slug}.canvaTemplate\` (gitignored — it is the product), then run \`node pipeline/gj.mjs commerce ${m.slug}\`.
   Until then the **thank-you page is not published** — buyers would land on a dead link.`);
  }
  // The header used to claim "Uploaded as private drafts" unconditionally — it
  // is written by `notify`, which runs whether or not `publish` ever did, so on
  // every build that stopped at master it stated the one thing that had not
  // happened. Read the real answer out of packaging.json.
  const pkgPath = path.join(dir, 'packaging.json');
  const pkg = exists(pkgPath) ? JSON.parse(fs.readFileSync(pkgPath, 'utf8')) : {};
  const uploaded = Boolean(pkg.longformId);

  const shopUrl = p.stripe || (p.existing ? `${CONFIG.site}/${p.existing}/` : null);
  const steps = [
    `**Watch it** — \`videos/${m.slug}/final.mp4\``,
    `${uploaded ? 'In' : 'Once it is uploaded, in'} YouTube Studio, on the long-form:
   - Monetisation → mid-rolls **MANUAL**, place at **${mid.join('** and **') || 'see SEO.md'}**, automatic **OFF**
   - Confirm the scheduled date: **${m.publishAt || 'not set'}**`,
    'After it goes public: pin the comment from `SEO.md`',
    `Shop: ${shopUrl || '(no Stripe link)'} — check the buy button once`,
    ...blockers,
  ];

  // "Done already" used to be a fixed string claiming Stripe, the landing page
  // and the thank-you page every time — including on the three videos where
  // commerce was deliberately never run because they point at an existing pack.
  // A handover that reports what a full pipeline WOULD have done is worse than
  // no handover. Report what is actually on disk and in the manifest.
  const shortsDir = path.join(dir, 'shorts');
  const nShorts = exists(shortsDir)
    ? fs.readdirSync(shortsDir).filter((f) => f.endsWith('.mp4')).length : 0;
  const prodDir = path.join(dir, 'product');
  const nPdfs = exists(prodDir)
    ? fs.readdirSync(prodDir).filter((f) => f.endsWith('.pdf')).length : 0;

  const done = [];
  if (exists(path.join(dir, 'final.mp4')))
    done.push(`render + master — \`final.mp4\` ${duration(path.join(dir, 'final.mp4')).toFixed(1)}s, ad windows verified silent`);
  if (exists(path.join(dir, 'thumbnail-A.png'))) done.push('thumbnail');
  if (nShorts) done.push(`${nShorts} Short${nShorts === 1 ? '' : 's'} mastered`);
  if (m.freeAsset?.slug) done.push(`free rung — \`${CONFIG.site}/${m.freeAsset.slug}/\``);
  if (p.existing) {
    done.push(`points at the EXISTING pack \`${p.existing}\` — commerce deliberately not run`);
  } else {
    if (nPdfs) done.push(`${nPdfs} pack PDFs`);
    if (p.stripe) done.push('Stripe product + price + payment link');
    if (p.slug && p.stripe) done.push(`landing page \`${CONFIG.site}/${p.slug}/\``);
    if (canvaReady) done.push('thank-you page (template link resolved)');
  }

  const notDone = [];
  if (!p.existing && p.slug && !canvaReady)
    notDone.push('the **thank-you page** — held until the Canva template link exists, so buyers cannot land on a dead link');

  const body = `# ${m.topic || m.slug} — ready for you

${uploaded
  ? 'Uploaded as **private drafts**. Nothing is public. Your move:'
  : '**Nothing has been uploaded yet** — this is built and mastered on the Mac only. Your move:'}

${steps.map((s, i) => `${i + 1}. ${s}`).join('\n')}

## Done already
${done.length ? done.map((d) => `- ${d}`).join('\n') : '- (nothing recorded)'}
${notDone.length ? `\n## Not done\n${notDone.map((d) => `- ${d}`).join('\n')}\n` : ''}
_Generated ${new Date().toISOString()}_
`;
  // Handovers belong where Annieth works, not in the repo. Named per video so
  // one release cannot overwrite the previous one's outstanding tasks. Falls
  // back to the video folder if the channel drive is not mounted.
  let dest = path.join(dir, 'NEXT-ACTIONS.md');
  if (CONFIG.handovers && exists(CONFIG.handovers)) {
    dest = path.join(CONFIG.handovers, `NEXT-ACTIONS-${m.slug}.md`);
  } else if (CONFIG.handovers) {
    log.warn(`handovers folder not found (${CONFIG.handovers}) — writing into the video folder instead`);
  }
  fs.writeFileSync(dest, body);
  console.log('\n' + c.bold(c.green('═══ READY ═══')));
  console.log(body.split('\n').slice(2).join('\n'));
  log.ok(`handover → ${dest}`);
}

// -------------------------------------------------------- checkListed ------
/**
 * A product that exists but is not LISTED earns nothing. It has happened twice:
 * the Seamless Pattern Kit sat live with a working Stripe link and no entry on
 * /templates/ for days, and two free checklists were missing from
 * /free-canva-resources/ at the same time. Both times the Monday audit found
 * it, which is days too late — the video promoting it had already gone out.
 *
 * So shipping now stops here. The page must appear on the page that exists to
 * list it before the video that points at it can be published.
 *
 * Reads through the ORIGIN over ssh, not from this Mac: Cloudflare 403s the
 * admin path from here, which is the same reason commerce shells out to
 * ghost-ssh.mjs.
 */
export function checkListed(slug) {
  const m = readManifest(slug);
  const p = m.product || {};
  const want = [];
  // product.existing means an already-built pack, already listed — nothing new.
  if (p.slug && !p.existing) want.push({ slug: p.slug, page: '/templates/', what: `product "${p.name || p.slug}"` });
  if (m.freeAsset && m.freeAsset.slug)
    want.push({ slug: m.freeAsset.slug, page: '/free-canva-resources/', what: `free checklist "${m.freeAsset.name || m.freeAsset.slug}"` });
  if (!want.length) { log.info('nothing new to list'); return; }

  const script = want.map((w) =>
    `echo "${w.slug}|$(curl -sk --resolve geniusjunkie.net:443:127.0.0.1 '${CONFIG.site}${w.page}' | grep -c '/${w.slug}/')"`).join('\n');
  const seen = Object.fromEntries(shOut(`ssh ${CONFIG.server} ${sq(script)}`).trim().split('\n')
    .filter(Boolean).map((l) => l.split('|')));

  const unlisted = want.filter((w) => !Number(seen[w.slug] || 0));
  for (const w of want) if (!unlisted.includes(w)) log.ok(`listed on ${w.page} — ${w.slug}`);
  if (!unlisted.length) return;

  for (const w of unlisted) log.warn(`NOT LISTED on ${w.page} — ${w.what}`);
  throw new Error(
    `${unlisted.length} page(s) exist but are invisible. Add ${unlisted.map((w) => w.slug).join(', ')} ` +
    `to ${[...new Set(unlisted.map((w) => w.page))].join(' and ')}, then re-run. ` +
    `Nobody can buy or download what is not linked, and the video pointing at it is about to go out.`);
}
