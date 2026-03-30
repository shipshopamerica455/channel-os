// ─── Channel Identities ──────────────────────────────────────────────────────

export type ChannelId = 'genius-junkie' | 'shipshop-tv' | 'ultra-health';

export interface ChannelStrategy {
  contentPillars: string[];
  contentFormats: string[];
  targetAudience: string;
  toneAndStyle: string;
  shortsCriteria: string[];
  repurposingRules: string[];
  avoidTopics: string[];
  keyPhrases: string[];
}

export interface Channel {
  id: ChannelId;
  name: string;
  tagline: string;
  color: string;
  accentDark: string;
  strategy: ChannelStrategy;
}

// ─── Analytics & Video Data ──────────────────────────────────────────────────

export interface VideoData {
  id: string;
  title: string;
  publishedAt: string; // ISO date string
  views: number;
  ctr: number; // percentage e.g. 4.5
  avgViewDurationSeconds: number;
  watchTimeHours: number;
  likes: number;
  comments: number;
  impressions: number;
  description?: string;
  tags?: string[];
}

export interface AnalyticsUpload {
  channelId: ChannelId;
  videos: VideoData[];
  uploadedAt: string;
  source: 'csv' | 'manual' | 'api';
}

export interface ChannelHealthSummary {
  channelId: ChannelId;
  period: string; // e.g. "Last 30 days"
  totalViews: number;
  avgCTR: number;
  avgRetentionPct: number;
  totalWatchHours: number;
  topVideos: VideoData[];
  topTopics: string[];
  winningFormats: string[];
  winningHooks: string[];
  recommendations: string[];
  warnings: string[];
  generatedAt: string;
}

// ─── Ideas ────────────────────────────────────────────────────────────────────

export type StrategyFit = 'strong' | 'moderate' | 'weak' | 'off-brand';
export type IdeaPriority = 'high' | 'medium' | 'low';
export type IdeaStatus = 'backlog' | 'planned' | 'in-production' | 'published' | 'rejected';

export interface VideoIdea {
  id: string;
  channelId: ChannelId;
  title: string;
  hook: string;
  angle: string;
  format: string;
  cluster: string;
  thumbnailConcept: string;
  shortsAngle?: string;
  repurposingIdeas: string[];
  strategyFit: StrategyFit;
  fitReason: string;
  priority: IdeaPriority;
  status: IdeaStatus;
  createdAt: string;
  notes?: string;
  aiGenerated: boolean;
}

// ─── Content Plan ─────────────────────────────────────────────────────────────

export type ProductionStatus =
  | 'planned'
  | 'scripting'
  | 'voiceover'
  | 'filming'
  | 'editing'
  | 'scheduled'
  | 'published';

export interface PromotionTask {
  id: string;
  task: string;
  platform: string;
  dueAfterPublish: string; // e.g. "Same day", "Day 3", "Week 1"
  done: boolean;
}

export interface ContentPlanItem {
  id: string;
  channelId: ChannelId;
  ideaId?: string;
  title: string;
  week: 1 | 2 | 3 | 4;
  month: number; // 1–12
  year: number;
  format: string;
  status: ProductionStatus;
  promotionChecklist: PromotionTask[];
  notes?: string;
}

// ─── Manual Notes ─────────────────────────────────────────────────────────────

export type NoteType = 'win' | 'failure' | 'observation' | 'audience-signal';

export interface ManualNote {
  id: string;
  channelId: ChannelId;
  content: string;
  type: NoteType;
  createdAt: string;
}

// ─── App State ────────────────────────────────────────────────────────────────

export interface AppState {
  selectedChannel: ChannelId;
  apiKey: string;
  analytics: Record<ChannelId, AnalyticsUpload | null>;
  healthSummaries: Record<ChannelId, ChannelHealthSummary | null>;
  ideas: VideoIdea[];
  contentPlan: ContentPlanItem[];
  notes: ManualNote[];
}

export type AppAction =
  | { type: 'SET_CHANNEL'; payload: ChannelId }
  | { type: 'SET_API_KEY'; payload: string }
  | { type: 'SET_ANALYTICS'; payload: AnalyticsUpload }
  | { type: 'SET_HEALTH_SUMMARY'; payload: ChannelHealthSummary }
  | { type: 'ADD_IDEA'; payload: VideoIdea }
  | { type: 'ADD_IDEAS'; payload: VideoIdea[] }
  | { type: 'UPDATE_IDEA'; payload: VideoIdea }
  | { type: 'REMOVE_IDEA'; payload: string }
  | { type: 'ADD_PLAN_ITEM'; payload: ContentPlanItem }
  | { type: 'UPDATE_PLAN_ITEM'; payload: ContentPlanItem }
  | { type: 'REMOVE_PLAN_ITEM'; payload: string }
  | { type: 'ADD_NOTE'; payload: ManualNote }
  | { type: 'REMOVE_NOTE'; payload: string }
  | { type: 'LOAD_STATE'; payload: Partial<AppState> };
