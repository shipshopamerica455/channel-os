#!/usr/bin/env node
/**
 * YouTube → Ghost Sync
 * Fetches new videos from the Genius Junkie YouTube channel and publishes them
 * as articles on geniusjunkie.net. Tracks synced videos by tag to avoid duplicates.
 */

import { createHmac } from 'crypto';

const GHOST_URL = 'https://geniusjunkie.net';
const GHOST_ADMIN_KEY = process.env.GHOST_ADMIN_KEY || '69b80d0d45599ceecb2216b1:fafd355a96af386a58f89b6d3a5acf60cc0e60c9cebd69c998b1d8c483992de3';
const YOUTUBE_CHANNEL_ID = 'UCz8eVGSEicfswKIe4XAp7Kw';
const SYNC_TAG = 'youtube-synced';

function makeJwt(adminKey) {
  const [id, secret] = adminKey.split(':');
  const now = Math.floor(Date.now() / 1000);
  const header = Buffer.from(JSON.stringify({ alg: 'HS256', kid: id, typ: 'JWT' })).toString('base64url');
  const payload = Buffer.from(JSON.stringify({ iat: now, exp: now + 300, aud: '/admin/' })).toString('base64url');
  const sig = createHmac('sha256', Buffer.from(secret, 'hex'))
    .update(`${header}.${payload}`)
    .digest('base64url');
  return `${header}.${payload}.${sig}`;
}

async function ghostRequest(method, path, body) {
  const token = makeJwt(GHOST_ADMIN_KEY);
  const res = await fetch(`${GHOST_URL}/ghost/api/admin${path}`, {
    method,
    headers: {
      'Authorization': `Ghost ${token}`,
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok && res.status !== 204) {
    const text = await res.text();
    throw new Error(`Ghost API ${method} ${path} → ${res.status}: ${text}`);
  }
  return res.status === 204 ? null : res.json();
}

async function fetchYouTubeVideos() {
  const url = `https://www.youtube.com/feeds/videos.xml?channel_id=${YOUTUBE_CHANNEL_ID}`;
  const res = await fetch(url);
  const xml = await res.text();

  const videos = [];
  const entries = xml.split('<entry>').slice(1);

  for (const entry of entries) {
    const videoId = entry.match(/<yt:videoId>([^<]+)<\/yt:videoId>/)?.[1];
    const title = entry.match(/<title>([^<]+)<\/title>/)?.[1]?.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
    const published = entry.match(/<published>([^<]+)<\/published>/)?.[1];
    const description = entry.match(/<media:description>([^<]*)<\/media:description>/s)?.[1]
      ?.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').trim();
    const thumbnail = entry.match(/url="(https:\/\/i[^"]*hqdefault[^"]*)"/)?.[1];

    if (videoId && title) {
      videos.push({ videoId, title, published, description, thumbnail });
    }
  }
  return videos;
}

async function getSyncedVideoIds() {
  const data = await ghostRequest('GET', `/posts/?limit=all&filter=tag:${SYNC_TAG}&include=tags`);
  const ids = new Set();
  for (const post of data.posts || []) {
    for (const tag of post.tags || []) {
      if (tag.slug?.startsWith('yt-')) {
        ids.add(tag.slug.replace('yt-', ''));
      }
    }
  }
  return ids;
}

function buildPostContent(video) {
  const lines = (video.description || '').split('\n').filter(l => l.trim());
  // Take first paragraph as excerpt (stop at blank line or timestamps)
  const excerptLines = [];
  for (const line of lines) {
    if (/^\[?\d+:\d+\]/.test(line) || line.startsWith('==') || line.startsWith('http')) break;
    excerptLines.push(line);
    if (excerptLines.length >= 3) break;
  }
  const excerpt = excerptLines.join(' ').substring(0, 300);

  // Build Mobiledoc with YouTube embed + description
  const cards = [
    ['embed', { url: `https://www.youtube.com/watch?v=${video.videoId}`, type: 'video' }]
  ];

  const sections = [[10, 0]]; // card index 0

  if (video.description) {
    // Add description as HTML paragraphs
    const descParagraphs = lines
      .filter(l => l.trim() && !l.startsWith('=='))
      .slice(0, 20)
      .map(l => `<p>${l.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</p>`)
      .join('');
    cards.push(['html', { html: descParagraphs }]);
    sections.push([10, 1]);
  }

  const mobiledoc = JSON.stringify({
    version: '0.3.1',
    markups: [],
    atoms: [],
    cards,
    sections,
  });

  return { mobiledoc, excerpt };
}

async function createPost(video) {
  const { mobiledoc, excerpt } = buildPostContent(video);

  await ghostRequest('POST', '/posts/', {
    posts: [{
      title: video.title,
      mobiledoc,
      custom_excerpt: excerpt || null,
      status: 'published',
      published_at: video.published || new Date().toISOString(),
      feature_image: video.thumbnail || null,
      tags: [
        { name: 'YouTube', slug: 'youtube' },
        { name: SYNC_TAG, slug: SYNC_TAG },
        { name: `yt-${video.videoId}`, slug: `yt-${video.videoId}` },
      ],
    }],
  });
}

async function main() {
  console.log('🔄 Fetching YouTube videos...');
  const videos = await fetchYouTubeVideos();
  console.log(`   Found ${videos.length} videos on channel`);

  console.log('📋 Checking already-synced videos...');
  const syncedIds = await getSyncedVideoIds();
  console.log(`   Already synced: ${syncedIds.size}`);

  const newVideos = videos.filter(v => !syncedIds.has(v.videoId));
  console.log(`   New to sync: ${newVideos.length}`);

  if (newVideos.length === 0) {
    console.log('✅ Nothing new to sync.');
    return;
  }

  for (const video of newVideos) {
    try {
      console.log(`   Publishing: "${video.title}"`);
      await createPost(video);
      console.log(`   ✓ Done`);
    } catch (err) {
      console.error(`   ✗ Failed: ${err.message}`);
    }
  }

  console.log(`\n✅ Sync complete. Published ${newVideos.length} new post(s).`);
}

main().catch(err => {
  console.error('Fatal:', err.message);
  process.exit(1);
});
