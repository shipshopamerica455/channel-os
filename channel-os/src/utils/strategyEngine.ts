import { VideoIdea, Channel, StrategyFit } from '../types';

// ─── Strategy fit checker ─────────────────────────────────────────────────────

export function checkStrategyFit(
  title: string,
  channel: Channel
): { fit: StrategyFit; reason: string } {
  const lower = title.toLowerCase();
  const { keyPhrases, avoidTopics, contentPillars } = channel.strategy;

  // Check avoid list first
  const avoid = avoidTopics.find((t) =>
    lower.includes(t.toLowerCase().split(' ')[0])
  );
  if (avoid) {
    return {
      fit: 'off-brand',
      reason: `Topic overlaps with avoid list: "${avoid}"`,
    };
  }

  // Check keyword match strength
  const matchedPhrases = keyPhrases.filter((kw) => lower.includes(kw.toLowerCase()));
  const matchedPillars = contentPillars.filter((p) =>
    p
      .toLowerCase()
      .split(' ')
      .some((word) => word.length > 4 && lower.includes(word))
  );

  if (matchedPhrases.length >= 3 || matchedPillars.length >= 2) {
    return {
      fit: 'strong',
      reason: `Directly aligns with ${matchedPillars[0] ?? matchedPhrases[0]}`,
    };
  }

  if (matchedPhrases.length >= 1 || matchedPillars.length >= 1) {
    return {
      fit: 'moderate',
      reason: `Loosely connected to ${matchedPillars[0] ?? matchedPhrases[0]}`,
    };
  }

  return {
    fit: 'weak',
    reason: 'No strong connection to channel pillars or keywords detected',
  };
}

// ─── Promotion checklist generator ───────────────────────────────────────────

import { PromotionTask, ChannelId } from '../types';
import { PROMOTION_TEMPLATES } from '../data/channels';

export function buildPromotionChecklist(channelId: ChannelId): PromotionTask[] {
  const tasks = PROMOTION_TEMPLATES[channelId] ?? [];
  return tasks.map((task, i) => ({
    id: `promo-${i}-${Date.now()}`,
    task,
    platform: inferPlatform(task),
    dueAfterPublish: inferDue(task),
    done: false,
  }));
}

function inferPlatform(task: string): string {
  const lower = task.toLowerCase();
  if (lower.includes('pinterest')) return 'Pinterest';
  if (lower.includes('blog')) return 'Blog';
  if (lower.includes('email')) return 'Email';
  if (lower.includes('instagram')) return 'Instagram';
  if (lower.includes('tiktok')) return 'TikTok';
  if (lower.includes('twitter') || lower.includes('x thread')) return 'X/Twitter';
  if (lower.includes('linkedin')) return 'LinkedIn';
  if (lower.includes('reddit')) return 'Reddit';
  if (lower.includes('community')) return 'YouTube Community';
  if (lower.includes('short')) return 'YouTube Shorts';
  if (lower.includes('newsletter')) return 'Newsletter';
  return 'YouTube';
}

function inferDue(task: string): string {
  const lower = task.toLowerCase();
  if (lower.includes('short') || lower.includes('pin') || lower.includes('community')) {
    return 'Same day';
  }
  if (lower.includes('blog') || lower.includes('email') || lower.includes('newsletter')) {
    return 'Day 3';
  }
  return 'Week 1';
}

// ─── Content cluster builder ──────────────────────────────────────────────────

export interface ContentCluster {
  name: string;
  pillar: string;
  ideas: VideoIdea[];
}

export function groupIdeasIntoClusters(ideas: VideoIdea[]): ContentCluster[] {
  const map = new Map<string, VideoIdea[]>();
  for (const idea of ideas) {
    const key = idea.cluster || 'Unclustered';
    if (!map.has(key)) map.set(key, []);
    map.get(key)!.push(idea);
  }

  return Array.from(map.entries()).map(([name, clusterIdeas]) => ({
    name,
    pillar: clusterIdeas[0]?.format ?? 'General',
    ideas: clusterIdeas,
  }));
}

// ─── Weekly health score ──────────────────────────────────────────────────────

export function scoreChannelHealth(
  avgCTR: number,
  avgRetentionPct: number,
  videosThisMonth: number
): { score: number; label: string; color: string } {
  let score = 0;
  if (avgCTR >= 6) score += 35;
  else if (avgCTR >= 4) score += 25;
  else if (avgCTR >= 2) score += 15;
  else score += 5;

  if (avgRetentionPct >= 50) score += 35;
  else if (avgRetentionPct >= 35) score += 25;
  else if (avgRetentionPct >= 20) score += 15;
  else score += 5;

  if (videosThisMonth >= 4) score += 30;
  else if (videosThisMonth >= 2) score += 20;
  else if (videosThisMonth >= 1) score += 10;

  if (score >= 80) return { score, label: 'Thriving', color: '#10B981' };
  if (score >= 60) return { score, label: 'Healthy', color: '#3B82F6' };
  if (score >= 40) return { score, label: 'Growing', color: '#F59E0B' };
  return { score, label: 'Needs Attention', color: '#EF4444' };
}

// ─── Idea deduplication helper ────────────────────────────────────────────────

export function deduplicateIdeas(
  existing: VideoIdea[],
  incoming: VideoIdea[]
): VideoIdea[] {
  const existingTitles = new Set(
    existing.map((i) => i.title.toLowerCase().trim())
  );
  return incoming.filter(
    (idea) => !existingTitles.has(idea.title.toLowerCase().trim())
  );
}
