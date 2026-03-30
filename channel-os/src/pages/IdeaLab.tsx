import React, { useState } from 'react';
import { useAppState, useAppDispatch } from '../store/AppContext';
import { getChannel } from '../data/channels';
import {
  PageHeader,
  Btn,
  Spinner,
  EmptyState,
  FitBadge,
  Badge,
} from '../components/Layout';
import { generateVideoIdeas, generateContentClusters } from '../utils/claudeApi';
import { groupIdeasIntoClusters, deduplicateIdeas, checkStrategyFit } from '../utils/strategyEngine';
import { formatAnalyticsForClaude } from '../utils/analyticsParser';
import { VideoIdea, IdeaStatus, StrategyFit } from '../types';

const STATUS_LABELS: Record<IdeaStatus, string> = {
  backlog: 'Backlog',
  planned: 'Planned',
  'in-production': 'In Production',
  published: 'Published',
  rejected: 'Rejected',
};

const STATUS_COLORS: Record<IdeaStatus, string> = {
  backlog: '#555',
  planned: '#3b82f6',
  'in-production': '#f59e0b',
  published: '#22c55e',
  rejected: '#555',
};

const FIT_ORDER: StrategyFit[] = ['strong', 'moderate', 'weak', 'off-brand'];

export default function IdeaLab() {
  const state = useAppState();
  const dispatch = useAppDispatch();
  const channel = getChannel(state.selectedChannel)!;
  const analytics = state.analytics[state.selectedChannel];
  const notes = state.notes.filter((n) => n.channelId === state.selectedChannel);

  const ideas = state.ideas.filter((i) => i.channelId === state.selectedChannel);

  const [tab, setTab] = useState<'backlog' | 'clusters' | 'add'>('backlog');
  const [generating, setGenerating] = useState(false);
  const [generatingClusters, setGeneratingClusters] = useState(false);
  const [error, setError] = useState('');
  const [filterStatus, setFilterStatus] = useState<IdeaStatus | 'all'>('all');
  const [filterFit, setFilterFit] = useState<StrategyFit | 'all'>('all');
  const [clusters, setClusters] = useState<{ clusterName: string; pillar: string; description: string; videoIdeas: string[]; seriesPotential: boolean; seriesName: string | null }[]>([]);

  // Manual idea form
  const [manualTitle, setManualTitle] = useState('');
  const [manualHook, setManualHook] = useState('');
  const [manualFormat, setManualFormat] = useState('');
  const [manualCluster, setManualCluster] = useState('');

  const visibleIdeas = ideas.filter((idea) => {
    if (filterStatus !== 'all' && idea.status !== filterStatus) return false;
    if (filterFit !== 'all' && idea.strategyFit !== filterFit) return false;
    return true;
  });

  const clusters_grouped = groupIdeasIntoClusters(ideas.filter((i) => i.status !== 'rejected'));

  async function handleGenerateIdeas() {
    if (!state.apiKey) {
      setError('Set your Anthropic API key in Settings first.');
      return;
    }
    setGenerating(true);
    setError('');
    try {
      const analyticsContext = analytics
        ? formatAnalyticsForClaude(analytics.videos)
        : '';
      const notesContext = notes.map((n) => `[${n.type}] ${n.content}`).join('\n');
      const raw = await generateVideoIdeas(
        state.apiKey,
        channel.name,
        channel.strategy,
        analyticsContext,
        notesContext,
        8
      );
      const parsed = JSON.parse(raw) as Omit<VideoIdea, 'id' | 'channelId' | 'createdAt' | 'status' | 'aiGenerated'>[];
      const newIdeas: VideoIdea[] = parsed.map((idea) => ({
        ...idea,
        id: `idea-${Date.now()}-${Math.random().toString(36).slice(2)}`,
        channelId: state.selectedChannel,
        createdAt: new Date().toISOString(),
        status: 'backlog',
        aiGenerated: true,
        repurposingIdeas: idea.repurposingIdeas ?? [],
      }));
      const deduped = deduplicateIdeas(ideas, newIdeas);
      if (deduped.length > 0) {
        dispatch({ type: 'ADD_IDEAS', payload: deduped });
      }
    } catch (err) {
      setError(`Failed to generate ideas: ${err}`);
    } finally {
      setGenerating(false);
    }
  }

  async function handleGenerateClusters() {
    if (!state.apiKey) {
      setError('Set your Anthropic API key in Settings first.');
      return;
    }
    setGeneratingClusters(true);
    setError('');
    try {
      const topIdeas = ideas.slice(0, 20).map((i) => i.title);
      const raw = await generateContentClusters(
        state.apiKey,
        channel.name,
        { contentPillars: channel.strategy.contentPillars, targetAudience: channel.strategy.targetAudience },
        topIdeas
      );
      const parsed = JSON.parse(raw);
      setClusters(Array.isArray(parsed) ? parsed : []);
      setTab('clusters');
    } catch (err) {
      setError(`Failed to generate clusters: ${err}`);
    } finally {
      setGeneratingClusters(false);
    }
  }

  function addManualIdea() {
    if (!manualTitle.trim()) return;
    const { fit, reason } = checkStrategyFit(manualTitle, channel);
    const idea: VideoIdea = {
      id: `idea-manual-${Date.now()}`,
      channelId: state.selectedChannel,
      title: manualTitle.trim(),
      hook: manualHook.trim(),
      angle: '',
      format: manualFormat.trim() || channel.strategy.contentFormats[0],
      cluster: manualCluster.trim() || 'Unclustered',
      thumbnailConcept: '',
      repurposingIdeas: [],
      strategyFit: fit,
      fitReason: reason,
      priority: 'medium',
      status: 'backlog',
      createdAt: new Date().toISOString(),
      aiGenerated: false,
    };
    dispatch({ type: 'ADD_IDEA', payload: idea });
    setManualTitle('');
    setManualHook('');
    setManualFormat('');
    setManualCluster('');
    setTab('backlog');
  }

  function updateStatus(id: string, status: IdeaStatus) {
    const idea = ideas.find((i) => i.id === id);
    if (idea) dispatch({ type: 'UPDATE_IDEA', payload: { ...idea, status } });
  }

  function updatePriority(id: string, priority: 'high' | 'medium' | 'low') {
    const idea = ideas.find((i) => i.id === id);
    if (idea) dispatch({ type: 'UPDATE_IDEA', payload: { ...idea, priority } });
  }

  return (
    <div className="h-full flex flex-col">
      <PageHeader
        title="Idea Lab"
        subtitle={`${channel.name} — generate, score, and manage video ideas`}
        channelColor={channel.color}
        actions={
          <div className="flex items-center gap-2">
            <Btn
              onClick={handleGenerateClusters}
              disabled={generatingClusters || !state.apiKey}
            >
              {generatingClusters ? '⏳' : '🗂'} Clusters
            </Btn>
            <Btn
              variant="primary"
              onClick={handleGenerateIdeas}
              disabled={generating || !state.apiKey}
            >
              {generating ? '⏳ Generating…' : '✨ Generate Ideas'}
            </Btn>
          </div>
        }
      />

      {error && (
        <div className="mx-8 mt-4 px-4 py-3 rounded-lg bg-[#1f0a0a] border border-[#3d1515] text-sm text-red-400">
          {error}
        </div>
      )}

      {/* Tabs */}
      <div className="px-8 pt-6 flex gap-1 border-b border-[#1A1A1A]">
        {(['backlog', 'clusters', 'add'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium rounded-t-lg capitalize transition-all ${
              tab === t ? 'text-white border-b-2 -mb-px' : 'text-[#555] hover:text-[#888]'
            }`}
            style={tab === t ? { borderBottomColor: channel.color } : {}}
          >
            {t === 'backlog'
              ? `Backlog (${ideas.filter((i) => i.status !== 'rejected').length})`
              : t === 'clusters'
              ? 'Clusters & Series'
              : 'Add Manually'}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto px-8 py-6">
        {/* BACKLOG TAB */}
        {tab === 'backlog' && (
          <div className="space-y-4">
            {/* Filters */}
            <div className="flex items-center gap-3 flex-wrap">
              <FilterGroup
                label="Status"
                options={['all', ...Object.keys(STATUS_LABELS)] as ('all' | IdeaStatus)[]}
                value={filterStatus}
                onChange={(v) => setFilterStatus(v as 'all' | IdeaStatus)}
                getLabel={(v) => (v === 'all' ? 'All Status' : STATUS_LABELS[v as IdeaStatus])}
              />
              <FilterGroup
                label="Fit"
                options={['all', ...FIT_ORDER] as ('all' | StrategyFit)[]}
                value={filterFit}
                onChange={(v) => setFilterFit(v as 'all' | StrategyFit)}
                getLabel={(v) =>
                  v === 'all'
                    ? 'All Fit'
                    : v === 'strong'
                    ? 'Strong'
                    : v === 'moderate'
                    ? 'Moderate'
                    : v === 'weak'
                    ? 'Weak'
                    : 'Off-Brand'
                }
              />
              <span className="text-xs text-[#444]">{visibleIdeas.length} ideas</span>
            </div>

            {generating ? (
              <Spinner />
            ) : !visibleIdeas.length ? (
              <EmptyState
                icon="💡"
                title="No ideas yet"
                description="Click Generate Ideas to get AI-powered video ideas tailored to this channel's strategy, or add one manually."
                action={
                  <Btn variant="primary" onClick={handleGenerateIdeas} disabled={!state.apiKey}>
                    ✨ Generate Ideas
                  </Btn>
                }
              />
            ) : (
              <div className="space-y-3">
                {visibleIdeas.map((idea) => (
                  <IdeaCard
                    key={idea.id}
                    idea={idea}
                    channelColor={channel.color}
                    onStatusChange={(s) => updateStatus(idea.id, s)}
                    onPriorityChange={(p) => updatePriority(idea.id, p)}
                    onRemove={() => dispatch({ type: 'REMOVE_IDEA', payload: idea.id })}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* CLUSTERS TAB */}
        {tab === 'clusters' && (
          <div className="space-y-4">
            {generatingClusters ? (
              <Spinner />
            ) : clusters.length > 0 ? (
              <>
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-medium text-[#666]">AI-Generated Content Clusters</h3>
                  <Btn onClick={handleGenerateClusters} disabled={!state.apiKey}>
                    🔄 Regenerate
                  </Btn>
                </div>
                <div className="grid grid-cols-1 gap-4">
                  {clusters.map((c, i) => (
                    <div key={i} className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h4 className="text-sm font-semibold text-white">{c.clusterName}</h4>
                          <p className="text-xs text-[#555] mt-0.5">{c.pillar}</p>
                        </div>
                        {c.seriesPotential && (
                          <Badge
                            label={c.seriesName ?? 'Series'}
                            color={`${channel.color}22`}
                            textColor={channel.color}
                          />
                        )}
                      </div>
                      <p className="text-xs text-[#777] mb-3">{c.description}</p>
                      <div className="space-y-1">
                        {c.videoIdeas.map((title, j) => (
                          <div key={j} className="flex items-center gap-2">
                            <div
                              className="w-1 h-1 rounded-full flex-shrink-0"
                              style={{ background: channel.color }}
                            />
                            <span className="text-xs text-[#888]">{title}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : clusters_grouped.length > 0 ? (
              <>
                <p className="text-sm text-[#555]">
                  Clusters derived from your backlog. Use AI Clusters for deeper analysis.
                </p>
                {clusters_grouped.map((cluster) => (
                  <div key={cluster.name} className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
                    <h4 className="text-sm font-semibold text-white mb-3">{cluster.name}</h4>
                    <div className="space-y-2">
                      {cluster.ideas.map((idea) => (
                        <div key={idea.id} className="flex items-center gap-3">
                          <FitBadge fit={idea.strategyFit} />
                          <span className="text-xs text-[#888]">{idea.title}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </>
            ) : (
              <EmptyState
                icon="🗂"
                title="No clusters yet"
                description="Generate AI clusters to see content series and thematic groupings for this channel."
                action={
                  <Btn onClick={handleGenerateClusters} disabled={!state.apiKey}>
                    🗂 Generate Clusters
                  </Btn>
                }
              />
            )}
          </div>
        )}

        {/* ADD MANUALLY TAB */}
        {tab === 'add' && (
          <div className="max-w-xl">
            <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-6 space-y-4">
              <h3 className="text-sm font-semibold text-white">Add Video Idea Manually</h3>
              <Field label="Title *">
                <input
                  value={manualTitle}
                  onChange={(e) => setManualTitle(e.target.value)}
                  placeholder="e.g. How I Design 10 Canva Posts in 20 Minutes"
                  className="input-base w-full"
                />
              </Field>
              <Field label="Hook (opening line or visual idea)">
                <input
                  value={manualHook}
                  onChange={(e) => setManualHook(e.target.value)}
                  placeholder="e.g. Most people waste 2 hours on what takes me 20 minutes…"
                  className="input-base w-full"
                />
              </Field>
              <div className="grid grid-cols-2 gap-4">
                <Field label="Format">
                  <select
                    value={manualFormat}
                    onChange={(e) => setManualFormat(e.target.value)}
                    className="input-base w-full"
                  >
                    <option value="">Select format</option>
                    {channel.strategy.contentFormats.map((f) => (
                      <option key={f} value={f}>
                        {f}
                      </option>
                    ))}
                  </select>
                </Field>
                <Field label="Cluster / Series">
                  <input
                    value={manualCluster}
                    onChange={(e) => setManualCluster(e.target.value)}
                    placeholder="e.g. Canva Workflows"
                    className="input-base w-full"
                  />
                </Field>
              </div>

              {manualTitle && (
                <div className="p-3 rounded-lg bg-[#0D0D0D] border border-[#1E1E1E]">
                  <p className="text-[11px] text-[#444] uppercase tracking-wider mb-1">
                    Strategy Fit Preview
                  </p>
                  <div className="flex items-center gap-2">
                    <FitBadge fit={checkStrategyFit(manualTitle, channel).fit} />
                    <span className="text-xs text-[#666]">
                      {checkStrategyFit(manualTitle, channel).reason}
                    </span>
                  </div>
                </div>
              )}

              <Btn variant="primary" onClick={addManualIdea} disabled={!manualTitle.trim()}>
                Add to Backlog
              </Btn>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Idea Card ────────────────────────────────────────────────────────────────

function IdeaCard({
  idea,
  channelColor,
  onStatusChange,
  onPriorityChange,
  onRemove,
}: {
  idea: VideoIdea;
  channelColor: string;
  onStatusChange: (s: IdeaStatus) => void;
  onPriorityChange: (p: 'high' | 'medium' | 'low') => void;
  onRemove: () => void;
}) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div
      className="bg-[#111] border border-[#1E1E1E] rounded-xl overflow-hidden transition-all"
      style={idea.strategyFit === 'off-brand' ? { opacity: 0.6 } : {}}
    >
      {/* Header */}
      <div
        className="px-5 py-4 cursor-pointer hover:bg-[#141414] transition-all"
        onClick={() => setExpanded((e) => !e)}
      >
        <div className="flex items-start gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap mb-1">
              <FitBadge fit={idea.strategyFit} />
              <PriorityBadge priority={idea.priority} />
              {idea.aiGenerated && (
                <Badge label="AI" color="#1a1a2e" textColor="#818cf8" />
              )}
            </div>
            <h4 className="text-sm font-medium text-white leading-snug">{idea.title}</h4>
            {idea.hook && (
              <p className="text-xs text-[#555] mt-1 italic">"{idea.hook}"</p>
            )}
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            <select
              value={idea.status}
              onChange={(e) => {
                e.stopPropagation();
                onStatusChange(e.target.value as IdeaStatus);
              }}
              onClick={(e) => e.stopPropagation()}
              className="bg-[#1A1A1A] border border-[#2A2A2A] rounded-lg px-2 py-1 text-xs text-[#888] focus:outline-none"
            >
              {(Object.keys(STATUS_LABELS) as IdeaStatus[]).map((s) => (
                <option key={s} value={s}>
                  {STATUS_LABELS[s]}
                </option>
              ))}
            </select>
            <span className="text-[#333] text-xs">{expanded ? '▲' : '▼'}</span>
          </div>
        </div>
      </div>

      {/* Expanded details */}
      {expanded && (
        <div className="px-5 pb-5 space-y-3 border-t border-[#1A1A1A]">
          <div className="pt-3 grid grid-cols-2 gap-4">
            {idea.angle && (
              <DetailRow label="Angle" value={idea.angle} />
            )}
            {idea.format && (
              <DetailRow label="Format" value={idea.format} />
            )}
            {idea.cluster && (
              <DetailRow label="Cluster" value={idea.cluster} />
            )}
            {idea.thumbnailConcept && (
              <DetailRow label="Thumbnail Concept" value={idea.thumbnailConcept} />
            )}
          </div>

          {idea.shortsAngle && (
            <div className="p-3 rounded-lg bg-[#0D0D0D] border border-[#1E1E1E]">
              <p className="text-[11px] text-[#444] uppercase tracking-wider mb-1">
                Shorts Angle
              </p>
              <p className="text-xs text-[#888]">{idea.shortsAngle}</p>
            </div>
          )}

          {idea.repurposingIdeas?.length > 0 && (
            <div>
              <p className="text-[11px] text-[#444] uppercase tracking-wider mb-2">
                Repurposing Ideas
              </p>
              <div className="flex flex-wrap gap-1.5">
                {idea.repurposingIdeas.map((r, i) => (
                  <span key={i} className="text-[11px] px-2 py-1 bg-[#1A1A1A] text-[#666] rounded-md">
                    {r}
                  </span>
                ))}
              </div>
            </div>
          )}

          {idea.fitReason && (
            <p className="text-[11px] text-[#444] italic">{idea.fitReason}</p>
          )}

          <div className="flex items-center justify-between pt-1">
            <div className="flex items-center gap-1">
              {(['high', 'medium', 'low'] as const).map((p) => (
                <button
                  key={p}
                  onClick={() => onPriorityChange(p)}
                  className="px-2 py-1 rounded text-[10px] font-medium capitalize transition-all"
                  style={
                    idea.priority === p
                      ? { background: '#1E1E1E', color: '#fff', border: '1px solid #3A3A3A' }
                      : { background: 'transparent', color: '#444', border: '1px solid transparent' }
                  }
                >
                  {p}
                </button>
              ))}
            </div>
            <button
              onClick={onRemove}
              className="text-xs text-[#333] hover:text-red-500 transition-colors"
            >
              Remove
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-[10px] text-[#444] uppercase tracking-wider mb-0.5">{label}</p>
      <p className="text-xs text-[#888]">{value}</p>
    </div>
  );
}

function PriorityBadge({ priority }: { priority: string }) {
  const map: Record<string, { bg: string; text: string }> = {
    high: { bg: '#1f0a0a', text: '#ef4444' },
    medium: { bg: '#1c1917', text: '#f59e0b' },
    low: { bg: '#111', text: '#555' },
  };
  const s = map[priority] ?? map.low;
  return <Badge label={priority} color={s.bg} textColor={s.text} />;
}

function FilterGroup<T extends string>({
  label,
  options,
  value,
  onChange,
  getLabel,
}: {
  label: string;
  options: T[];
  value: T;
  onChange: (v: T) => void;
  getLabel: (v: T) => string;
}) {
  return (
    <div className="flex items-center gap-1">
      {options.map((opt) => (
        <button
          key={opt}
          onClick={() => onChange(opt)}
          className="px-2.5 py-1 rounded-lg text-[11px] font-medium transition-all"
          style={
            value === opt
              ? { background: '#1E1E1E', color: '#ccc', border: '1px solid #3A3A3A' }
              : { background: 'transparent', color: '#444', border: '1px solid transparent' }
          }
        >
          {getLabel(opt)}
        </button>
      ))}
    </div>
  );
}

function Field({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label className="text-[11px] font-medium text-[#555] uppercase tracking-wider block mb-1.5">
        {label}
      </label>
      {children}
    </div>
  );
}
