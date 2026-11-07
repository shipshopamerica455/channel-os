#!/usr/bin/env node
/**
 * Append one link to the /checklists/ hub, idempotently.
 *   node ghost-hub.mjs <page-slug> "<link text>" "<trailing description>"
 *
 * Lives here rather than in the scratchpad because it is needed once per video
 * and the scratchpad is cleared between days.
 *
 * Idempotency matches on the SLUG in the href — never on a class attribute,
 * which Ghost strips on the HTML round-trip (that bug appended a link four
 * times to five pages). Reads back and reports the count.
 */
import { execFileSync } from 'child_process';
import { ghostToken } from './ghost-key.mjs';

const API = 'https://geniusjunkie.net/ghost/api/admin';
const RES = '--resolve geniusjunkie.net:443:127.0.0.1';   // bypass Cloudflare's bot challenge
const HOST = 'geniusjunkie';
const call = (m, path, body) => JSON.parse(execFileSync('ssh', ['-o', 'BatchMode=yes', HOST,
  `curl -s ${RES} -X ${m} "${API}${path}" -H "Authorization: Ghost ${ghostToken()}" -H "Content-Type: application/json" -H "Accept-Version: v5.0"` + (body ? ' --data-binary @-' : '')],
  { input: body ? JSON.stringify(body) : undefined, encoding: 'utf8', maxBuffer: 20e6 }));

const [slug, text, desc] = process.argv.slice(2);
const p = call('GET', '/pages/slug/checklists/?formats=html').pages[0];
if (p.html.includes(`/${slug}/`)) { console.log(`• ${slug} already listed`); process.exit(0); }
const add = `<p><a href="https://geniusjunkie.net/${slug}/">${text}</a> — ${desc}</p>`;
const r = call('PUT', `/pages/${p.id}/?source=html`, { pages: [{ html: p.html + add, updated_at: p.updated_at }] });
if (r.errors) { console.error('✗', JSON.stringify(r.errors).slice(0, 300)); process.exit(1); }
const after = call('GET', '/pages/slug/checklists/?formats=html').pages[0];
console.log(`✓ added — appears ${(after.html.match(new RegExp(slug, 'g')) || []).length} time(s)`);
