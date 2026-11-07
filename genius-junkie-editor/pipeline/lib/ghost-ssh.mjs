#!/usr/bin/env node
/**
 * Ghost admin API, called FROM THE SERVER over ssh.
 *
 *   node ghost-ssh.mjs <slug> "<title>" <file.html> [--members]
 *
 * Why this exists: since the Cloudflare zone went live, hitting
 * https://geniusjunkie.net/ghost/api/admin/ from this machine returns a 403
 * "Just a moment..." JS challenge — Cloudflare bot protection sees an API
 * client with no browser. `ghost.mjs` therefore fails on every call.
 *
 * Curling 127.0.0.1:2368 on the box itself never touches Cloudflare. The JWT
 * is minted locally and lives 5 minutes, so nothing long-lived crosses the
 * wire; the admin key itself comes from ghost-key.mjs, never from this file.
 *
 * `--members` sets visibility so the page is gated to signed-up members —
 * that is what makes the free asset worth an email address.
 */
import fs from 'fs';
import { execFileSync } from 'child_process';
import { ghostToken } from './ghost-key.mjs';

const HOST = 'geniusjunkie';
// Ghost 301s any request whose Host is not the configured canonical URL, so
// hitting 127.0.0.1:2368 bounces straight back out through Cloudflare. Keep
// the real hostname and scheme and pin the DNS to the loopback instead —
// nginx terminates TLS on the box, so the certificate still matches.
const API = 'https://geniusjunkie.net/ghost/api/admin';
const RESOLVE = '--resolve geniusjunkie.net:443:127.0.0.1';

/** Run one curl on the server. Body (if any) goes over stdin, never argv. */
function call(method, path, body) {
  const args = [
    '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=20', HOST,
    `curl -s ${RESOLVE} -X ${method} "${API}${path}" ` +
    `-H "Authorization: Ghost ${ghostToken()}" -H "Content-Type: application/json" ` +
    `-H "Accept-Version: v5.0"` + (body ? ' --data-binary @-' : ''),
  ];
  const out = execFileSync('ssh', args, {
    input: body ? JSON.stringify(body) : undefined,
    encoding: 'utf8', maxBuffer: 20e6,
  });
  try { return JSON.parse(out); } catch { throw new Error(`non-JSON reply: ${out.slice(0, 300)}`); }
}

const [slug, title, file, ...flags] = process.argv.slice(2);
const html = fs.readFileSync(file, 'utf8');
const visibility = flags.includes('--members') ? 'members' : 'public';

let existing = null;
const found = call('GET', `/pages/slug/${slug}/?formats=html`);
if (found.pages?.length) existing = found.pages[0];

let res;
if (existing) {
  // PUT needs updated_at for collision detection AND the id in the path
  res = call('PUT', `/pages/${existing.id}/?source=html`, {
    pages: [{ html, title, visibility, updated_at: existing.updated_at }],
  });
} else {
  res = call('POST', '/pages/?source=html', {
    pages: [{ title, slug, html, visibility, status: 'published' }],
  });
}
if (res.errors) { console.error('  ✗', JSON.stringify(res.errors).slice(0, 400)); process.exit(1); }
const p = res.pages[0];
console.log(`  ✓ ${existing ? 'updated' : 'created'} ${p.url}  (visibility: ${p.visibility})`);
