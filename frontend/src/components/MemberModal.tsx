import React, { useState } from 'react';
import { X, User } from 'lucide-react';
import { TeamMember } from '../types';


interface MemberModalProps {
  member?: TeamMember | null;
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: Partial<TeamMember>) => Promise<void>;
}

export const MemberModal: React.FC<MemberModalProps> = ({
  member,
  isOpen,
  onClose,
  onSave,
}) => {
  if (!isOpen) return null;

  const [formData, setFormData] = useState<Partial<TeamMember>>({
    name: member?.name || '',
    role: member?.role || '',
    bio: member?.bio || '',
    avatar_url: member?.avatar_url || '',
    discord_id: member?.discord_id || '',
    skills: member?.skills ? (typeof member.skills === 'string' && member.skills.startsWith('[') ? JSON.parse(member.skills).join(', ') : member.skills) : '',
    github_url: member?.github_url || '',
    linkedin_url: member?.linkedin_url || '',
    portfolio_url: member?.portfolio_url || '',
    display_order: member?.display_order || 0,
    is_active: member ? member.is_active : true,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Parse skills into JSON array string
      const rawSkills = formData.skills || '';
      const skillsArray = typeof rawSkills === 'string' 
        ? rawSkills.split(',').map((s) => s.trim()).filter(Boolean)
        : [];

      await onSave({
        ...formData,
        skills: JSON.stringify(skillsArray),
      });
      onClose();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to save team member.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-5 my-8">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
              <User className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-white text-base">
                {member ? 'Edit Squad Member' : 'Add New Squad Member'}
              </h3>
              <p className="text-xs text-slate-400">Syncs immediately with Discord `/team` and `/member`</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Full Name *</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="Marwan"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Primary Role / Title *</label>
              <input
                type="text"
                required
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="Lead AI Architect"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Short Bio *</label>
            <textarea
              rows={3}
              required
              value={formData.bio}
              onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              placeholder="Specialized in autonomous multi-agent pipelines and scalable cloud infrastructure."
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Skills (comma-separated)</label>
            <input
              type="text"
              value={formData.skills}
              onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              placeholder="Python, FastAPI, Gemini API, Docker, PyTorch"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Avatar Image URL</label>
              <input
                type="url"
                value={formData.avatar_url || ''}
                onChange={(e) => setFormData({ ...formData, avatar_url: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="https://images.unsplash.com/..."
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Discord User ID (Optional)</label>
              <input
                type="text"
                value={formData.discord_id || ''}
                onChange={(e) => setFormData({ ...formData, discord_id: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="123456789012345678"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Portfolio Link</label>
              <input
                type="url"
                value={formData.portfolio_url || ''}
                onChange={(e) => setFormData({ ...formData, portfolio_url: e.target.value })}
                className="w-full px-2.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500"
                placeholder="https://..."
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">GitHub Link</label>
              <input
                type="url"
                value={formData.github_url || ''}
                onChange={(e) => setFormData({ ...formData, github_url: e.target.value })}
                className="w-full px-2.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500"
                placeholder="https://github.com/..."
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">LinkedIn Link</label>
              <input
                type="url"
                value={formData.linkedin_url || ''}
                onChange={(e) => setFormData({ ...formData, linkedin_url: e.target.value })}
                className="w-full px-2.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500"
                placeholder="https://linkedin.com/in/..."
              />
            </div>
          </div>

          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="is_active"
                checked={formData.is_active}
                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                className="rounded border-slate-700 bg-slate-950 text-indigo-600 focus:ring-0"
              />
              <label htmlFor="is_active" className="text-xs text-slate-300">
                Active in squad roster
              </label>
            </div>

            <div className="flex gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-800"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-5 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white disabled:opacity-50"
              >
                {loading ? 'Saving...' : member ? 'Update Member' : 'Add Member'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};
