#!/usr/bin/env node
// Create or update a Ghost page from an HTML file.
//   node ghost.mjs <slug> "<title>" <file.html>
// Also: node ghost.mjs --shop-card <file.html>   (inserts a card into /templates/)
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { ghostToken } from './ghost-key.mjs';

const BASE = 'https://geniusjunkie.net/ghost/api/admin';

async function req(method, path, body) {
  const r = await fetch(BASE + path, {
    method,
    headers: { Authorization: `Ghost ${ghostToken()}`, 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  const txt = await r.text();
  if (!r.ok) { const e = new Error(`HTTP ${r.status}: ${txt.slice(0, 300)}`); e.status = r.status; throw e; }
  return JSON.parse(txt);
}

export async function upsert(slug, title, html) {
  let existing = null;
  try { existing = (await req('GET', `/pages/slug/${slug}/?formats=html`)).pages[0]; } catch (e) { if (e.status !== 404) throw e; }
  if (existing) {
    const out = await req('PUT', `/pages/${existing.id}/?source=html`,
      { pages: [{ html, title, updated_at: existing.updated_at }] });
    console.log(`  ✓ updated ${out.pages[0].url}`);
  } else {
    const out = await req('POST', '/pages/?source=html',
      { pages: [{ title, slug, html, status: 'published' }] });
    console.log(`  ✓ created ${out.pages[0].url}`);
  }
}

/** Insert a product card into /templates/ before the Template Club upsell. */
export async function shopCard(cardHtml, marker) {
  const p = (await req('GET', '/pages/slug/templates/?formats=html')).pages[0];
  if (p.html.includes(marker)) { console.log('  • shop card already listed'); return; }
  const m = p.html.match(/<h[23][^>]*>[^<]*Template Club[^<]*<\/h[23]>/);
  const html = m ? p.html.slice(0, m.index) + cardHtml + p.html.slice(m.index) : p.html + cardHtml;
  await req('PUT', `/pages/${p.id}/?source=html`, { pages: [{ html, updated_at: p.updated_at }] });
  console.log('  ✓ shop card added to /templates/');
}

// NB: compare decoded paths — this repo lives under a directory with a space
// in it, and import.meta.url percent-encodes it, so a raw string compare
// silently skips the whole CLI block.
if (fileURLToPath(import.meta.url) === path.resolve(process.argv[1] || '')) {
  const a = process.argv.slice(2);
  if (a[0] === '--shop-card') {
    const html = fs.readFileSync(a[1], 'utf8');
    await shopCard(html, a[2] || html.match(/href="([^"]+)"/)?.[1] || '');
  } else {
    const [slug, title, file] = a;
    await upsert(slug, title, fs.readFileSync(file, 'utf8'));
  }
}
