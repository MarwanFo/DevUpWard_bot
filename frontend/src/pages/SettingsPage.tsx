import React, { useEffect, useState } from 'react';
import { Save, RefreshCw } from 'lucide-react';
import ApiService from '../services/api';


export const SettingsPage: React.FC = () => {
  const [settingsDict, setSettingsDict] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState('');
  const [syncing, setSyncing] = useState(false);
  const [syncMsg, setSyncMsg] = useState('');

  const [adminKey, setAdminKey] = useState(
    localStorage.getItem('devupward_admin_key') || 'dev_admin_key_12345'
  );

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const res = await ApiService.getSettingsDict();
      setSettingsDict(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  const handleChange = (key: string, value: string) => {
    setSettingsDict((prev) => ({ ...prev, [key]: value }));
  };

  const handleSaveAll = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSaving(true);
      setSaveMsg('');

      // Update all settings in parallel
      const promises = Object.entries(settingsDict).map(([key, val]) =>
        ApiService.updateSetting(key, val)
      );
      await Promise.all(promises);

      // Save admin key to local storage
      localStorage.setItem('devupward_admin_key', adminKey);

      setSaveMsg('✅ All settings saved successfully! Bot and web configs updated.');
    } catch (err: any) {
      setSaveMsg('❌ Error saving settings: ' + (err?.response?.data?.detail || err.message));
    } finally {
      setSaving(false);
    }
  };

  const handleForceSync = async () => {
    try {
      setSyncing(true);
      setSyncMsg('');
      const res = await ApiService.syncCommands();
      setSyncMsg(`✅ Synced ${res.data.synced_count} slash commands with Discord!`);
    } catch (err: any) {
      setSyncMsg('❌ Sync failed: ' + (err?.response?.data?.detail || 'Is the bot connected?'));
    } finally {
      setSyncing(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="border-b border-slate-800 pb-5">
        <h2 className="text-xl font-bold tracking-tight text-white">Bot & Team Configuration</h2>
        <p className="text-xs text-slate-400">
          Configure branding, Discord channel IDs, and trigger slash command synchronization
        </p>
      </div>

      {saveMsg && (
        <div
          className={`p-3.5 rounded-xl text-xs border ${
            saveMsg.startsWith('✅')
              ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
              : 'bg-rose-500/10 border-rose-500/20 text-rose-400'
          }`}
        >
          {saveMsg}
        </div>
      )}

      {loading ? (
        <div className="text-center py-16 text-slate-500 text-sm">Loading configurations...</div>
      ) : (
        <form onSubmit={handleSaveAll} className="space-y-8">
          {/* Section 1: Team Identity */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <h3 className="font-semibold text-white text-sm border-b border-slate-800 pb-2">
              🎨 Team Identity & Brand Theme
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Official Team Name</label>
                <input
                  type="text"
                  value={settingsDict.team_name || ''}
                  onChange={(e) => handleChange('team_name', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                  placeholder="DevUpward"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Brand Hex Color</label>
                <div className="flex gap-2">
                  <input
                    type="color"
                    value={settingsDict.brand_color || '#5865F2'}
                    onChange={(e) => handleChange('brand_color', e.target.value)}
                    className="h-10 w-12 rounded-xl bg-slate-950 border border-slate-800 p-1 cursor-pointer"
                  />
                  <input
                    type="text"
                    value={settingsDict.brand_color || '#5865F2'}
                    onChange={(e) => handleChange('brand_color', e.target.value)}
                    className="flex-1 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white font-mono focus:outline-none focus:border-indigo-500"
                    placeholder="#5865F2"
                  />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Team Slogan / Motto</label>
              <input
                type="text"
                value={settingsDict.team_motto || ''}
                onChange={(e) => handleChange('team_motto', e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="Building the future, one hackathon at a time"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">About Bio (Shown in `/about`)</label>
              <textarea
                rows={3}
                value={settingsDict.team_about || ''}
                onChange={(e) => handleChange('team_about', e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          {/* Section 2: Discord Channel IDs */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <h3 className="font-semibold text-white text-sm border-b border-slate-800 pb-2">
              📡 Discord Channel Routing
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Welcome Channel Snowflake ID
                </label>
                <input
                  type="text"
                  value={settingsDict.welcome_channel_id || ''}
                  onChange={(e) => handleChange('welcome_channel_id', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white font-mono focus:outline-none focus:border-indigo-500"
                  placeholder="e.g. 123456789012345678"
                />
                <span className="text-[11px] text-slate-500 mt-1 block">
                  Channel where the bot welcomes new server members.
                </span>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Team Inbox Channel Snowflake ID
                </label>
                <input
                  type="text"
                  value={settingsDict.inbox_channel_id || ''}
                  onChange={(e) => handleChange('inbox_channel_id', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white font-mono focus:outline-none focus:border-indigo-500"
                  placeholder="e.g. 123456789012345678"
                />
                <span className="text-[11px] text-slate-500 mt-1 block">
                  Private channel receiving `/contact` modal notifications.
                </span>
              </div>
            </div>
          </div>

          {/* Section 3: Official Social Links */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <h3 className="font-semibold text-white text-sm border-b border-slate-800 pb-2">
              🌐 Official Links Hub (Shown in `/socials`)
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Website URL</label>
                <input
                  type="url"
                  value={settingsDict.website_url || ''}
                  onChange={(e) => handleChange('website_url', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">GitHub Organization</label>
                <input
                  type="url"
                  value={settingsDict.github_org_url || ''}
                  onChange={(e) => handleChange('github_org_url', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">LinkedIn Page</label>
                <input
                  type="url"
                  value={settingsDict.linkedin_org_url || ''}
                  onChange={(e) => handleChange('linkedin_org_url', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Devpost Team Profile</label>
                <input
                  type="url"
                  value={settingsDict.devpost_url || ''}
                  onChange={(e) => handleChange('devpost_url', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>
          </div>

          {/* Section 4: Cloudinary Media Storage */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <h3 className="font-semibold text-white text-sm">
                ☁️ Cloudinary Media Storage (Direct Photo Uploads)
              </h3>
              <a
                href="https://cloudinary.com"
                target="_blank"
                rel="noreferrer"
                className="text-xs text-indigo-400 hover:text-indigo-300"
              >
                Get Free Cloudinary Keys &rarr;
              </a>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Cloud Name</label>
                <input
                  type="text"
                  value={settingsDict.cloudinary_cloud_name || ''}
                  onChange={(e) => handleChange('cloudinary_cloud_name', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white font-mono focus:outline-none focus:border-indigo-500"
                  placeholder="e.g. devupward"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">API Key</label>
                <input
                  type="text"
                  value={settingsDict.cloudinary_api_key || ''}
                  onChange={(e) => handleChange('cloudinary_api_key', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white font-mono focus:outline-none focus:border-indigo-500"
                  placeholder="e.g. 123456789012345"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">API Secret</label>
                <input
                  type="password"
                  value={settingsDict.cloudinary_api_secret || ''}
                  onChange={(e) => handleChange('cloudinary_api_secret', e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white font-mono focus:outline-none focus:border-indigo-500"
                  placeholder="••••••••••••••••••••••••"
                />
              </div>
            </div>
          </div>

          {/* Section 5: Security & Command Sync */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">

            <h3 className="font-semibold text-white text-sm border-b border-slate-800 pb-2">
              🔐 Admin Security & Discord Synchronization
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 items-start">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Admin API Key</label>
                <input
                  type="password"
                  value={adminKey}
                  onChange={(e) => setAdminKey(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                />
                <span className="text-[11px] text-slate-500 mt-1 block">
                  Must match `ADMIN_API_KEY` defined in `.env`.
                </span>
              </div>

              <div className="space-y-2">
                <label className="block text-xs font-medium text-slate-300">Force Slash Command Sync</label>
                <button
                  type="button"
                  onClick={handleForceSync}
                  disabled={syncing}
                  className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold border border-slate-700 transition-colors disabled:opacity-50"
                >
                  <RefreshCw className={`w-4 h-4 ${syncing ? 'animate-spin' : ''}`} />
                  <span>{syncing ? 'Syncing...' : 'Sync Slash Commands to Discord'}</span>
                </button>
                {syncMsg && (
                  <p className="text-[11px] text-indigo-400 font-mono mt-1">{syncMsg}</p>
                )}
              </div>
            </div>
          </div>

          {/* Submit button */}
          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={saving}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-xl shadow-indigo-600/20 disabled:opacity-50 transition-all"
            >
              <Save className="w-4 h-4" />
              <span>{saving ? 'Saving...' : 'Save All Configurations'}</span>
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default SettingsPage;
