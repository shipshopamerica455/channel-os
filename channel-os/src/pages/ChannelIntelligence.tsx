import React, { useState, useRef } from 'react';
import { useAppState, useAppDispatch } from '../store/AppContext';
import { getChannel } from '../data/channels';
import {
  PageHeader,
  MetricCard,
  Btn,
  Spinner,
  EmptyState,
  FitBadge,
  Badge,
} from '../components/Layout';
import {
  parseYouTubeCSV,
  summarizeAnalytics,
  formatAnalyticsForClaude,
} from '../utils/analyticsParser';
import { generateHealthSummary } from '../utils/claudeApi';
import { scoreChannelHealth } from '../utils/strategyEngine';
import { AnalyticsUpload, ChannelHealthSummary, ManualNote, NoteType } from '../types';

export default function ChannelIntelligence() {
  const state = useAppState();
  const dispatch = useAppDispatch();
  const channel = getChannel(state.selectedChannel)!;
  const analytics = state.analytics[state.selectedChannel];
  const summary = state.healthSummaries[state.selectedChannel];
  const notes = state.notes.filter((n) => n.channelId === state.selectedChannel);

  const [tab, setTab] = useState<'overview' | 'videos' | 'notes'>('overview');
  const [uploading, setUploading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [noteText, setNoteText] = useState('');
  const [noteType, setNoteType] = useState<NoteType>('observation');
  const fileRef = useRef<HTMLInputElement>(null);

  const summaryData = analytics ? summarizeAnalytics(analytics.videos) : null;
  const healthScore = summaryData
    ? scoreChannelHealth(
        summaryData.avgCTR,
        // estimate retention pct from avg duration (assume avg video 10 min)
        Math.min(100, (summaryData.avgRetentionSeconds / 600) * 100),
        analytics?.videos.length ?? 0
      )
    : null;

  async function handleFileUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setError('');
    try {
      const text = await file.text();
      const videos = parseYouTubeCSV(text);
      if (!videos.length) {
        setError('Could not parse CSV. Make sure it is a YouTube Studio analytics export.');
        return;
      }
      const upload: AnalyticsUpload = {
        channelId: state.selectedChannel,
        videos,
        uploadedAt: new Date().toISOString(),
        source: 'csv',
      };
      dispatch({ type: 'SET_ANALYTICS', payload: upload });
    } catch {
      setError('Failed to read file.');
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = '';
    }
  }

  async function handleGenerateSummary() {
    if (!state.apiKey) {
      setError('Set your Anthropic API key in Settings first.');
      return;
    }
    setGenerating(true);
    setError('');
    try {
      const analyticsText = analytics
        ? formatAnalyticsForClaude(analytics.videos)
        : 'No analytics data uploaded.';
      const notesText = notes.map((n) => `[${n.type}] ${n.content}`).join('\n');
      const raw = await generateHealthSummary(
        state.apiKey,
        channel.name,
        analyticsText,
        notesText
      );
      const parsed = JSON.parse(raw) as Omit<ChannelHealthSummary, 'channelId' | 'topVideos' | 'generatedAt'>;
      const healthSummary: ChannelHealthSummary = {
        ...parsed,
        channelId: state.selectedChannel,
        topVideos: analytics?.videos.slice(0, 5) ?? [],
        generatedAt: new Date().toISOString(),
      };
      dispatch({ type: 'SET_HEALTH_SUMMARY', payload: healthSummary });
    } catch (err) {
      setError(String(err));
    } finally {
      setGenerating(false);
    }
  }

  function addNote() {
    if (!noteText.trim()) return;
    const note: ManualNote = {
      id: `note-${Date.now()}`,
      channelId: state.selectedChannel,
      content: noteText.trim(),
      type: noteType,
      createdAt: new Date().toISOString(),
    };
    dispatch({ type: 'ADD_NOTE', payload: note });
    setNoteText('');
  }

  return (
    <div className="h-full flex flex-col">
      <PageHeader
        title="Channel Intelligence"
        subtitle={`${channel.name} — strategy analysis and performance tracking`}
        channelColor={channel.color}
        actions={
          <div className="flex items-center gap-2">
            <input
              ref={fileRef}
              type="file"
              accept=".csv"
              className="hidden"
              onChange={handleFileUpload}
            />
            <Btn onClick={() => fileRef.current?.click()} disabled={uploading}>
              {uploading ? '⏳ Uploading…' : '📤 Upload CSV'}
            </Btn>
            <Btn
              variant="primary"
              onClick={handleGenerateSummary}
              disabled={generating || !state.apiKey}
            >
              {generating ? '⏳ Analyzing…' : '✨ Generate Summary'}
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
        {(['overview', 'videos', 'notes'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium rounded-t-lg capitalize transition-all ${
              tab === t
                ? 'text-white border-b-2 -mb-px'
                : 'text-[#555] hover:text-[#888]'
            }`}
            style={tab === t ? { borderBottomColor: channel.color } : {}}
          >
            {t === 'overview' ? 'Overview' : t === 'videos' ? 'Video Data' : 'Notes & Signals'}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto px-8 py-6">
        {/* OVERVIEW TAB */}
        {tab === 'overview' && (
          <div className="space-y-6">
            {/* Metrics row */}
            {summaryData ? (
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard
                  label="Total Views"
                  value={summaryData.totalViews.toLocaleString()}
                  color={channel.color}
                />
                <MetricCard
                  label="Watch Hours"
                  value={summaryData.totalWatchHours.toLocaleString()}
                  sub="Total accumulated"
                />
                <MetricCard
                  label="Avg CTR"
                  value={`${summaryData.avgCTR}%`}
                  color={summaryData.avgCTR >= 4 ? '#22c55e' : summaryData.avgCTR >= 2 ? '#f59e0b' : '#ef4444'}
                />
                <MetricCard
                  label="Videos Analyzed"
                  value={summaryData.videoCount}
                  sub={`Uploaded ${analytics ? new Date(analytics.uploadedAt).toLocaleDateString() : ''}`}
                />
              </div>
            ) : (
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                {['Total Views', 'Watch Hours', 'Avg CTR', 'Videos'].map((l) => (
                  <MetricCard key={l} label={l} value="—" sub="Upload CSV to populate" />
                ))}
              </div>
            )}

            {/* Health score */}
            {healthScore && (
              <div
                className="rounded-xl p-5 border"
                style={{ background: `${healthScore.color}0D`, borderColor: `${healthScore.color}30` }}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-[#555] uppercase tracking-wider font-medium">
                      Channel Health Score
                    </p>
                    <p className="text-3xl font-bold mt-1" style={{ color: healthScore.color }}>
                      {healthScore.score}
                      <span className="text-sm font-normal text-[#555] ml-2">/100</span>
                    </p>
                  </div>
                  <span
                    className="text-sm font-semibold px-4 py-2 rounded-lg"
                    style={{ background: `${healthScore.color}22`, color: healthScore.color }}
                  >
                    {healthScore.label}
                  </span>
                </div>
              </div>
            )}

            {/* AI Summary */}
            {generating ? (
              <Spinner />
            ) : summary ? (
              <div className="space-y-4">
                <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-semibold text-white">Weekly Health Summary</h3>
                    <span className="text-[11px] text-[#444]">
                      Generated {new Date(summary.generatedAt).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-6">
                    <Section
                      title="Top Topics"
                      items={summary.topTopics}
                      color={channel.color}
                    />
                    <Section
                      title="Winning Formats"
                      items={summary.winningFormats}
                      color={channel.color}
                    />
                    <Section
                      title="Winning Hooks"
                      items={summary.winningHooks}
                      color={channel.color}
                    />
                    <Section
                      title="Warnings"
                      items={summary.warnings ?? []}
                      color="#ef4444"
                      bullet="⚠️"
                    />
                  </div>
                </div>

                <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
                  <h3 className="text-sm font-semibold text-white mb-3">
                    Growth Recommendations
                  </h3>
                  <ol className="space-y-2">
                    {(summary.recommendations ?? []).map((rec, i) => (
                      <li key={i} className="flex gap-3">
                        <span
                          className="flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold"
                          style={{ background: `${channel.color}22`, color: channel.color }}
                        >
                          {i + 1}
                        </span>
                        <p className="text-sm text-[#999]">{rec}</p>
                      </li>
                    ))}
                  </ol>
                </div>
              </div>
            ) : (
              <EmptyState
                icon="📊"
                title="No summary yet"
                description="Upload your YouTube analytics CSV, then click Generate Summary to get AI-powered channel intelligence."
              />
            )}

            {/* Strategy Rules */}
            <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
              <h3 className="text-sm font-semibold text-white mb-4">
                Channel Strategy Rules — {channel.name}
              </h3>
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <p className="text-[11px] font-medium text-[#444] uppercase tracking-wider mb-2">
                    Content Pillars
                  </p>
                  <ul className="space-y-1">
                    {channel.strategy.contentPillars.map((p, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <div
                          className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0"
                          style={{ background: channel.color }}
                        />
                        <span className="text-xs text-[#888]">{p}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="text-[11px] font-medium text-[#444] uppercase tracking-wider mb-2">
                    Avoid Topics
                  </p>
                  <ul className="space-y-1">
                    {channel.strategy.avoidTopics.map((t, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-red-500 text-xs mt-0.5">✕</span>
                        <span className="text-xs text-[#888]">{t}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* VIDEO DATA TAB */}
        {tab === 'videos' && (
          <div>
            {!analytics?.videos.length ? (
              <EmptyState
                icon="📹"
                title="No video data"
                description="Upload a YouTube Studio analytics CSV export to see your video performance."
                action={
                  <Btn onClick={() => fileRef.current?.click()}>📤 Upload CSV</Btn>
                }
              />
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-[#1E1E1E]">
                      {['Title', 'Views', 'CTR', 'Avg Duration', 'Watch Hrs', 'Published'].map(
                        (h) => (
                          <th
                            key={h}
                            className="text-left pb-3 pr-6 text-[11px] font-medium text-[#444] uppercase tracking-wider"
                          >
                            {h}
                          </th>
                        )
                      )}
                    </tr>
                  </thead>
                  <tbody>
                    {[...analytics.videos]
                      .sort((a, b) => b.views - a.views)
                      .map((v) => (
                        <tr key={v.id} className="border-b border-[#141414] hover:bg-[#111]">
                          <td className="py-3 pr-6 text-[#ccc] max-w-xs truncate">{v.title}</td>
                          <td className="py-3 pr-6 text-white font-medium">
                            {v.views.toLocaleString()}
                          </td>
                          <td
                            className="py-3 pr-6 font-medium"
                            style={{
                              color:
                                v.ctr >= 4 ? '#22c55e' : v.ctr >= 2 ? '#f59e0b' : '#ef4444',
                            }}
                          >
                            {v.ctr > 0 ? `${v.ctr}%` : '—'}
                          </td>
                          <td className="py-3 pr-6 text-[#777]">
                            {v.avgViewDurationSeconds > 0
                              ? `${Math.floor(v.avgViewDurationSeconds / 60)}m ${v.avgViewDurationSeconds % 60}s`
                              : '—'}
                          </td>
                          <td className="py-3 pr-6 text-[#777]">
                            {v.watchTimeHours > 0 ? v.watchTimeHours.toFixed(1) : '—'}
                          </td>
                          <td className="py-3 text-[#555]">
                            {v.publishedAt
                              ? new Date(v.publishedAt).toLocaleDateString()
                              : '—'}
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* NOTES TAB */}
        {tab === 'notes' && (
          <div className="space-y-4">
            {/* Add note */}
            <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
              <h3 className="text-sm font-semibold text-white mb-3">Add Note or Audience Signal</h3>
              <div className="flex gap-2 mb-3">
                {(['win', 'failure', 'observation', 'audience-signal'] as NoteType[]).map((t) => (
                  <button
                    key={t}
                    onClick={() => setNoteType(t)}
                    className="px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-all"
                    style={
                      noteType === t
                        ? {
                            background: `${channel.color}22`,
                            color: channel.color,
                            border: `1px solid ${channel.color}44`,
                          }
                        : {
                            background: '#1A1A1A',
                            color: '#555',
                            border: '1px solid #2A2A2A',
                          }
                    }
                  >
                    {t === 'win' ? '🏆 Win' : t === 'failure' ? '💥 Failure' : t === 'observation' ? '👁 Observation' : '💬 Audience'}
                  </button>
                ))}
              </div>
              <textarea
                value={noteText}
                onChange={(e) => setNoteText(e.target.value)}
                placeholder="Describe what happened, what you noticed, or what the audience is saying…"
                rows={3}
                className="w-full bg-[#0D0D0D] border border-[#2A2A2A] rounded-lg px-3 py-2.5 text-sm text-white placeholder-[#444] focus:outline-none focus:border-[#444] resize-none"
              />
              <div className="mt-2 flex justify-end">
                <Btn variant="primary" onClick={addNote} disabled={!noteText.trim()}>
                  Add Note
                </Btn>
              </div>
            </div>

            {/* Note list */}
            {!notes.length ? (
              <EmptyState
                icon="📝"
                title="No notes yet"
                description="Record wins, failures, and audience signals to feed better AI analysis and idea generation."
              />
            ) : (
              <div className="space-y-2">
                {notes.map((note) => (
                  <div
                    key={note.id}
                    className="bg-[#111] border border-[#1E1E1E] rounded-xl px-4 py-3 flex items-start gap-3"
                  >
                    <span className="text-base mt-0.5">
                      {note.type === 'win' ? '🏆' : note.type === 'failure' ? '💥' : note.type === 'audience-signal' ? '💬' : '👁'}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-[#ccc]">{note.content}</p>
                      <p className="text-[11px] text-[#444] mt-1">
                        {new Date(note.createdAt).toLocaleDateString()}
                      </p>
                    </div>
                    <button
                      onClick={() => dispatch({ type: 'REMOVE_NOTE', payload: note.id })}
                      className="text-[#333] hover:text-[#666] text-sm transition-colors"
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function Section({
  title,
  items,
  color,
  bullet = '•',
}: {
  title: string;
  items: string[];
  color: string;
  bullet?: string;
}) {
  return (
    <div>
      <p className="text-[11px] font-medium text-[#444] uppercase tracking-wider mb-2">{title}</p>
      <ul className="space-y-1">
        {items.map((item, i) => (
          <li key={i} className="flex items-start gap-2">
            <span style={{ color }} className="text-xs mt-0.5 flex-shrink-0">
              {bullet}
            </span>
            <span className="text-xs text-[#888]">{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
