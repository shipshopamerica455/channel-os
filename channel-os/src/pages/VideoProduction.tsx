import React, { useState } from 'react';
import { useAppState, useAppDispatch } from '../store/AppContext';
import { getChannel } from '../data/channels';
import { PageHeader, Btn, Badge, MetricCard } from '../components/Layout';
import { VideoIdea, VideoType } from '../types';

// Pipeline steps in order
const PIPELINE_STEPS = [
  {
    id: 'script',
    icon: '✍️',
    label: 'Script',
    description: 'Generate or write the video script',
    command: 'node generate-script.mjs',
    detail: 'Uses Claude API to write a structured 5-scene script. Edit SCRIPT object in CanvaTemplateVideo.tsx.',
  },
  {
    id: 'voice',
    icon: '🎙',
    label: 'Voiceover',
    description: 'Generate MP3s via ElevenLabs',
    command: 'npm run voiceover',
    detail: 'Reads each scene from the SCRIPT object and generates scene1.mp3 – scene5.mp3 via ElevenLabs turbo_v2.',
  },
  {
    id: 'images',
    icon: '🎨',
    label: 'Scene Images',
    description: 'Generate AI background images',
    command: 'node generate-images.mjs',
    detail: 'Uses Gemini or FAL.ai to generate scene1-bg.jpg – scene5-bg.jpg based on scene content.',
  },
  {
    id: 'render',
    icon: '🎬',
    label: 'Render',
    description: 'Render the final MP4 via Remotion',
    command: 'npm run render',
    detail: 'Remotion renders a 1080×1920 vertical Short at 30fps (~65 seconds). Output: /out/short.mp4',
  },
  {
    id: 'export',
    icon: '📦',
    label: 'Export',
    description: 'Your video is ready',
    command: 'open out/short.mp4',
    detail: 'The rendered MP4 is in remotion-shorts/out/short.mp4, ready to upload to YouTube Shorts.',
  },
];

const LONG_FORM_STEPS = [
  {
    id: 'research',
    icon: '🔍',
    label: 'Research & Outline',
    description: 'Define the topic, angle, and structure',
    command: '— (manual)',
    detail: 'Write a one-page outline: hook, 3–5 main sections, CTA. Use your Idea Lab angle and cluster context.',
  },
  {
    id: 'script-long',
    icon: '✍️',
    label: 'Script',
    description: 'Write the full script with timestamps',
    command: 'node generate-script.mjs',
    detail: 'Use Claude to generate a full long-form script. Aim for 1 word per second of target runtime (e.g. 1500 words = 10 min video).',
  },
  {
    id: 'record',
    icon: '🎙',
    label: 'Record / Film',
    description: 'Record voiceover or on-camera footage',
    command: '— (manual)',
    detail: 'Record to your DAW or camera. Keep takes short and clearly labeled by section for easier editing.',
  },
  {
    id: 'edit',
    icon: '✂️',
    label: 'Edit',
    description: 'Edit in Premiere / DaVinci / CapCut',
    command: '— (manual)',
    detail: 'Cut for pacing: no dead air, hook in first 30 seconds, chapters if over 8 minutes. Export 1080p or 4K.',
  },
  {
    id: 'thumbnail',
    icon: '🖼',
    label: 'Thumbnail',
    description: 'Design thumbnail in Canva',
    command: '— (manual)',
    detail: 'Use high-contrast text (3–5 words max), expressive face or bold visual, consistent channel style.',
  },
  {
    id: 'upload',
    icon: '📤',
    label: 'Upload & Optimize',
    description: 'Upload to YouTube with full metadata',
    command: '— (manual)',
    detail: 'Write SEO title, description with timestamps, tags. Add to playlist. Schedule or publish. Pin a comment.',
  },
];

const SCRIPT_STRUCTURE = [
  { scene: 1, name: 'Hook', duration: '9s', color: '#ef4444', desc: 'Attention-grabbing opening line — red pulsing overlay' },
  { scene: 2, name: 'Problem', duration: '12s', color: '#f97316', desc: 'State the pain point clearly — shaky animation, red text' },
  { scene: 3, name: 'Solution', duration: '17s', color: '#22c55e', desc: 'The fix or answer — green "THE FIX" badge, slide-in' },
  { scene: 4, name: 'Payoff', duration: '15s', color: '#3b82f6', desc: 'Results and transformation — scale animation' },
  { scene: 5, name: 'CTA', duration: '12s', color: '#8b5cf6', desc: 'Subscribe / call to action — pulsing button' },
];

export default function VideoProduction() {
  const state = useAppState();
  const dispatch = useAppDispatch();
  const channel = getChannel(state.selectedChannel)!;

  const [copiedStep, setCopiedStep] = useState<string | null>(null);
  const [activeStep, setActiveStep] = useState<string | null>(null);
  const [pipelineType, setPipelineType] = useState<VideoType>('long-form');

  const readyIdeas = state.ideas.filter(
    (i) => i.channelId === state.selectedChannel && i.status === 'planned'
  );

  function copyCommand(step: { id: string; command: string }) {
    navigator.clipboard.writeText(step.command);
    setCopiedStep(step.id);
    setTimeout(() => setCopiedStep(null), 1500);
  }

  function promoteIdea(idea: VideoIdea) {
    dispatch({ type: 'UPDATE_IDEA', payload: { ...idea, status: 'in-production' } });
  }

  const activePipeline = pipelineType === 'short' ? PIPELINE_STEPS : LONG_FORM_STEPS;

  return (
    <div className="h-full flex flex-col">
      <PageHeader
        title="Video Production"
        subtitle={pipelineType === 'short' ? 'Script → Voice → Scenes → Render → Export' : 'Research → Script → Record → Edit → Upload'}
        channelColor={channel.color}
        actions={
          <div className="flex items-center gap-1 p-1 rounded-lg bg-[#141414] border border-[#1E1E1E]">
            {(['long-form', 'short'] as VideoType[]).map((t) => (
              <button
                key={t}
                onClick={() => { setPipelineType(t); setActiveStep(null); }}
                className="px-4 py-1.5 rounded-md text-sm font-medium transition-all"
                style={
                  pipelineType === t
                    ? t === 'short'
                      ? { background: '#7c3aed22', color: '#a78bfa', border: '1px solid #7c3aed44' }
                      : { background: '#0369a122', color: '#38bdf8', border: '1px solid #0369a144' }
                    : { background: 'transparent', color: '#555', border: '1px solid transparent' }
                }
              >
                {t === 'long-form' ? '🎬 Long-form' : '⚡ Short'}
              </button>
            ))}
          </div>
        }
      />

      <div className="flex-1 overflow-y-auto px-8 py-6 space-y-6">
        {/* Quick stats */}
        <div className="grid grid-cols-3 gap-4">
          <MetricCard
            label="Ideas Ready to Produce"
            value={readyIdeas.length}
            color={channel.color}
            sub="Status: Planned"
          />
          <MetricCard
            label="In Production"
            value={state.ideas.filter((i) => i.channelId === state.selectedChannel && i.status === 'in-production').length}
            sub="Currently being made"
          />
          <MetricCard
            label="Published"
            value={state.ideas.filter((i) => i.channelId === state.selectedChannel && i.status === 'published').length}
            sub="Total published videos"
          />
        </div>

        {/* Ideas queued for production */}
        {readyIdeas.length > 0 && (
          <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
            <h3 className="text-sm font-semibold text-white mb-3">Ready to Produce</h3>
            <div className="space-y-2">
              {readyIdeas.map((idea) => (
                <div
                  key={idea.id}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-[#0D0D0D] border border-[#1E1E1E]"
                >
                  <div
                    className="w-2 h-2 rounded-full flex-shrink-0"
                    style={{ background: channel.color }}
                  />
                  <span className="text-sm text-white flex-1 truncate">{idea.title}</span>
                  <span className="text-xs text-[#555]">{idea.format}</span>
                  <Btn onClick={() => promoteIdea(idea)} variant="ghost" className="text-xs">
                    Start →
                  </Btn>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Pipeline */}
        <div>
          <div className="flex items-center gap-3 mb-4">
            <h3 className="text-sm font-semibold text-white">
              {pipelineType === 'short' ? '⚡ Shorts Pipeline' : '🎬 Long-form Pipeline'}
            </h3>
            <span className="text-xs text-[#444]">
              {pipelineType === 'short' ? 'Automated via Remotion + ElevenLabs' : 'Manual production checklist'}
            </span>
          </div>
          <div className="relative">
            {/* Connector line */}
            <div className="absolute left-6 top-6 bottom-6 w-px bg-[#1E1E1E]" />

            <div className="space-y-3">
              {activePipeline.map((step, i) => (
                <div
                  key={step.id}
                  className={`relative flex gap-4 cursor-pointer transition-all`}
                  onClick={() => setActiveStep(activeStep === step.id ? null : step.id)}
                >
                  {/* Circle */}
                  <div
                    className="flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center text-xl relative z-10 transition-all"
                    style={{
                      background: activeStep === step.id ? `${channel.color}22` : '#111',
                      border: activeStep === step.id
                        ? `1px solid ${channel.color}44`
                        : '1px solid #1E1E1E',
                    }}
                  >
                    {step.icon}
                  </div>

                  {/* Content */}
                  <div className="flex-1 bg-[#111] border border-[#1E1E1E] rounded-xl p-4 hover:border-[#2A2A2A] transition-all">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-[11px] font-medium text-[#444] uppercase tracking-wider">
                            Step {i + 1}
                          </span>
                        </div>
                        <h4 className="text-sm font-semibold text-white mt-0.5">{step.label}</h4>
                        <p className="text-xs text-[#555] mt-0.5">{step.description}</p>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          copyCommand(step);
                        }}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#1A1A1A] border border-[#2A2A2A] text-xs text-[#666] hover:text-white hover:border-[#3A3A3A] transition-all font-mono"
                      >
                        {copiedStep === step.id ? '✓ Copied' : step.command}
                      </button>
                    </div>

                    {activeStep === step.id && (
                      <div className="mt-3 pt-3 border-t border-[#1A1A1A]">
                        <p className="text-xs text-[#777]">{step.detail}</p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Script structure reference — Short only */}
        {pipelineType === 'short' && (
          <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
            <h3 className="text-sm font-semibold text-white mb-4">5-Scene Short Structure</h3>
            <div className="space-y-2">
              {SCRIPT_STRUCTURE.map((s) => (
                <div key={s.scene} className="flex items-center gap-4">
                  <div
                    className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold"
                    style={{ background: `${s.color}18`, color: s.color }}
                  >
                    {s.scene}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-white">{s.name}</span>
                      <span className="text-[11px] text-[#444]">{s.duration}</span>
                    </div>
                    <p className="text-xs text-[#555]">{s.desc}</p>
                  </div>
                  <div
                    className="h-1.5 rounded-full"
                    style={{
                      background: s.color,
                      width: `${(parseInt(s.duration) / 65) * 200}px`,
                      minWidth: '20px',
                      opacity: 0.6,
                    }}
                  />
                </div>
              ))}
            </div>
            <div className="mt-4 p-3 rounded-lg bg-[#0D0D0D] border border-[#1E1E1E]">
              <p className="text-[11px] text-[#555]">
                Edit the <span className="font-mono text-[#888]">SCRIPT</span> object in{' '}
                <span className="font-mono text-[#888]">remotion-shorts/src/CanvaTemplateVideo.tsx</span>{' '}
                to change content. All scenes update automatically on the next render.
              </p>
            </div>
          </div>
        )}

        {/* Long-form structure reference */}
        {pipelineType === 'long-form' && (
          <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
            <h3 className="text-sm font-semibold text-white mb-4">Long-form Structure Guide</h3>
            <div className="space-y-3">
              {[
                { label: 'Hook (0:00–0:30)', desc: 'State the payoff immediately — "By the end of this video you\'ll know…"', color: '#ef4444' },
                { label: 'Context (0:30–2:00)', desc: 'Why this matters. Brief credibility or story to earn trust.', color: '#f97316' },
                { label: 'Main Content (2:00–end–2:00)', desc: 'Core sections. Use chapters. One idea per section, clear transitions.', color: '#3b82f6' },
                { label: 'Recap (–2:00)', desc: 'Summarize the 3 key takeaways in 60 seconds.', color: '#22c55e' },
                { label: 'CTA (Final 30s)', desc: 'One clear action: subscribe, watch next, download, comment.', color: '#8b5cf6' },
              ].map((s, i) => (
                <div key={i} className="flex gap-3 items-start">
                  <div className="w-1 h-full min-h-[32px] rounded-full flex-shrink-0 mt-1" style={{ background: s.color, width: '3px' }} />
                  <div>
                    <p className="text-sm font-medium text-white">{s.label}</p>
                    <p className="text-xs text-[#555] mt-0.5">{s.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Environment check */}
        <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-5">
          <h3 className="text-sm font-semibold text-white mb-3">Environment Setup</h3>
          <div className="space-y-2">
            {[
              { label: 'Anthropic API Key', key: state.apiKey, hint: 'For script generation' },
            ].map(({ label, key, hint }) => (
              <div key={label} className="flex items-center gap-3">
                <div
                  className="w-2 h-2 rounded-full flex-shrink-0"
                  style={{ background: key ? '#22c55e' : '#ef4444' }}
                />
                <span className="text-sm text-[#888]">{label}</span>
                <span className="text-xs text-[#444]">{hint}</span>
                {!key && (
                  <span className="text-xs text-[#ef4444] ml-auto">Not set — see Settings</span>
                )}
              </div>
            ))}
            {[
              { label: 'ElevenLabs API Key', file: 'remotion-shorts/.env', hint: 'For voiceover generation' },
              { label: 'Google Gemini / FAL.ai Key', file: 'remotion-shorts/.env', hint: 'For image generation' },
            ].map(({ label, file, hint }) => (
              <div key={label} className="flex items-center gap-3">
                <div className="w-2 h-2 rounded-full flex-shrink-0 bg-[#f59e0b]" />
                <span className="text-sm text-[#888]">{label}</span>
                <span className="text-xs text-[#444]">{hint}</span>
                <span className="text-xs text-[#444] ml-auto font-mono">{file}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
