// Direct browser calls to Anthropic API (local tool — BYOK)

const API_URL = 'https://api.anthropic.com/v1/messages';
const MODEL = 'claude-opus-4-6';

export interface ClaudeMessage {
  role: 'user' | 'assistant';
  content: string;
}

export async function callClaude(
  apiKey: string,
  systemPrompt: string,
  userMessage: string,
  maxTokens = 2000
): Promise<string> {
  if (!apiKey) throw new Error('No API key set. Add your Anthropic API key in Settings.');

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-allow-browser': 'true',
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: maxTokens,
      system: systemPrompt,
      messages: [{ role: 'user', content: userMessage }],
    }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(
      (err as { error?: { message?: string } }).error?.message ??
        `API error ${response.status}`
    );
  }

  const data = await response.json() as {
    content: Array<{ type: string; text: string }>;
  };
  return data.content[0]?.text ?? '';
}

// ─── Idea generation ──────────────────────────────────────────────────────────

export async function generateVideoIdeas(
  apiKey: string,
  channelName: string,
  strategy: {
    contentPillars: string[];
    contentFormats: string[];
    targetAudience: string;
    toneAndStyle: string;
    shortsCriteria: string[];
    repurposingRules: string[];
    avoidTopics: string[];
  },
  analyticsContext: string,
  notesContext: string,
  count: number = 8
): Promise<string> {
  const system = `You are a YouTube channel strategist. You generate highly specific, search-optimized video ideas tailored to a channel's exact identity and audience. Always output valid JSON only — no markdown, no explanation.`;

  const user = `Generate exactly ${count} YouTube video ideas for the channel "${channelName}".

CHANNEL STRATEGY:
- Content pillars: ${strategy.contentPillars.join(', ')}
- Formats: ${strategy.contentFormats.join(', ')}
- Target audience: ${strategy.targetAudience}
- Tone/style: ${strategy.toneAndStyle}
- AVOID these topics: ${strategy.avoidTopics.join(', ')}
- Shorts criteria: ${strategy.shortsCriteria.join(', ')}
- Repurposing rules: ${strategy.repurposingRules.join(', ')}

ANALYTICS CONTEXT (top-performing patterns):
${analyticsContext || 'No analytics data uploaded yet — generate based on channel strategy.'}

CHANNEL NOTES (wins/failures/observations):
${notesContext || 'No notes yet.'}

Return a JSON array of exactly ${count} objects. Each object must have these fields:
{
  "title": "Specific, compelling YouTube title",
  "hook": "Opening line or visual hook for the video",
  "angle": "The unique angle or framing that makes this stand out",
  "format": "One of the channel's content formats",
  "cluster": "Content cluster or series this belongs to",
  "thumbnailConcept": "Brief thumbnail visual concept",
  "shortsAngle": "How to cut a 60-second Short from this (or null if not applicable)",
  "repurposingIdeas": ["array", "of", "repurposing", "ideas"],
  "strategyFit": "strong | moderate | weak | off-brand",
  "fitReason": "One sentence explaining why this fits (or doesn't fit) the channel strategy",
  "priority": "high | medium | low"
}`;

  return callClaude(apiKey, system, user, 3000);
}

// ─── Channel health summary ───────────────────────────────────────────────────

export async function generateHealthSummary(
  apiKey: string,
  channelName: string,
  analyticsData: string,
  notes: string
): Promise<string> {
  const system = `You are a YouTube analytics expert. Analyze channel data and generate actionable intelligence. Output valid JSON only.`;

  const user = `Analyze this YouTube channel data for "${channelName}" and generate a health summary.

ANALYTICS DATA:
${analyticsData}

CHANNEL NOTES:
${notes || 'None'}

Return a JSON object with:
{
  "period": "Time period covered",
  "totalViews": number,
  "avgCTR": number,
  "avgRetentionPct": number,
  "totalWatchHours": number,
  "topTopics": ["array of top 5 topics by performance"],
  "winningFormats": ["array of top 3 formats"],
  "winningHooks": ["array of top 3 hook patterns observed"],
  "recommendations": ["array of 5 specific, actionable growth recommendations"],
  "warnings": ["array of 1-3 things to watch out for or fix"]
}`;

  return callClaude(apiKey, system, user, 2000);
}

// ─── Content cluster generation ───────────────────────────────────────────────

export async function generateContentClusters(
  apiKey: string,
  channelName: string,
  strategy: { contentPillars: string[]; targetAudience: string },
  topIdeas: string[]
): Promise<string> {
  const system = `You are a YouTube content strategist specializing in content clusters and series planning. Output valid JSON only.`;

  const user = `Create content clusters and series ideas for "${channelName}".

Content pillars: ${strategy.contentPillars.join(', ')}
Target audience: ${strategy.targetAudience}
Current idea backlog: ${topIdeas.slice(0, 10).join(' | ')}

Return a JSON array of content clusters:
[{
  "clusterName": "Descriptive cluster name",
  "pillar": "Which content pillar this belongs to",
  "description": "What this cluster covers",
  "videoIdeas": ["3-5 specific video titles for this cluster"],
  "seriesPotential": true/false,
  "seriesName": "Series name if applicable, else null"
}]

Generate 4-6 clusters.`;

  return callClaude(apiKey, system, user, 2000);
}

// ─── Marketing plan generation ────────────────────────────────────────────────

export async function generateMarketingPlan(
  apiKey: string,
  channelName: string,
  channelId: string,
  upcomingVideos: string[],
  repurposingRules: string[]
): Promise<string> {
  const system = `You are a YouTube channel marketing strategist. Create practical, platform-specific promotion plans. Output valid JSON only.`;

  const user = `Create a simple monthly marketing plan for "${channelName}" (${channelId}).

Upcoming videos: ${upcomingVideos.join(' | ')}
Repurposing rules: ${repurposingRules.join(' | ')}

Return a JSON object:
{
  "monthlyTheme": "One overarching theme for the month",
  "weeklyFocus": [
    { "week": 1, "focus": "...", "keyAction": "..." },
    { "week": 2, "focus": "...", "keyAction": "..." },
    { "week": 3, "focus": "...", "keyAction": "..." },
    { "week": 4, "focus": "...", "keyAction": "..." }
  ],
  "channelGrowthActions": ["5 specific channel growth actions for this month"],
  "promotionChecklist": [
    { "task": "...", "platform": "...", "dueAfterPublish": "Same day | Day 3 | Week 1" }
  ],
  "repurposingPlan": [
    { "format": "...", "platform": "...", "description": "...", "timing": "..." }
  ]
}`;

  return callClaude(apiKey, system, user, 2000);
}
