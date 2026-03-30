import { VideoData } from '../types';

// ─── YouTube Studio CSV format parser ────────────────────────────────────────
// Handles the standard YouTube Analytics export format

const COLUMN_MAP: Record<string, keyof VideoData> = {
  'video title': 'title',
  'content': 'title',
  'video publish time': 'publishedAt',
  'views': 'views',
  'watch time (hours)': 'watchTimeHours',
  'watch time': 'watchTimeHours',
  'impressions': 'impressions',
  'impressions click-through rate (%)': 'ctr',
  'impressions ctr (%)': 'ctr',
  'average view duration': 'avgViewDurationSeconds',
  'average percentage viewed (%)': 'avgViewDurationSeconds', // treated as proxy
  'likes': 'likes',
  'comments': 'comments',
};

function parseNumber(val: string): number {
  if (!val || val === '--') return 0;
  return parseFloat(val.replace(/,/g, '')) || 0;
}

function parseDuration(val: string): number {
  // Handles "0:03:45" → 225 seconds, or "225" → 225
  if (!val || val === '--') return 0;
  if (val.includes(':')) {
    const parts = val.split(':').map(Number);
    if (parts.length === 3) return parts[0] * 3600 + parts[1] * 60 + parts[2];
    if (parts.length === 2) return parts[0] * 60 + parts[1];
  }
  return parseFloat(val) || 0;
}

export function parseYouTubeCSV(csvText: string): VideoData[] {
  const lines = csvText
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean);

  if (lines.length < 2) return [];

  // Find header row (skip any metadata rows YouTube prepends)
  let headerIdx = 0;
  for (let i = 0; i < Math.min(5, lines.length); i++) {
    const lower = lines[i].toLowerCase();
    if (lower.includes('video title') || lower.includes('content') || lower.includes('views')) {
      headerIdx = i;
      break;
    }
  }

  const headers = parseCSVRow(lines[headerIdx]).map((h) => h.toLowerCase().trim());
  const videos: VideoData[] = [];

  for (let i = headerIdx + 1; i < lines.length; i++) {
    const cols = parseCSVRow(lines[i]);
    if (cols.length < 2 || !cols[0]) continue;

    const row: Partial<VideoData> & { title?: string } = {
      id: `video-${i}-${Date.now()}`,
    };

    headers.forEach((header, idx) => {
      const field = COLUMN_MAP[header];
      if (!field || idx >= cols.length) return;
      const val = cols[idx]?.trim() ?? '';

      if (field === 'title' || field === 'publishedAt') {
        (row as Record<string, string | number>)[field] = val;
      } else if (field === 'avgViewDurationSeconds') {
        row.avgViewDurationSeconds = parseDuration(val);
      } else {
        (row as Record<string, number>)[field] = parseNumber(val);
      }
    });

    if (row.title) {
      videos.push({
        id: row.id ?? `v-${i}`,
        title: row.title,
        publishedAt: row.publishedAt ?? '',
        views: row.views ?? 0,
        ctr: row.ctr ?? 0,
        avgViewDurationSeconds: row.avgViewDurationSeconds ?? 0,
        watchTimeHours: row.watchTimeHours ?? 0,
        likes: row.likes ?? 0,
        comments: row.comments ?? 0,
        impressions: row.impressions ?? 0,
      });
    }
  }

  return videos;
}

// Simple CSV row parser that handles quoted fields
function parseCSVRow(line: string): string[] {
  const result: string[] = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      inQuotes = !inQuotes;
    } else if (ch === ',' && !inQuotes) {
      result.push(current);
      current = '';
    } else {
      current += ch;
    }
  }
  result.push(current);
  return result;
}

// ─── Analytics aggregation helpers ───────────────────────────────────────────

export function summarizeAnalytics(videos: VideoData[]) {
  if (!videos.length) return null;

  const totalViews = videos.reduce((s, v) => s + v.views, 0);
  const totalWatchHours = videos.reduce((s, v) => s + v.watchTimeHours, 0);
  const totalImpressions = videos.reduce((s, v) => s + v.impressions, 0);
  const avgCTR =
    videos.filter((v) => v.ctr > 0).reduce((s, v) => s + v.ctr, 0) /
    (videos.filter((v) => v.ctr > 0).length || 1);
  const avgRetention =
    videos
      .filter((v) => v.avgViewDurationSeconds > 0)
      .reduce((s, v) => s + v.avgViewDurationSeconds, 0) /
    (videos.filter((v) => v.avgViewDurationSeconds > 0).length || 1);

  const topByViews = [...videos].sort((a, b) => b.views - a.views).slice(0, 5);
  const topByCTR = [...videos]
    .filter((v) => v.ctr > 0)
    .sort((a, b) => b.ctr - a.ctr)
    .slice(0, 5);

  return {
    totalViews,
    totalWatchHours: Math.round(totalWatchHours),
    totalImpressions,
    avgCTR: Math.round(avgCTR * 10) / 10,
    avgRetentionSeconds: Math.round(avgRetention),
    videoCount: videos.length,
    topByViews,
    topByCTR,
  };
}

export function formatAnalyticsForClaude(videos: VideoData[]): string {
  if (!videos.length) return 'No video data available.';

  const summary = summarizeAnalytics(videos)!;
  const topVideos = summary.topByViews.slice(0, 10);

  return `
Total videos: ${summary.videoCount}
Total views: ${summary.totalViews.toLocaleString()}
Total watch hours: ${summary.totalWatchHours.toLocaleString()}
Avg CTR: ${summary.avgCTR}%
Avg view duration: ${Math.floor(summary.avgRetentionSeconds / 60)}m ${summary.avgRetentionSeconds % 60}s

Top 10 videos by views:
${topVideos
  .map(
    (v, i) =>
      `${i + 1}. "${v.title}" — ${v.views.toLocaleString()} views, ${v.ctr}% CTR, ${Math.floor(v.avgViewDurationSeconds / 60)}m retention`
  )
  .join('\n')}
`.trim();
}
