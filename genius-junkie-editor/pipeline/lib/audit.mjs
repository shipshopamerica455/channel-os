/**
 * audit.mjs — diff what EXISTS against what is LINKED, and check the paths a
 * customer actually walks.
 *
 * Every problem this catches was found the hard way on 12 Sep 2026: products
 * live but missing from /templates/, checklists live but missing from
 * /free-canva-resources/, a welcome email switched off, 27 viewer comments with
 * no reply, and Cloudflare challenging Ghost's own Content API so no one could
 * sign up at all. None of it errored. It was all silent.
 *
 *   node pipeline/gj.mjs audit          full report
 *   node pipeline/gj.mjs audit --quiet  only failures
 *
 * Exits non-zero if anything fails, so it can gate a publish.
 *
 * Most fetches go to the ORIGIN over ssh, bypassing the CDN. The portal check
 * deliberately goes through the public edge — that is the only way to catch a
 * Cloudflare rule eating the API.
 */
import { execFileSync } from 'child_process';
import { c } from './util.mjs';

const HOST = 'geniusjunkie';
const SITE = 'https://geniusjunkie.net';
const ORIGIN = `--resolve geniusjunkie.net:443:127.0.0.1`;
/** a couple of unanswered comments is normal; a growing pile is the problem */
const COMMENT_BACKLOG = 5;

const sh = (script) => {
  try { return execFileSync('ssh', [HOST, script], { encoding: 'utf8', maxBuffer: 1 << 24 }); }
  catch (e) { return e.stdout || ''; }
};
/** fetch a URL from the server, bypassing the CDN */
const origin = (path) => sh(`curl -sk ${ORIGIN} '${SITE}${path}'`);
/** fetch through the public edge — catches CDN rules blocking our own APIs */
const edge = (path) => sh(`curl -s -o /tmp/_a -w '%{http_code}' '${SITE}${path}'; echo; cat /tmp/_a`);

const uniq = (a) => [...new Set(a)].sort();
const matches = (s, re) => uniq([...s.matchAll(re)].map((m) => m[1]));

const results = [];
/** worth seeing, but does not block a publish — a quiet backlog, not a broken page */
const warn = (name, detail) => {
  console.log(`${c.yellow('  WARN')}  ${name}`);
  if (detail) detail.split('\n').forEach((l) => console.log(`          ${c.dim(l)}`));
};
const check = (name, ok, detail) => {
  results.push({ name, ok, detail });
  const tag = ok ? c.green('  PASS') : c.red('  FAIL');
  if (!ok || !process.argv.includes('--quiet')) console.log(`${tag}  ${name}`);
  if (!ok && detail) detail.split('\n').forEach((l) => console.log(`          ${c.yellow(l)}`));
};

export async function audit() {
  console.log(`\n${c.bold ? c.bold('Genius Junkie — site audit') : 'Genius Junkie — site audit'}\n`);

  // 1. can Portal reach its own API through the CDN? (the silent killer)
  const home = origin('/');
  const key = (home.match(/data-key="([a-f0-9]+)"/) || [])[1];
  if (!key) check('portal · content api key found in page', false, 'no data-key on the homepage — Portal script missing?');
  else {
    const res = edge(`/ghost/api/content/settings/?key=${key}`);
    const [code, ...rest] = res.split('\n');
    const body = rest.join('\n');
    check('portal · Content API reachable through the CDN', code.trim() === '200' && body.trim().startsWith('{'),
      `got HTTP ${code.trim()} and ${body.trim().startsWith('<') ? 'an HTML challenge page' : 'a non-JSON body'}\n` +
      `a CDN rule is blocking /ghost/api/content/ — every signup silently fails`);
  }
  const site = edge('/members/api/site/');
  check('portal · members API reachable', site.split('\n')[0].trim() === '200', `HTTP ${site.split('\n')[0].trim()}`);

  // 2. every product page that exists is listed in the shop
  const sitemap = origin('/sitemap-pages.xml');
  const allPages = matches(sitemap, /geniusjunkie\.net\/([a-z0-9-]+)\//g);
  const products = allPages.filter((p) => /(kit|pack)$/.test(p) && !p.endsWith('-thank-you'));
  const shop = origin('/templates/');
  const listed = products.filter((p) => shop.includes(`/${p}/`));
  const unlisted = products.filter((p) => !shop.includes(`/${p}/`));
  check(`shop · all ${products.length} products listed on /templates/`, unlisted.length === 0,
    `missing: ${unlisted.join(', ')}`);

  // 3. every product delivers: thank-you page live, with a template link or files
  //    one remote pass — a per-file ssh round trip made this take minutes
  const script = `for p in ${products.join(' ')}; do
  code=$(curl -sk -o /tmp/_t -w '%{http_code}' ${ORIGIN} '${SITE}/'"$p"'-thank-you/')
  if [ "$code" != "200" ]; then echo "$p|HTTP $code|"; continue; fi
  if grep -q 'CANVA_LINK\\|STRIPE_LINK' /tmp/_t; then echo "$p|placeholder|"; continue; fi
  canva=$(grep -c 'canva\\.link/' /tmp/_t)
  nfiles=0
  bad=""
  for f in $(grep -oE '/content/files/[^"'"'"']+\\.(pdf|zip)' /tmp/_t | sort -u); do
    fc=$(curl -sk -o /dev/null -w '%{http_code}' ${ORIGIN} '${SITE}'"$f")
    [ "$fc" != "200" ] && bad="$bad $f=$fc"
    nfiles=$((nfiles+1))
  done
  echo "$p|$canva:$nfiles|$bad"
done`;
  const broken = [];
  for (const line of sh(script).trim().split('\n').filter(Boolean)) {
    const [slug, status, bad] = line.split('|');
    if (status.startsWith('HTTP')) broken.push(`${slug}: thank-you page ${status}`);
    else if (status === 'placeholder') broken.push(`${slug}: unresolved placeholder on the delivery page`);
    else {
      const [canva, nfiles] = status.split(':').map(Number);
      if (!canva && !nfiles) broken.push(`${slug}: no Canva link and no files — buyer gets nothing`);
    }
    if (bad && bad.trim()) broken.push(`${slug}: dead file ->${bad}`);
  }
  check(`delivery · all ${products.length} thank-you pages hand over the goods`, broken.length === 0, broken.join('\n'));

  // 4. every free checklist is listed on the public page that exists to list them
  // Every `get-` page is a lead magnet, whatever it is called. The old pattern
  // demanded `-checklist` too, so the twelve "…-card" one-pagers built from
  // Oct 2026 onwards were invisible to this check AND to readers — it reported
  // "all 12 listed" while twelve more sat unlinked. Match the prefix only.
  const checklists = allPages.filter((p) => p.startsWith('get-'));
  const freePage = origin('/free-canva-resources/');
  const missingCk = checklists.filter((p) => !freePage.includes(p));
  check(`checklists · all ${checklists.length} listed on /free-canva-resources/`, missingCk.length === 0,
    `missing: ${missingCk.join(', ')}`);

  // 5. every nav item goes somewhere real
  const nav = matches(home.match(/<nav[\s\S]*?<\/nav>/)?.[0] || home,
    /href="(https:\/\/geniusjunkie\.net\/[^"]*)"/g);
  const deadNav = [];
  for (const u of nav) {
    const p = u.replace(SITE, '') || '/';
    const code = sh(`curl -sk -o /dev/null -w '%{http_code}' ${ORIGIN} '${SITE}${p}'`).trim();
    if (code !== '200') deadNav.push(`${p} → HTTP ${code}`);
  }
  check(`nav · all ${nav.length} destinations return 200`, deadNav.length === 0, deadNav.join('\n'));

  // 6. every buy button on the shop actually opens a checkout
  const links = matches(shop, /(https:\/\/buy\.stripe\.com\/[A-Za-z0-9]+)/g);
  const deadPay = [];
  for (const u of links) {
    const code = sh(`curl -s -o /dev/null -w '%{http_code}' '${u}'`).trim();
    if (code !== '200') deadPay.push(`${u} → HTTP ${code}`);
  }
  check(`checkout · all ${links.length} Stripe links live`, deadPay.length === 0, deadPay.join('\n'));

  // 7. every social icon in the footer points at an account that still exists
  //    The Pinterest link was dead for months: pinterest.com/GeniusJunkieYT had
  //    no account behind it and still answered 200, so nothing noticed.
  //    Deliberately narrow — a 404 or a named not-found page fails, anything
  //    else (bot walls, 429s, redirects) is reported but never fails the build.
  //    TikTok ships the string "Couldn't find this account" in its JS on EVERY
  //    profile, live ones included. Do not add phrase matching without a
  //    control test against an account you know is live.
  const socials = matches(home.match(/class="footer-social"[\s\S]*?<\/div>/)?.[0] || '',
    /href="(https?:\/\/[^"]+)"/g);
  const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0 Safari/537.36';
  const socialScript = socials.map((u) => `c=$(curl -sL -m 25 -A '${UA}' -o /tmp/_s -w '%{http_code}' '${u}')
n=$(tr -d '\\000' < /tmp/_s | grep -ci 'User not found')
echo '${u}|'"$c|$n"`).join('\n');
  const deadSocial = [], oddSocial = [];
  for (const line of sh(socialScript).trim().split('\n').filter(Boolean)) {
    const [u, code, notfound] = line.split('|');
    if (code === '404' || code === '410') deadSocial.push(`${u} → HTTP ${code}`);
    else if (Number(notfound)) deadSocial.push(`${u} → the platform says that account does not exist`);
    else if (code !== '200') oddSocial.push(`${u} → HTTP ${code}`);
  }
  check(`socials · all ${socials.length} footer accounts exist`, deadSocial.length === 0, deadSocial.join('\n'));
  if (oddSocial.length) warn('socials · some could not be confirmed', `${oddSocial.join('\n')}\nusually a bot wall, not a dead link — open one to be sure`);

  // 8. nothing falls back to Ghost's stock photo when it is shared or pinned
  //    78 pages had no share image, so every pin of a product page showed a
  //    generic Ghost cover. Pinterest is image-first; that is a dead pin.
  const ogScript = `for u in $(curl -sk ${ORIGIN} '${SITE}/sitemap-pages.xml' | grep -oE 'https://geniusjunkie.net/[^<]*'); do
  img=$(curl -sk ${ORIGIN} "$u" | tr -d '\\000' | grep -oE '<meta property="og:image" content="[^"]*"' | head -1)
  case "$img" in *static.ghost.org*) echo "STOCK|$u";; '') echo "MISSING|$u";; esac
done`;
  const noShare = sh(ogScript).trim().split('\n').filter(Boolean)
    .map((l) => l.split('|')[1] + (l.startsWith('STOCK') ? ' → Ghost stock photo' : ' → no og:image'));
  check('share · every page has its own share image', noShare.length === 0, noShare.join('\n'));

  // 9. the comment backlog — the one check that isn't about the site
  //    It reached 27 unanswered before anyone noticed. Replies are the cheapest
  //    reach this channel has, so a backlog is a revenue leak, not housekeeping.
  //    Runs out of process: the token and googleapis live with the YouTube
  //    scripts, and an expired token must never fail the site audit.
  const YT = '/Users/admin/Documents/Kimi Extension v1/remotion-shorts';
  let comments = null;
  try {
    comments = JSON.parse(execFileSync('node', ['gj-unanswered.mjs'],
      { cwd: YT, encoding: 'utf8', timeout: 60000, stdio: ['ignore', 'pipe', 'pipe'] }));
  } catch (e) {
    const lines = `${e.stderr || ''}\n${e.message}`.split('\n').map((l) => l.trim()).filter(Boolean);
    warn('comments · backlog not checked',
      `${lines.find((l) => /error|invalid|expired|denied/i.test(l)) || lines[0]}\nre-auth: node ${YT}/reauth-geniusjunkie.mjs`);
  }
  if (comments) {
    const { waiting, days, oldest, who } = comments;
    check(`comments · ${waiting} viewer comment${waiting === 1 ? '' : 's'} waiting on a reply`, waiting <= COMMENT_BACKLOG,
      `${waiting} unanswered for more than ${days} days, oldest ${oldest}\n` +
      `${who.join(', ')}${waiting > who.length ? ` and ${waiting - who.length} more` : ''}\n` +
      `list them: node ${YT}/gj-unanswered.mjs  ·  post approved replies: node ${YT}/gj-post-replies.mjs`);
  }

  const failed = results.filter((r) => !r.ok);
  console.log(`\n  ${failed.length ? c.red(`${failed.length} of ${results.length} checks failed`)
    : c.green(`all ${results.length} checks passed`)}\n`);
  if (failed.length) process.exitCode = 1;
}
