import React, { useState } from 'react';
import { useAppState, useAppDispatch } from '../store/AppContext';
import { getChannel } from '../data/channels';
import {
  PageHeader,
  Btn,
  Spinner,
  EmptyState,
  Badge,
} from '../components/Layout';
import { generateMarketingPlan } from '../utils/claudeApi';
import { buildPromotionChecklist } from '../utils/strategyEngine';
import { ContentPlanItem, ProductionStatus, PromotionTask } from '../types';

const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

const STATUS_COLORS: Record<ProductionStatus, string> = {
  planned: '#3b82f6',
  scripting: '#8b5cf6',
  voiceover: '#f59e0b',
  filming: '#f97316',
  editing: '#ec4899',
  scheduled: '#06b6d4',
  published: '#22c55e',
};

export default function MarketingPlanner() {
  const state = useAppState();
  const dispatch = useAppDispatch();
  const channel = getChannel(state.selectedChannel)!;

  const now = new Date();
  const [viewMonth, setViewMonth] = useState(now.getMonth() + 1);
  const [viewYear, setViewYear] = useState(now.getFullYear());
  const [tab, setTab] = useState<'calendar' | 'plan' | 'repurpose'>('calendar');
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [aiPlan, setAiPlan] = useState<AiPlan | null>(null);

  // Add video form
  const [showAddForm, setShowAddForm] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newWeek, setNewWeek] = useState<1 | 2 | 3 | 4>(1);
  const [newFormat, setNewFormat] = useState('');

  const planItems = state.contentPlan.filter(
    (p) => p.channelId === state.selectedChannel && p.month === viewMonth && p.year === viewYear
  );

  const allIdeas = state.ideas.filter(
    (i) => i.channelId === state.selectedChannel && i.status !== 'rejected'
  );

  async function handleGeneratePlan() {
    if (!state.apiKey) {
      setError('Set your Anthropic API key in Settings first.');
      return;
    }
    setGenerating(true);
    setError('');
    try {
      const upcomingVideos = planItems.map((p) => p.title);
      if (upcomingVideos.length === 0 && allIdeas.length > 0) {
        upcomingVideos.push(...allIdeas.slice(0, 5).map((i) => i.title));
      }
      const raw = await generateMarketingPlan(
        state.apiKey,
        channel.name,
        channel.id,
        upcomingVideos,
        channel.strategy.repurposingRules
      );
      const parsed = JSON.parse(raw) as AiPlan;
      setAiPlan(parsed);
      setTab('plan');
    } catch (err) {
      setError(`Failed to generate plan: ${err}`);
    } finally {
      setGenerating(false);
    }
  }

  function addPlanItem() {
    if (!newTitle.trim()) return;
    const item: ContentPlanItem = {
      id: `plan-${Date.now()}`,
      channelId: state.selectedChannel,
      title: newTitle.trim(),
      week: newWeek,
      month: viewMonth,
      year: viewYear,
      format: newFormat || channel.strategy.contentFormats[0],
      status: 'planned',
      promotionChecklist: buildPromotionChecklist(state.selectedChannel),
    };
    dispatch({ type: 'ADD_PLAN_ITEM', payload: item });
    setNewTitle('');
    setNewWeek(1);
    setNewFormat('');
    setShowAddForm(false);
  }

  function updateItemStatus(item: ContentPlanItem, status: ProductionStatus) {
    dispatch({ type: 'UPDATE_PLAN_ITEM', payload: { ...item, status } });
  }

  function togglePromoTask(item: ContentPlanItem, taskId: string) {
    const updated: ContentPlanItem = {
      ...item,
      promotionChecklist: item.promotionChecklist.map((t) =>
        t.id === taskId ? { ...t, done: !t.done } : t
      ),
    };
    dispatch({ type: 'UPDATE_PLAN_ITEM', payload: updated });
  }

  function prevMonth() {
    if (viewMonth === 1) {
      setViewMonth(12);
      setViewYear((y) => y - 1);
    } else {
      setViewMonth((m) => m - 1);
    }
  }

  function nextMonth() {
    if (viewMonth === 12) {
      setViewMonth(1);
      setViewYear((y) => y + 1);
    } else {
      setViewMonth((m) => m + 1);
    }
  }

  return (
    <div className="h-full flex flex-col">
      <PageHeader
        title="Marketing Planner"
        subtitle={`${channel.name} — monthly content calendar and promotion planning`}
        channelColor={channel.color}
        actions={
          <div className="flex items-center gap-2">
            <Btn onClick={() => setShowAddForm((s) => !s)}>
              + Add Video
            </Btn>
            <Btn
              variant="primary"
              onClick={handleGeneratePlan}
              disabled={generating || !state.apiKey}
            >
              {generating ? '⏳ Generating…' : '✨ Generate Plan'}
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
        {(['calendar', 'plan', 'repurpose'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium rounded-t-lg transition-all ${
              tab === t ? 'text-white border-b-2 -mb-px' : 'text-[#555] hover:text-[#888]'
            }`}
            style={tab === t ? { borderBottomColor: channel.color } : {}}
          >
            {t === 'calendar' ? 'Content Calendar' : t === 'plan' ? 'Monthly Plan' : 'Repurposing'}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto px-8 py-6">
        {/* CALENDAR TAB */}
        {tab === 'calendar' && (
          <div className="space-y-5">
            {/* Month nav */}
            <div className="flex items-center gap-4">
              <button
                onClick={prevMonth}
                className="w-8 h-8 rounded-lg bg-[#1A1A1A] text-[#666] hover:text-white hover:bg-[#2A2A2A] transition-all flex items-center justify-center"
              >
                ←
              </button>
              <h2 className="text-base font-semibold text-white min-w-[160px] text-center">
                {MONTHS[viewMonth - 1]} {viewYear}
              </h2>
              <button
                onClick={nextMonth}
                className="w-8 h-8 rounded-lg bg-[#1A1A1A] text-[#666] hover:text-white hover:bg-[#2A2A2A] transition-all flex items-center justify-center"
              >
                →
              </button>
            </div>

            {/* Add form */}
            {showAddForm && (
              <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5 space-y-3">
                <h3 className="text-sm font-semibold text-white">Add Video to Plan</h3>
                <div className="flex gap-3">
                  <input
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                    placeholder="Video title"
                    className="flex-1 bg-[#0D0D0D] border border-[#2A2A2A] rounded-lg px-3 py-2 text-sm text-white placeholder-[#444] focus:outline-none focus:border-[#444]"
                    onKeyDown={(e) => e.key === 'Enter' && addPlanItem()}
                  />
                  <select
                    value={newWeek}
                    onChange={(e) => setNewWeek(Number(e.target.value) as 1 | 2 | 3 | 4)}
                    className="bg-[#0D0D0D] border border-[#2A2A2A] rounded-lg px-3 py-2 text-sm text-[#888] focus:outline-none"
                  >
                    {[1, 2, 3, 4].map((w) => (
                      <option key={w} value={w}>
                        Week {w}
                      </option>
                    ))}
                  </select>
                  <select
                    value={newFormat}
                    onChange={(e) => setNewFormat(e.target.value)}
                    className="bg-[#0D0D0D] border border-[#2A2A2A] rounded-lg px-3 py-2 text-sm text-[#888] focus:outline-none"
                  >
                    <option value="">Format…</option>
                    {channel.strategy.contentFormats.map((f) => (
                      <option key={f} value={f}>
                        {f}
                      </option>
                    ))}
                  </select>
                  <Btn variant="primary" onClick={addPlanItem} disabled={!newTitle.trim()}>
                    Add
                  </Btn>
                </div>

                {/* Quick add from backlog */}
                {allIdeas.filter((i) => i.status === 'backlog').length > 0 && (
                  <div>
                    <p className="text-[11px] text-[#444] uppercase tracking-wider mb-2">
                      Quick-add from Backlog
                    </p>
                    <div className="flex flex-wrap gap-1.5">
                      {allIdeas
                        .filter((i) => i.status === 'backlog')
                        .slice(0, 6)
                        .map((idea) => (
                          <button
                            key={idea.id}
                            onClick={() => {
                              setNewTitle(idea.title);
                              setNewFormat(idea.format);
                            }}
                            className="text-xs px-2.5 py-1.5 bg-[#1A1A1A] text-[#777] hover:text-white rounded-lg border border-[#2A2A2A] hover:border-[#3A3A3A] transition-all truncate max-w-[200px]"
                          >
                            {idea.title}
                          </button>
                        ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Week columns */}
            {!planItems.length && !showAddForm ? (
              <EmptyState
                icon="📅"
                title="No videos planned"
                description="Add videos to your content calendar for this month."
                action={<Btn onClick={() => setShowAddForm(true)}>+ Add Video</Btn>}
              />
            ) : (
              <div className="grid grid-cols-4 gap-4">
                {([1, 2, 3, 4] as const).map((week) => {
                  const weekItems = planItems.filter((p) => p.week === week);
                  return (
                    <div key={week} className="min-h-[200px]">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="text-xs font-semibold text-[#555] uppercase tracking-wider">
                          Week {week}
                        </h3>
                        <span className="text-[10px] text-[#333]">{weekItems.length} videos</span>
                      </div>
                      <div className="space-y-2">
                        {weekItems.map((item) => (
                          <CalendarCard
                            key={item.id}
                            item={item}
                            channelColor={channel.color}
                            onStatusChange={(s) => updateItemStatus(item, s)}
                            onRemove={() =>
                              dispatch({ type: 'REMOVE_PLAN_ITEM', payload: item.id })
                            }
                          />
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* Promotion checklists */}
            {planItems.some((p) => p.promotionChecklist.length > 0) && (
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-white">Post-Publish Promotion Checklists</h3>
                {planItems.map((item) => (
                  <div key={item.id} className="bg-[#111] border border-[#1E1E1E] rounded-xl p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-sm font-medium text-white">{item.title}</p>
                        <p className="text-[11px] text-[#444] mt-0.5">Week {item.week}</p>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <div
                          className="w-1.5 h-1.5 rounded-full"
                          style={{ background: STATUS_COLORS[item.status] }}
                        />
                        <span className="text-[11px] text-[#555] capitalize">{item.status}</span>
                      </div>
                    </div>
                    <div className="space-y-1.5">
                      {item.promotionChecklist.map((task) => (
                        <PromoTaskRow
                          key={task.id}
                          task={task}
                          channelColor={channel.color}
                          onToggle={() => togglePromoTask(item, task.id)}
                        />
                      ))}
                    </div>
                    <div className="mt-2 flex items-center gap-2">
                      <div className="flex-1 bg-[#1A1A1A] rounded-full h-1 overflow-hidden">
                        <div
                          className="h-full rounded-full transition-all"
                          style={{
                            background: channel.color,
                            width: `${
                              item.promotionChecklist.length > 0
                                ? (item.promotionChecklist.filter((t) => t.done).length /
                                    item.promotionChecklist.length) *
                                  100
                                : 0
                            }%`,
                          }}
                        />
                      </div>
                      <span className="text-[11px] text-[#444]">
                        {item.promotionChecklist.filter((t) => t.done).length}/
                        {item.promotionChecklist.length} done
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* AI PLAN TAB */}
        {tab === 'plan' && (
          <div className="space-y-5">
            {generating ? (
              <Spinner />
            ) : aiPlan ? (
              <>
                {/* Monthly theme */}
                <div
                  className="rounded-xl p-5 border"
                  style={{
                    background: `${channel.color}0D`,
                    borderColor: `${channel.color}30`,
                  }}
                >
                  <p className="text-[11px] text-[#555] uppercase tracking-wider mb-1">
                    Monthly Theme
                  </p>
                  <p className="text-lg font-semibold text-white">{aiPlan.monthlyTheme}</p>
                </div>

                {/* Weekly focus */}
                <div className="grid grid-cols-2 gap-4">
                  {(aiPlan.weeklyFocus ?? []).map((w) => (
                    <div key={w.week} className="bg-[#111] border border-[#1E1E1E] rounded-xl p-4">
                      <p
                        className="text-[11px] font-semibold uppercase tracking-wider mb-1"
                        style={{ color: channel.color }}
                      >
                        Week {w.week}
                      </p>
                      <p className="text-sm text-white font-medium">{w.focus}</p>
                      <p className="text-xs text-[#555] mt-1">{w.keyAction}</p>
                    </div>
                  ))}
                </div>

                {/* Channel growth actions */}
                {aiPlan.channelGrowthActions?.length > 0 && (
                  <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
                    <h3 className="text-sm font-semibold text-white mb-3">
                      Channel Growth Actions This Month
                    </h3>
                    <ol className="space-y-2">
                      {aiPlan.channelGrowthActions.map((action, i) => (
                        <li key={i} className="flex gap-3 items-start">
                          <span
                            className="flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold"
                            style={{ background: `${channel.color}22`, color: channel.color }}
                          >
                            {i + 1}
                          </span>
                          <p className="text-sm text-[#999]">{action}</p>
                        </li>
                      ))}
                    </ol>
                  </div>
                )}

                {/* Promotion checklist */}
                {aiPlan.promotionChecklist?.length > 0 && (
                  <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
                    <h3 className="text-sm font-semibold text-white mb-3">
                      Default Promotion Checklist
                    </h3>
                    <div className="space-y-2">
                      {aiPlan.promotionChecklist.map((t, i) => (
                        <div key={i} className="flex items-center gap-3">
                          <div
                            className="w-1.5 h-1.5 rounded-full flex-shrink-0"
                            style={{ background: channel.color }}
                          />
                          <div className="flex-1">
                            <span className="text-sm text-[#ccc]">{t.task}</span>
                          </div>
                          <Badge label={t.platform} color="#1A1A1A" textColor="#666" />
                          <span className="text-[11px] text-[#444]">{t.dueAfterPublish}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <EmptyState
                icon="📋"
                title="No plan generated"
                description="Click Generate Plan to create an AI-powered monthly marketing strategy for this channel."
                action={
                  <Btn variant="primary" onClick={handleGeneratePlan} disabled={!state.apiKey}>
                    ✨ Generate Plan
                  </Btn>
                }
              />
            )}
          </div>
        )}

        {/* REPURPOSE TAB */}
        {tab === 'repurpose' && (
          <div className="space-y-5">
            {/* Channel repurposing rules */}
            <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
              <h3 className="text-sm font-semibold text-white mb-4">
                Repurposing Playbook — {channel.name}
              </h3>
              <div className="space-y-3">
                {channel.strategy.repurposingRules.map((rule, i) => {
                  const [platform, ...rest] = rule.split(':');
                  return (
                    <div key={i} className="flex gap-3 items-start">
                      <div
                        className="flex-shrink-0 px-2.5 py-1 rounded-md text-[11px] font-semibold"
                        style={{ background: `${channel.color}18`, color: channel.color }}
                      >
                        {platform.trim()}
                      </div>
                      <p className="text-sm text-[#888]">{rest.join(':').trim()}</p>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Shorts criteria */}
            <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
              <h3 className="text-sm font-semibold text-white mb-3">
                Shorts Selection Criteria
              </h3>
              <p className="text-xs text-[#555] mb-3">
                Use these to decide which moments from long-form videos to cut into Shorts.
              </p>
              <ul className="space-y-2">
                {channel.strategy.shortsCriteria.map((c, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span style={{ color: channel.color }} className="text-sm flex-shrink-0">
                      ✓
                    </span>
                    <span className="text-sm text-[#888]">{c}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* AI repurposing plan */}
            {(aiPlan?.repurposingPlan?.length ?? 0) > 0 && (
              <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
                <h3 className="text-sm font-semibold text-white mb-3">AI Repurposing Plan</h3>
                <div className="space-y-3">
                  {aiPlan?.repurposingPlan?.map((r, i) => (
                    <div key={i} className="flex gap-3 items-start pb-3 border-b border-[#1A1A1A] last:border-0 last:pb-0">
                      <Badge label={r.platform} color="#1A1A1A" textColor="#888" />
                      <div className="flex-1">
                        <p className="text-xs font-medium text-[#ccc]">{r.format}</p>
                        <p className="text-xs text-[#666] mt-0.5">{r.description}</p>
                        <p className="text-[11px] text-[#444] mt-1">{r.timing}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function CalendarCard({
  item,
  channelColor,
  onStatusChange,
  onRemove,
}: {
  item: ContentPlanItem;
  channelColor: string;
  onStatusChange: (s: ProductionStatus) => void;
  onRemove: () => void;
}) {
  return (
    <div className="bg-[#111] border border-[#1E1E1E] rounded-lg p-3 group">
      <div
        className="w-full h-0.5 rounded-full mb-2"
        style={{ background: STATUS_COLORS[item.status] }}
      />
      <p className="text-xs text-white font-medium leading-snug mb-2">{item.title}</p>
      <div className="flex items-center justify-between">
        <select
          value={item.status}
          onChange={(e) => onStatusChange(e.target.value as ProductionStatus)}
          className="bg-[#1A1A1A] border border-[#2A2A2A] rounded px-1.5 py-0.5 text-[10px] text-[#777] focus:outline-none"
        >
          {(Object.keys(STATUS_COLORS) as ProductionStatus[]).map((s) => (
            <option key={s} value={s}>
              {s.charAt(0).toUpperCase() + s.slice(1)}
            </option>
          ))}
        </select>
        <button
          onClick={onRemove}
          className="text-[#222] hover:text-red-500 text-xs transition-colors opacity-0 group-hover:opacity-100"
        >
          ✕
        </button>
      </div>
      {item.format && (
        <p className="text-[10px] text-[#444] mt-1.5">{item.format}</p>
      )}
    </div>
  );
}

function PromoTaskRow({
  task,
  channelColor,
  onToggle,
}: {
  task: PromotionTask;
  channelColor: string;
  onToggle: () => void;
}) {
  return (
    <div
      className="flex items-center gap-3 cursor-pointer group"
      onClick={onToggle}
    >
      <div
        className="w-4 h-4 rounded border flex items-center justify-center flex-shrink-0 transition-all"
        style={
          task.done
            ? { background: channelColor, borderColor: channelColor }
            : { background: 'transparent', borderColor: '#333' }
        }
      >
        {task.done && <span className="text-[9px] text-black font-bold">✓</span>}
      </div>
      <div className="flex-1 flex items-center gap-2">
        <span
          className={`text-xs transition-all ${
            task.done ? 'text-[#444] line-through' : 'text-[#888] group-hover:text-[#ccc]'
          }`}
        >
          {task.task}
        </span>
      </div>
      <span className="text-[10px] text-[#333]">{task.dueAfterPublish}</span>
      <Badge label={task.platform} color="#1A1A1A" textColor="#444" />
    </div>
  );
}

// ─── Types for AI plan ────────────────────────────────────────────────────────

interface AiPlan {
  monthlyTheme: string;
  weeklyFocus: { week: number; focus: string; keyAction: string }[];
  channelGrowthActions: string[];
  promotionChecklist: { task: string; platform: string; dueAfterPublish: string }[];
  repurposingPlan: { format: string; platform: string; description: string; timing: string }[];
}
