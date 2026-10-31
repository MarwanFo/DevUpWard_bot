import React, { useEffect, useState } from 'react';
import {
  Users,
  FolderGit2,
  Trophy,
  Coffee,
  Activity,
  Send,
  RefreshCw,
  MessageSquare,
  Sparkles,
} from 'lucide-react';
import { BotTelemetry, ContactSubmission, TeamStats } from '../types';
import ApiService from '../services/api';

export const OverviewPage: React.FC = () => {
  const [stats, setStats] = useState<TeamStats | null>(null);
  const [telemetry, setTelemetry] = useState<BotTelemetry | null>(null);
  const [recentInquiries, setRecentInquiries] = useState<ContactSubmission[]>([]);
  const [loading, setLoading] = useState(true);

  // Quick presence updater state
  const [statusText, setStatusText] = useState('🏆 Preparing for Next Hackathon');
  const [activityType, setActivityType] = useState('watching');
  const [updatingPresence, setUpdatingPresence] = useState(false);
  const [presenceMsg, setPresenceMsg] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsRes, telemetryRes, inboxRes] = await Promise.all([
        ApiService.getStats(),
        ApiService.getBotStatus(),
        ApiService.getInbox(),
      ]);
      setStats(statsRes.data);
      setTelemetry(telemetryRes.data);
      setRecentInquiries(inboxRes.data.slice(0, 5));
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleUpdatePresence = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setUpdatingPresence(true);
      setPresenceMsg('');
      const res = await ApiService.updatePresence(statusText, activityType);
      setPresenceMsg(res.data.message);
      loadData();
    } catch (err: any) {
      setPresenceMsg(err?.response?.data?.detail || 'Failed to update presence.');
    } finally {
      setUpdatingPresence(false);
    }
  };

  return (
    <div className="space-y-8">
      {loading && (
        <div className="text-xs text-indigo-400 font-mono animate-pulse">
          Syncing latest telemetry and metrics...
        </div>
      )}
      {/* Top Welcome & Bot Telemetry */}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Team Banner */}
        <div className="lg:col-span-2 bg-gradient-to-br from-indigo-950/60 via-slate-900 to-slate-900 border border-slate-800 rounded-3xl p-7 relative overflow-hidden flex flex-col justify-between shadow-xl">
          <div className="space-y-3 z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <Sparkles className="w-3.5 h-3.5" />
              DevUpward Hackathon HQ
            </div>
            <h2 className="text-2xl font-bold tracking-tight text-white">
              Official Team Showcase & Portfolio Bot
            </h2>
            <p className="text-slate-400 text-sm max-w-xl">
              Manage your squad roster, hackathon showroom prototypes, podium awards, and live Discord bot presence in one unified cockpit.
            </p>
          </div>

          <div className="pt-6 border-t border-slate-800/80 flex items-center gap-4 text-xs text-slate-400 z-10">
            <span>Unified Async Architecture</span>
            <span>•</span>
            <span>Python FastAPI + discord.py</span>
            <span>•</span>
            <span>React 19 Dashboard</span>
          </div>

          {/* Decorative glow */}
          <div className="absolute top-0 right-0 w-80 h-80 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />
        </div>

        {/* Live Bot Gateway Telemetry */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 flex flex-col justify-between shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-slate-800 flex items-center justify-center text-slate-300">
                <Activity className="w-4 h-4" />
              </div>
              <h3 className="font-semibold text-white text-sm">Bot Telemetry</h3>
            </div>
            <button
              onClick={loadData}
              className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
              title="Refresh"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>

          <div className="grid grid-cols-2 gap-4 py-4">
            <div className="bg-slate-950 p-3.5 rounded-2xl border border-slate-800/80">
              <span className="text-[11px] font-medium text-slate-400 block mb-1">Gateway Ping</span>
              <span className="text-xl font-bold text-white font-mono">
                {telemetry?.latency_ms || 0}
                <span className="text-xs font-normal text-slate-500 ml-1">ms</span>
              </span>
            </div>
            <div className="bg-slate-950 p-3.5 rounded-2xl border border-slate-800/80">
              <span className="text-[11px] font-medium text-slate-400 block mb-1">Servers</span>
              <span className="text-xl font-bold text-white font-mono">
                {telemetry?.guild_count || 0}
              </span>
            </div>
            <div className="bg-slate-950 p-3.5 rounded-2xl border border-slate-800/80">
              <span className="text-[11px] font-medium text-slate-400 block mb-1">Status</span>
              <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1.5 mt-1">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                {telemetry?.is_online ? 'Gateway Live' : 'API Standby'}
              </span>
            </div>
            <div className="bg-slate-950 p-3.5 rounded-2xl border border-slate-800/80">
              <span className="text-[11px] font-medium text-slate-400 block mb-1">Uptime</span>
              <span className="text-sm font-bold text-slate-300 font-mono mt-1 block">
                {Math.floor((telemetry?.uptime_seconds || 0) / 60)} mins
              </span>
            </div>
          </div>

          <div className="text-[11px] text-slate-500 font-mono truncate">
            User: {telemetry?.bot_user || 'ShowcaseBot (Standby)'}
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center border border-blue-500/20">
            <Users className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-slate-400 font-medium block">Core Members</span>
            <span className="text-2xl font-bold text-white font-mono">
              {stats?.total_members || 0}
            </span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center border border-purple-500/20">
            <FolderGit2 className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-slate-400 font-medium block">Prototypes</span>
            <span className="text-2xl font-bold text-white font-mono">
              {stats?.total_projects || 0}
            </span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center border border-amber-500/20">
            <Trophy className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-slate-400 font-medium block">Awards Won</span>
            <span className="text-2xl font-bold text-white font-mono">
              {stats?.total_awards || 0}
            </span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center border border-emerald-500/20">
            <span className="text-xl">🥇</span>
          </div>
          <div>
            <span className="text-xs text-slate-400 font-medium block">Grand Prizes</span>
            <span className="text-2xl font-bold text-white font-mono">
              {stats?.first_place_wins || 0}
            </span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-rose-500/10 text-rose-400 flex items-center justify-center border border-rose-500/20">
            <Coffee className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-slate-400 font-medium block">Coffee Consumed</span>
            <span className="text-2xl font-bold text-white font-mono">
              {stats?.coffee_cups_consumed || 420}
            </span>
          </div>
        </div>
      </div>

      {/* Interactive Controls & Recent Inquiries */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Instant Bot Rich Presence Changer */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
              <Send className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-white text-base">Instant Bot Presence Changer</h3>
              <p className="text-xs text-slate-400">Updates live Discord status immediately without restarts</p>
            </div>
          </div>

          {presenceMsg && (
            <div className="p-3 rounded-xl text-xs bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
              {presenceMsg}
            </div>
          )}

          <form onSubmit={handleUpdatePresence} className="space-y-3">
            <div className="flex gap-2">
              <select
                value={activityType}
                onChange={(e) => setActivityType(e.target.value)}
                className="w-32 px-3 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500"
              >
                <option value="watching">Watching</option>
                <option value="playing">Playing</option>
                <option value="competing">Competing in</option>
                <option value="listening">Listening to</option>
              </select>

              <input
                type="text"
                required
                value={statusText}
                onChange={(e) => setStatusText(e.target.value)}
                className="flex-1 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500"
                placeholder="🏆 4x Hackathon Winners"
              />
            </div>

            <button
              type="submit"
              disabled={updatingPresence}
              className="w-full py-2.5 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white disabled:opacity-50 transition-colors"
            >
              {updatingPresence ? 'Updating Discord...' : 'Push Live Presence to Discord'}
            </button>
          </form>
        </div>

        {/* Recent Visitor Inquiries */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center border border-emerald-500/20">
                <MessageSquare className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-semibold text-white text-base">Recent Inquiries</h3>
                <p className="text-xs text-slate-400">Messages sent via `/contact` Discord Modal</p>
              </div>
            </div>
          </div>

          <div className="space-y-2.5">
            {recentInquiries.length === 0 ? (
              <p className="text-xs text-slate-500 text-center py-6">No visitor submissions yet.</p>
            ) : (
              recentInquiries.map((inq) => (
                <div
                  key={inq.id}
                  className="p-3.5 rounded-xl bg-slate-950 border border-slate-800/80 flex items-start justify-between gap-3 text-xs"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-white">{inq.sender_name}</span>
                      {inq.organization && (
                        <span className="text-slate-400 font-normal">({inq.organization})</span>
                      )}
                      <span
                        className={`px-1.5 py-0.5 rounded text-[10px] uppercase font-semibold ${
                          inq.status === 'unread'
                            ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                            : 'bg-slate-800 text-slate-400'
                        }`}
                      >
                        {inq.status}
                      </span>
                    </div>
                    <p className="text-slate-400 line-clamp-1">{inq.message}</p>
                  </div>
                  <span className="text-[10px] text-slate-500 shrink-0">
                    {new Date(inq.created_at).toLocaleDateString()}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OverviewPage;
