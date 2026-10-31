import React, { useState } from 'react';
import { X, Trophy } from 'lucide-react';
import { Award, Project } from '../types';

interface AwardModalProps {
  award?: Award | null;
  projects: Project[];
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: Partial<Award>) => Promise<void>;
}

export const AwardModal: React.FC<AwardModalProps> = ({
  award,
  projects,
  isOpen,
  onClose,
  onSave,
}) => {
  if (!isOpen) return null;

  const [formData, setFormData] = useState<Partial<Award>>({
    hackathon_name: award?.hackathon_name || '',
    award_title: award?.award_title || '',
    placement: award ? award.placement : 1,
    category: award?.category || '',
    prize_description: award?.prize_description || '',
    year: award?.year || 2026,
    icon: award?.icon || '🏆',
    project_id: award?.project_id || undefined,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await onSave({
        ...formData,
        project_id: formData.project_id ? Number(formData.project_id) : undefined,
      });
      onClose();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to save award.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-5 my-8">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center border border-amber-500/20">
              <Trophy className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-white text-base">
                {award ? 'Edit Award' : 'Record New Award'}
              </h3>
              <p className="text-xs text-slate-400">Updates the `/awards` and `/stats` trophy room in Discord</p>
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
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Hackathon Name *</label>
            <input
              type="text"
              required
              value={formData.hackathon_name}
              onChange={(e) => setFormData({ ...formData, hackathon_name: e.target.value })}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              placeholder="HackGlobal 2026"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Award Title *</label>
              <input
                type="text"
                required
                value={formData.award_title}
                onChange={(e) => setFormData({ ...formData, award_title: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="1st Place Grand Winner"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Category / Track</label>
              <input
                type="text"
                value={formData.category || ''}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="Overall, AI Track, FinTech"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Placement *</label>
              <select
                value={formData.placement}
                onChange={(e) => {
                  const p = parseInt(e.target.value);
                  const iconMap: Record<number, string> = { 1: '🥇', 2: '🥈', 3: '🥉', 0: '🌟' };
                  setFormData({ ...formData, placement: p, icon: iconMap[p] || '🏆' });
                }}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              >
                <option value={1}>1st Place (Grand Prize)</option>
                <option value={2}>2nd Place</option>
                <option value={3}>3rd Place</option>
                <option value={0}>Special / Track Prize</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Icon Badge</label>
              <input
                type="text"
                value={formData.icon}
                onChange={(e) => setFormData({ ...formData, icon: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white text-center focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Year</label>
              <input
                type="number"
                value={formData.year}
                onChange={(e) => setFormData({ ...formData, year: parseInt(e.target.value) || 2026 })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Prize / Grant Details</label>
            <input
              type="text"
              value={formData.prize_description || ''}
              onChange={(e) => setFormData({ ...formData, prize_description: e.target.value })}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              placeholder="$15,000 + Cloud Credits"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Linked Showcase Project</label>
            <select
              value={formData.project_id || ''}
              onChange={(e) => setFormData({ ...formData, project_id: e.target.value ? Number(e.target.value) : undefined })}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
            >
              <option value="">-- No linked project --</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.title} ({p.hackathon_name})
                </option>
              ))}
            </select>
          </div>

          <div className="flex justify-end gap-2 pt-2">
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
              {loading ? 'Saving...' : award ? 'Update Award' : 'Save Award'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
