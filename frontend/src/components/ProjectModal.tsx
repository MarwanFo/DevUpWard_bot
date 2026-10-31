import React, { useState } from 'react';
import { X, FolderGit2 } from 'lucide-react';
import { Project } from '../types';

interface ProjectModalProps {
  project?: Project | null;
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: Partial<Project>) => Promise<void>;
}

export const ProjectModal: React.FC<ProjectModalProps> = ({
  project,
  isOpen,
  onClose,
  onSave,
}) => {
  if (!isOpen) return null;

  const [formData, setFormData] = useState<Partial<Project>>({
    title: project?.title || '',
    slug: project?.slug || '',
    tagline: project?.tagline || '',
    description: project?.description || '',
    category: project?.category || 'AI',
    hackathon_name: project?.hackathon_name || '',
    hackathon_year: project?.hackathon_year || 2026,
    awards_won: project?.awards_won || '',
    demo_url: project?.demo_url || '',
    repo_url: project?.repo_url || '',
    devpost_url: project?.devpost_url || '',
    banner_url: project?.banner_url || '',
    is_featured: project ? project.is_featured : false,
    display_order: project?.display_order || 0,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const generateSlug = (title: string) => {
    return title
      .toLowerCase()
      .trim()
      .replace(/[^\w\s-]/g, '')
      .replace(/[\s_-]+/g, '-')
      .replace(/^-+|-+$/g, '');
  };

  const handleTitleChange = (val: string) => {
    setFormData((prev) => ({
      ...prev,
      title: val,
      slug: !project ? generateSlug(val) : prev.slug,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await onSave(formData);
      onClose();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to save project.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-5 my-8">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
              <FolderGit2 className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-white text-base">
                {project ? 'Edit Prototype' : 'Add Showroom Prototype'}
              </h3>
              <p className="text-xs text-slate-400">Syncs live with Discord `/projects` and `/project`</p>
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
              <label className="block text-xs font-medium text-slate-300 mb-1">Project Title *</label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => handleTitleChange(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="OmniAgent Flow"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">URL Identifier (Slug) *</label>
              <input
                type="text"
                required
                value={formData.slug}
                onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="omniagent-flow"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Tagline (One-line pitch) *</label>
            <input
              type="text"
              required
              value={formData.tagline}
              onChange={(e) => setFormData({ ...formData, tagline: e.target.value })}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              placeholder="Autonomous multi-modal agent workspace for real-time code generation."
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Category *</label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              >
                <option value="AI">AI / Agents</option>
                <option value="Web3">Web3 / Crypto</option>
                <option value="FinTech">FinTech</option>
                <option value="DevTools">Developer Tools</option>
                <option value="Mobile">Mobile App</option>
                <option value="Full-Stack">Full-Stack</option>
              </select>
            </div>
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
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Year</label>
              <input
                type="number"
                value={formData.hackathon_year}
                onChange={(e) => setFormData({ ...formData, hackathon_year: parseInt(e.target.value) || 2026 })}
                className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Awards & Recognition</label>
            <input
              type="text"
              value={formData.awards_won || ''}
              onChange={(e) => setFormData({ ...formData, awards_won: e.target.value })}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              placeholder="🥇 1st Place Overall & Best AI Agent"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Full Description (Problem & Solution) *</label>
            <textarea
              rows={4}
              required
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              placeholder="Explain the problem solved, tech architecture, and key innovations during the hackathon..."
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Live Demo URL</label>
              <input
                type="url"
                value={formData.demo_url || ''}
                onChange={(e) => setFormData({ ...formData, demo_url: e.target.value })}
                className="w-full px-2.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500"
                placeholder="https://demo.app"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">GitHub Repo URL</label>
              <input
                type="url"
                value={formData.repo_url || ''}
                onChange={(e) => setFormData({ ...formData, repo_url: e.target.value })}
                className="w-full px-2.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500"
                placeholder="https://github.com/..."
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Devpost URL</label>
              <input
                type="url"
                value={formData.devpost_url || ''}
                onChange={(e) => setFormData({ ...formData, devpost_url: e.target.value })}
                className="w-full px-2.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500"
                placeholder="https://devpost.com/..."
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Banner Image / Screenshot URL</label>
            <input
              type="url"
              value={formData.banner_url || ''}
              onChange={(e) => setFormData({ ...formData, banner_url: e.target.value })}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-indigo-500"
              placeholder="https://images.unsplash.com/..."
            />
          </div>

          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="is_featured"
                checked={formData.is_featured}
                onChange={(e) => setFormData({ ...formData, is_featured: e.target.checked })}
                className="rounded border-slate-700 bg-slate-950 text-indigo-600 focus:ring-0"
              />
              <label htmlFor="is_featured" className="text-xs text-slate-300 font-medium">
                ⭐ Mark as Featured Project
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
                {loading ? 'Saving...' : project ? 'Update Project' : 'Add Project'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};
