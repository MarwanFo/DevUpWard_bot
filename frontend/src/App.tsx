import React from 'react';
import { Bot, Sparkles, Terminal } from 'lucide-react';

export const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="max-w-xl w-full bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl text-center space-y-6">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
          <Bot className="w-8 h-8" />
        </div>
        
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <Sparkles className="w-3.5 h-3.5" />
            Phase 0 Initialized
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Hackathon Showcase Bot Manager
          </h1>
          <p className="text-slate-400 text-sm">
            Unified management dashboard for team roster, showroom projects, awards, and live Discord bot settings.
          </p>
        </div>

        <div className="bg-slate-950 border border-slate-800/80 rounded-xl p-4 text-left font-mono text-xs text-slate-400 space-y-2">
          <div className="flex items-center gap-2 text-indigo-400 font-semibold">
            <Terminal className="w-4 h-4" />
            <span>System Status</span>
          </div>
          <p>• Backend: Python 3.13 (FastAPI + discord.py + SQLModel ready)</p>
          <p>• Frontend: React 19 + TypeScript + Vite + Tailwind CSS ready</p>
          <p>• Database: SQLite Async with WAL mode ready</p>
        </div>
      </div>
    </div>
  );
};

export default App;
