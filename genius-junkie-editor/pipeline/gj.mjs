#!/usr/bin/env node
/**
 * gj — the Genius Junkie production pipeline.
 *
 *   node pipeline/gj.mjs <command> <slug> [flags]
 *
 * The creative stages (script, scenes) are yours. Everything mechanical is here.
 *
 *   brief <slug>     scaffold the folder + research brief from the slate
 *   build <slug>     voice → align → timeline → images   (after script.md exists)
 *   qa <slug>        contact sheets — LOOK at these before rendering
 *   ship <slug>      render → master → product → commerce → publish → notify
 *   status           where every video in the slate stands
 *   audit            diff what exists against what is linked; the buyer's path; the comment backlog
 *   listed <slug>    is this video's product/checklist actually linked anywhere? (ship gate)
 *
 *   voice|align|timeline|images|render|master|product|commerce|publish  run one stage
 *   music <slug>     optional procedural music bed (then `master --force` to mix it in)
 *
 * Flags: --force  redo a stage that already has output
 *        --dry-run  (publish) don't actually upload
 *        --title A|B|C  which title option to publish under
 *
 * Nothing here ever makes a video public. Uploads are private drafts with a
 * publishAt date; you flip them yourself after watching.
 */
import fs from 'fs';
import path from 'path';
import { brief, voice, align, timeline, images } from './lib/build.mjs';
import { qa, render, master, music, product, commerce, publish, notify, checkCutaways, checkListed } from './lib/ship.mjs';
import { audit } from './lib/audit.mjs';
import { EDITOR, c, log, readManifest, exists, videoDir, latestScheduled } from './lib/util.mjs';

const argv = process.argv.slice(2);
const cmd = argv[0];
const slug = argv.find((a, i) => i > 0 && !a.startsWith('--'));
const flag = (n) => argv.includes(`--${n}`);
const val = (n) => { const i = argv.indexOf(`--${n}`); return i > -1 ? argv[i + 1] : undefined; };
const opts = {
  force: flag('force'), dryRun: flag('dry-run'), title: val('title'),
  uniform: flag('uniform'), frames: val('frames'), perSection: val('per-section'),
};

function need(s) { if (!s) { console.error(c.red('missing <slug>')); process.exit(1); } return s; }

function status() {
  const dir = path.join(EDITOR, 'videos');
  const rows = [];
  for (const s of fs.readdirSync(dir).sort()) {
    const d = path.join(dir, s);
    if (!fs.statSync(d).isDirectory()) continue;
    const has = (f) => exists(path.join(d, f));
    let pub = '';
    try { pub = JSON.parse(fs.readFileSync(path.join(d, 'packaging.json'), 'utf8')).publishAt || ''; } catch {}
    rows.push({
      slug: s,
      script: has('script.md') ? '✓' : '·',
      vo: has('vo') && fs.readdirSync(path.join(d, 'vo')).some((f) => f.endsWith('.mp3')) ? '✓' : '·',
      words: has('words.json') ? '✓' : '·',
      final: has('final.mp4') ? '✓' : '·',
      shorts: has('shorts') ? String(fs.readdirSync(path.join(d, 'shorts')).filter((f) => f.endsWith('.mp4')).length) : '·',
      publish: pub ? pub.slice(0, 16).replace('T', ' ') : '—',
    });
  }
  const w = Math.max(...rows.map((r) => r.slug.length), 6);
  console.log(`\n${c.bold('slug'.padEnd(w))}  script  vo  words  final  shorts  scheduled`);
  console.log('─'.repeat(w + 44));
  for (const r of rows) {
    console.log(`${r.slug.padEnd(w)}    ${r.script}      ${r.vo}    ${r.words}      ${r.final}      ${r.shorts}     ${r.publish}`);
  }
  const last = latestScheduled();
  console.log(`\n${c.dim(`latest scheduled: ${last ? last.slice(0, 16).replace('T', ' ') + ' UTC' : 'none'}`)}\n`);
}

const CHAIN = {
  build: [
    ['voice', voice], ['align', align], ['timeline', timeline], ['images', images],
  ],
  ship: [
    ['render', render], ['master', master], ['product', product],
    ['commerce', commerce], ['publish', publish],
  ],
};

async function runChain(name, s) {
  for (const [label, fn] of CHAIN[name]) {
    log.step(`${name} · ${label}`);
    await fn(s, opts);
  }
  if (name === 'ship') notify(s);
}

const single = { voice, align, timeline, images, qa, render, master, music, product, commerce, publish, notify, cutaways: checkCutaways };

try {
  switch (cmd) {
    case 'brief': brief(need(slug), { ...opts, topic: val('topic') }); break;
    case 'build': await runChain('build', need(slug)); break;
    case 'ship': await runChain('ship', need(slug)); break;
    case 'status': case undefined: status(); break;
    case 'audit': await audit(); break;
    case 'listed': checkListed(slug); break;
    case 'all': {
      const s = need(slug);
      await runChain('build', s);
      log.step('ship · qa');
      qa(s, opts);
      console.log(c.yellow('\n  Read the QA sheets, then: node pipeline/gj.mjs ship ' + s + '\n'));
      break;
    }
    default: {
      if (single[cmd]) { log.step(cmd); await single[cmd](need(slug), opts); }
      else { console.error(`unknown command: ${cmd}\n`); console.log(fs.readFileSync(new URL(import.meta.url), 'utf8').split('*/')[0].split('/**')[1]); process.exit(1); }
    }
  }
} catch (e) {
  console.error(`\n${c.red('✗ ' + e.message)}\n`);
  process.exit(1);
}
