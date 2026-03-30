import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { CHANNELS } from '../data/channels';
import { useAppState, useAppDispatch } from '../store/AppContext';
import { ChannelId } from '../types';

const NAV_ITEMS = [
  { path: '/', label: 'Video Production', icon: '🎬', exact: true },
  { path: '/intelligence', label: 'Channel Intelligence', icon: '📊' },
  { path: '/ideas', label: 'Idea Lab', icon: '💡' },
  { path: '/marketing', label: 'Marketing Planner', icon: '📅' },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const state = useAppState();
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const [showSettings, setShowSettings] = useState(false);
  const [apiKeyInput, setApiKeyInput] = useState(state.apiKey);

  const selectedChannel = CHANNELS.find((c) => c.id === state.selectedChannel)!;

  function handleChannelChange(id: ChannelId) {
    dispatch({ type: 'SET_CHANNEL', payload: id });
  }

  function handleSaveKey() {
    dispatch({ type: 'SET_API_KEY', payload: apiKeyInput.trim() });
    setShowSettings(false);
  }

  return (
    <div className="flex h-screen bg-[#0A0A0A] text-white overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 flex-shrink-0 flex flex-col border-r border-[#1E1E1E] bg-[#0D0D0D]">
        {/* Logo */}
        <div className="px-5 py-5 border-b border-[#1E1E1E]">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-md flex items-center justify-center text-sm font-bold"
              style={{ background: `${selectedChannel.color}22`, border: `1px solid ${selectedChannel.color}44` }}>
              <span style={{ color: selectedChannel.color }}>C</span>
            </div>
            <div>
              <p className="text-sm font-semibold text-white leading-none">Channel OS</p>
              <p className="text-[10px] text-[#555] mt-0.5">Content Operating System</p>
            </div>
          </div>
        </div>

        {/* Channel Selector */}
        <div className="px-4 py-3 border-b border-[#1E1E1E]">
          <p className="text-[10px] font-medium text-[#444] uppercase tracking-widest mb-2">Active Channel</p>
          <div className="flex flex-col gap-1">
            {CHANNELS.map((ch) => (
              <button
                key={ch.id}
                onClick={() => handleChannelChange(ch.id as ChannelId)}
                className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-left transition-all"
                style={
                  state.selectedChannel === ch.id
                    ? { background: `${ch.color}18`, border: `1px solid ${ch.color}40` }
                    : { background: 'transparent', border: '1px solid transparent' }
                }
              >
                <div
                  className="w-2 h-2 rounded-full flex-shrink-0"
                  style={{
                    background: state.selectedChannel === ch.id ? ch.color : '#333',
                  }}
                />
                <span
                  className="text-xs font-medium truncate"
                  style={{ color: state.selectedChannel === ch.id ? ch.color : '#666' }}
                >
                  {ch.name}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 overflow-y-auto">
          <p className="text-[10px] font-medium text-[#444] uppercase tracking-widest px-2 mb-2">
            Navigation
          </p>
          <ul className="flex flex-col gap-0.5">
            {NAV_ITEMS.map((item) => (
              <li key={item.path}>
                <NavLink
                  to={item.path}
                  end={item.exact}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all ${
                      isActive
                        ? 'bg-[#1E1E1E] text-white font-medium'
                        : 'text-[#666] hover:text-[#999] hover:bg-[#141414]'
                    }`
                  }
                >
                  <span className="text-base leading-none">{item.icon}</span>
                  <span>{item.label}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        {/* Settings Footer */}
        <div className="px-3 py-3 border-t border-[#1E1E1E]">
          <button
            onClick={() => setShowSettings((s) => !s)}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-[#555] hover:text-[#888] hover:bg-[#141414] transition-all"
          >
            <span>⚙️</span>
            <span>Settings</span>
            {!state.apiKey && (
              <span className="ml-auto w-2 h-2 rounded-full bg-amber-500" title="API key not set" />
            )}
          </button>

          {showSettings && (
            <div className="mt-2 p-3 rounded-lg bg-[#141414] border border-[#2A2A2A]">
              <p className="text-[11px] text-[#555] mb-2">Anthropic API Key</p>
              <input
                type="password"
                value={apiKeyInput}
                onChange={(e) => setApiKeyInput(e.target.value)}
                placeholder="sk-ant-..."
                className="w-full bg-[#0D0D0D] border border-[#2A2A2A] rounded px-2 py-1.5 text-xs text-white placeholder-[#444] focus:outline-none focus:border-[#444] font-mono"
              />
              <button
                onClick={handleSaveKey}
                className="mt-2 w-full py-1.5 rounded text-xs font-medium bg-[#1E1E1E] text-[#888] hover:text-white hover:bg-[#2A2A2A] transition-all"
              >
                Save Key
              </button>
              {state.apiKey && (
                <p className="text-[10px] text-emerald-500 mt-1.5">
                  Key active
                </p>
              )}
            </div>
          )}
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}

// ─── Shared UI primitives ─────────────────────────────────────────────────────

export function PageHeader({
  title,
  subtitle,
  actions,
  channelColor,
}: {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
  channelColor?: string;
}) {
  return (
    <div className="px-8 py-6 border-b border-[#1A1A1A] flex items-start justify-between">
      <div>
        <div className="flex items-center gap-2">
          {channelColor && (
            <div className="w-1 h-5 rounded-full" style={{ background: channelColor }} />
          )}
          <h1 className="text-xl font-semibold text-white">{title}</h1>
        </div>
        {subtitle && <p className="text-sm text-[#555] mt-0.5 ml-3">{subtitle}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  );
}

export function MetricCard({
  label,
  value,
  sub,
  color,
}: {
  label: string;
  value: string | number;
  sub?: string;
  color?: string;
}) {
  return (
    <div className="bg-[#111] border border-[#1E1E1E] rounded-xl p-4">
      <p className="text-[11px] text-[#555] font-medium uppercase tracking-wider">{label}</p>
      <p
        className="text-2xl font-bold mt-1.5"
        style={{ color: color ?? '#fff' }}
      >
        {value}
      </p>
      {sub && <p className="text-[11px] text-[#444] mt-1">{sub}</p>}
    </div>
  );
}

export function Badge({
  label,
  color = '#333',
  textColor = '#999',
}: {
  label: string;
  color?: string;
  textColor?: string;
}) {
  return (
    <span
      className="inline-flex items-center px-2 py-0.5 rounded-md text-[10px] font-semibold uppercase tracking-wider"
      style={{ background: color, color: textColor }}
    >
      {label}
    </span>
  );
}

export function FitBadge({ fit }: { fit: string }) {
  const map: Record<string, { bg: string; text: string; label: string }> = {
    strong: { bg: '#052e16', text: '#22c55e', label: 'Strong Fit' },
    moderate: { bg: '#1c1917', text: '#f59e0b', label: 'Moderate Fit' },
    weak: { bg: '#1c1917', text: '#f97316', label: 'Weak Fit' },
    'off-brand': { bg: '#1f0a0a', text: '#ef4444', label: 'Off-Brand' },
  };
  const style = map[fit] ?? map.weak;
  return <Badge label={style.label} color={style.bg} textColor={style.text} />;
}

export function Spinner() {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="w-5 h-5 border-2 border-[#333] border-t-[#666] rounded-full animate-spin" />
    </div>
  );
}

export function EmptyState({
  icon,
  title,
  description,
  action,
}: {
  icon: string;
  title: string;
  description?: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center px-8">
      <div className="text-5xl mb-4 opacity-30">{icon}</div>
      <h3 className="text-base font-medium text-[#666]">{title}</h3>
      {description && (
        <p className="text-sm text-[#444] mt-1 max-w-sm">{description}</p>
      )}
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}

export function Btn({
  children,
  onClick,
  variant = 'default',
  disabled,
  className = '',
}: {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'default' | 'primary' | 'ghost' | 'danger';
  disabled?: boolean;
  className?: string;
}) {
  const base =
    'inline-flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all disabled:opacity-40 disabled:cursor-not-allowed';
  const variants = {
    default: 'bg-[#1A1A1A] border border-[#2A2A2A] text-[#999] hover:text-white hover:border-[#3A3A3A]',
    primary: 'bg-white text-black hover:bg-[#e5e5e5]',
    ghost: 'text-[#666] hover:text-[#999] hover:bg-[#141414]',
    danger: 'bg-[#1f0a0a] border border-[#3d1515] text-[#ef4444] hover:bg-[#2d1010]',
  };
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${base} ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  );
}
