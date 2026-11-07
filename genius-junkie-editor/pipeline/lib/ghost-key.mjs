// The Ghost Admin API key for geniusjunkie.net, in one place.
//
// It used to be hardcoded in ghost.mjs, ghost-ssh.mjs and ghost-hub.mjs: three
// copies of a credential with full write access to the live site, in a folder
// sitting beside a PUBLIC git remote. One `git add -A` would have published it.
//
// There is now exactly ONE copy on disk — GHOST_ADMIN_KEY in
// remotion-shorts/.env, gitignored inside a PRIVATE repo, which is already the
// copy gj-health-check.mjs reads. A second copy here would mean rotating the
// key in two places and finding out later that one of them was missed.
//
// Lazy on purpose, like kitBase(): a missing key must break the Ghost commands
// only, not every pipeline command at import time. It never falls back to a
// literal, because a wrong-but-present key fails as a 401 halfway through a
// publish, which is worse than refusing to start.
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ENV_FILE = path.resolve(__dirname, '../../../remotion-shorts/.env');
const VAR = 'GHOST_ADMIN_KEY';
const SHAPE = /^[0-9a-f]{24}:[0-9a-f]{64}$/;   // <key id>:<hex secret>

const recover = `Set ${VAR}=<id>:<secret> in ${ENV_FILE}, or export it. ` +
  `The key is in Ghost admin under Settings > Integrations > the pipeline integration.`;

let _key;
function key() {
  if (_key) return _key;
  let raw = (process.env[VAR] || '').trim();
  if (!raw && fs.existsSync(ENV_FILE)) {
    raw = (fs.readFileSync(ENV_FILE, 'utf8').split('\n')
      .find((l) => l.startsWith(`${VAR}=`)) || '').slice(VAR.length + 1).trim();
  }
  raw = raw.replace(/^['"]|['"]$/g, '');
  if (!raw) throw new Error(`no Ghost admin key: ${VAR} is unset and ${ENV_FILE} does not define it. ${recover}`);
  if (!SHAPE.test(raw)) throw new Error(`${VAR} is not <24-hex id>:<64-hex secret> (got ${raw.length} chars). ${recover}`);
  const [id, secret] = raw.split(':');
  _key = { id, secret };
  return _key;
}

const b64 = (b) => Buffer.from(b).toString('base64url');

/** A 5-minute Ghost Admin API JWT. Mint one per request; they are free. */
export function ghostToken() {
  const { id, secret } = key();
  const iat = Math.floor(Date.now() / 1000);
  const h = b64(JSON.stringify({ alg: 'HS256', typ: 'JWT', kid: id }));
  const p = b64(JSON.stringify({ iat, exp: iat + 300, aud: '/admin/' }));
  const sig = crypto.createHmac('sha256', Buffer.from(secret, 'hex')).update(`${h}.${p}`).digest('base64url');
  return `${h}.${p}.${sig}`;
}

/** The key id — safe to print. Use it to confirm which integration is loaded. */
export const keyId = () => key().id;

// node ghost-key.mjs --check  -> proves the key loads and mints, printing no secret.
// Decoded-path compare: this repo lives under a directory with a space in it.
if (fileURLToPath(import.meta.url) === path.resolve(process.argv[1] || '')) {
  const t = ghostToken();
  console.log(`✓ key ${keyId()} loaded from ${process.env[VAR] ? `$${VAR}` : ENV_FILE}`);
  console.log(`✓ minted a JWT (${t.split('.').length} parts, ${t.length} chars)`);
}
