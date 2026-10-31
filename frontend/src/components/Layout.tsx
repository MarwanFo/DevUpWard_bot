import React, { useEffect, useState } from 'react';
import {
  LayoutDashboard,
  Users,
  FolderGit2,
  Trophy,
  Inbox,
  Settings,
  Bot,
  KeyRound,
  ExternalLink,
  Menu,
  X,
} from 'lucide-react';
import { BotTelemetry } from '../types';
import ApiService from '../services/api';

interface LayoutProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ currentTab, setCurrentTab, children }) => {
  const [telemetry, setTelemetry] = useState<BotTelemetry>({
    is_online: false,
    latency_ms: 0,
    guild_count: 0,
    uptime_seconds: 0,
  });
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [showKeyModal, setShowKeyModal] = useState(false);
  const [adminKey, setAdminKey] = useState(
    localStorage.getItem('devupward_admin_key') || 'dev_admin_key_12345'
  );
  const [inboxUnread, setInboxUnread] = useState(0);

  const pollStatus = async () => {
    try {
      const res = await ApiService.getBotStatus();
      setTelemetry(res.data);
    } catch {
      setTelemetry((prev) => ({ ...prev, is_online: false }));
    }

    try {
      const inboxRes = await ApiService.getInbox('unread');
      setInboxUnread(inboxRes.data.length);
    } catch {
      // ignore auth or network error
    }
  };

  useEffect(() => {
    pollStatus();
    const interval = setInterval(pollStatus, 8000);
    return () => clearInterval(interval);
  }, []);

  const saveAdminKey = (key: string) => {
    setAdminKey(key);
    localStorage.setItem('devupward_admin_key', key);
    setShowKeyModal(false);
  };

  const navItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'team', label: 'Team Roster', icon: Users },
    { id: 'projects', label: 'Project Showroom', icon: FolderGit2 },
    { id: 'awards', label: 'Hall of Fame', icon: Trophy },
    { id: 'inbox', label: 'Inquiries Inbox', icon: Inbox, badge: inboxUnread },
    { id: 'settings', label: 'Bot Settings', icon: Settings },
  ];

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Sidebar for Desktop */}
      <aside className="hidden md:flex flex-col w-64 bg-slate-900 border-r border-slate-800">
        {/* Brand header */}
        <div className="p-6 border-b border-slate-800 flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold tracking-tight text-white leading-tight">DevUpward</h1>
            <p className="text-xs text-slate-400 font-mono">Showcase Bot Hub</p>
          </div>
        </div>

        {/* Navigation links */}
        <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </div>
                {item.badge !== undefined && item.badge > 0 && (
                  <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Admin key & footer */}
        <div className="p-4 border-t border-slate-800 space-y-3">
          <button
            onClick={() => setShowKeyModal(true)}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium text-slate-400 bg-slate-800/50 hover:bg-slate-800 transition-colors border border-slate-700/50"
          >
            <div className="flex items-center gap-2">
              <KeyRound className="w-3.5 h-3.5 text-indigo-400" />
              <span>Admin API Key</span>
            </div>
            <span className="text-[10px] text-emerald-400">Set</span>
          </button>

          <div className="flex items-center justify-between text-xs text-slate-500 px-1">
            <span>v1.0.0 (Python + React)</span>
            <a
              href="https://github.com/MarwanFo/DevUpWard_bot"
              target="_blank"
              rel="noreferrer"
              className="hover:text-slate-300"
            >
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Navbar */}
        <header className="h-16 bg-slate-900/60 backdrop-blur-md border-b border-slate-800/80 px-6 flex items-center justify-between z-10">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden text-slate-400 hover:text-white"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
            <h2 className="text-base font-semibold text-white capitalize">
              {navItems.find((n) => n.id === currentTab)?.label || 'Dashboard'}
            </h2>
          </div>

          {/* Right Status Pill */}
          <div className="flex items-center gap-3">
            <div
              className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border ${
                telemetry.is_online
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                  : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
              }`}
            >
              <span
                className={`w-2 h-2 rounded-full ${
                  telemetry.is_online ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'
                }`}
              />
              <span>
                {telemetry.is_online
                  ? `Bot Online (${telemetry.latency_ms}ms • ${telemetry.guild_count} servers)`
                  : 'API Running (Bot Gateway Idle)'}
              </span>
            </div>
          </div>
        </header>

        {/* Page Content Body */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8 bg-slate-950">
          <div className="max-w-7xl mx-auto">{children}</div>
        </main>
      </div>

      {/* Admin Key Modal */}
      {showKeyModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-md w-full shadow-2xl space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
                <KeyRound className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-semibold text-white text-base">Configure Admin Key</h3>
                <p className="text-xs text-slate-400">Used to authenticate mutation actions</p>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                Admin API Key (`ADMIN_API_KEY`)
              </label>
              <input
                type="password"
                defaultValue={adminKey}
                id="keyInput"
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="dev_admin_key_12345"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => setShowKeyModal(false)}
                className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-800"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  const input = document.getElementById('keyInput') as HTMLInputElement;
                  if (input) saveAdminKey(input.value);
                }}
                className="px-4 py-2 rounded-xl text-xs font-medium bg-indigo-600 hover:bg-indigo-500 text-white"
              >
                Save Key
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Layout;

