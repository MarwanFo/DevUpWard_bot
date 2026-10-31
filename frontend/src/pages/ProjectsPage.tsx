import React, { useEffect, useState } from 'react';
import { Plus, Edit2, Trash2, ExternalLink, Trophy, Star } from 'lucide-react';
import { Project } from '../types';
import ApiService from '../services/api';
import { ProjectModal } from '../components/ProjectModal';
import { GithubIcon } from '../components/Icons';


export const ProjectsPage: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState('All');
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const fetchProjects = async (category?: string) => {
    try {
      setLoading(true);
      const catParam = category && category !== 'All' ? category : undefined;
      const res = await ApiService.getProjects(catParam);
      setProjects(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects(activeCategory);
  }, [activeCategory]);

  const handleSave = async (data: Partial<Project>) => {
    if (editingProject?.id) {
      await ApiService.updateProject(editingProject.id, data);
    } else {
      await ApiService.createProject(data);
    }
    fetchProjects(activeCategory);
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete this project from the showroom?')) return;
    try {
      await ApiService.deleteProject(id);
      fetchProjects(activeCategory);
    } catch (err) {
      alert('Failed to delete project.');
    }
  };

  const categories = ['All', 'AI', 'Web3', 'FinTech', 'DevTools', 'Mobile'];

  return (
    <div className="space-y-6">
      {/* Header and Add button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">Project Showroom Catalog</h2>
          <p className="text-xs text-slate-400">
            Prototypes and products showcased via Discord `/projects` and `/project [name]`
          </p>
        </div>
        <button
          onClick={() => {
            setEditingProject(null);
            setModalOpen(true);
          }}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/20 transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>Add Showroom Prototype</span>
        </button>
      </div>

      {/* Category filter pills */}
      <div className="flex flex-wrap gap-2">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
              activeCategory === cat
                ? 'bg-indigo-600 text-white shadow-md'
                : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Projects Grid */}
      {loading ? (
        <div className="text-center py-16 text-slate-500 text-sm">Loading showroom projects...</div>
      ) : projects.length === 0 ? (
        <div className="text-center py-16 bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-3">
          <p className="text-slate-400 text-sm">No projects found in this category.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((proj) => (
            <div
              key={proj.id}
              className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl flex flex-col justify-between hover:border-slate-700 transition-colors group"
            >
              <div>
                {/* Banner image */}
                {proj.banner_url ? (
                  <div className="h-44 w-full relative overflow-hidden bg-slate-950">
                    <img
                      src={proj.banner_url}
                      alt={proj.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    {proj.is_featured && (
                      <span className="absolute top-3 right-3 px-2.5 py-1 rounded-full text-[10px] font-semibold bg-amber-500/90 text-slate-950 flex items-center gap-1 shadow-md">
                        <Star className="w-3 h-3 fill-slate-950" /> Featured
                      </span>
                    )}
                  </div>
                ) : (
                  <div className="h-28 bg-gradient-to-r from-indigo-950 to-slate-900 border-b border-slate-800 flex items-center justify-between p-4">
                    <span className="text-xs font-bold text-indigo-400">{proj.category}</span>
                    {proj.is_featured && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30 flex items-center gap-1">
                        <Star className="w-3 h-3 fill-amber-400" /> Featured
                      </span>
                    )}
                  </div>
                )}

                {/* Card Content */}
                <div className="p-5 space-y-3">
                  <div className="space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-mono font-semibold text-indigo-400 uppercase">
                        {proj.category} • {proj.hackathon_name} ({proj.hackathon_year})
                      </span>
                    </div>
                    <h3 className="font-bold text-white text-base leading-snug">{proj.title}</h3>
                    <p className="text-xs font-medium text-slate-300 italic">{proj.tagline}</p>
                  </div>

                  {proj.awards_won && (
                    <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      <Trophy className="w-3.5 h-3.5 shrink-0" />
                      <span className="truncate">{proj.awards_won}</span>
                    </div>
                  )}

                  <p className="text-xs text-slate-400 line-clamp-3 leading-relaxed">
                    {proj.description}
                  </p>
                </div>
              </div>

              {/* Card Footer Actions */}
              <div className="p-4 border-t border-slate-800/80 bg-slate-900/50 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {proj.demo_url && (
                    <a
                      href={proj.demo_url}
                      target="_blank"
                      rel="noreferrer"
                      className="px-2.5 py-1 rounded-lg bg-indigo-600/20 text-indigo-400 hover:bg-indigo-600 hover:text-white border border-indigo-500/30 text-xs font-semibold flex items-center gap-1 transition-colors"
                    >
                      <ExternalLink className="w-3 h-3" /> Demo
                    </a>
                  )}
                  {proj.repo_url && (
                    <a
                      href={proj.repo_url}
                      target="_blank"
                      rel="noreferrer"
                      className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                      title="GitHub Repository"
                    >
                      <GithubIcon className="w-4 h-4" />
                    </a>
                  )}

                </div>

                <div className="flex items-center gap-1">
                  <button
                    onClick={() => {
                      setEditingProject(proj);
                      setModalOpen(true);
                    }}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                    title="Edit Prototype"
                  >
                    <Edit2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => proj.id && handleDelete(proj.id)}
                    className="p-1.5 rounded-lg text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 transition-colors"
                    title="Delete Prototype"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <ProjectModal
        isOpen={modalOpen}
        project={editingProject}
        onClose={() => setModalOpen(false)}
        onSave={handleSave}
      />
    </div>
  );
};

export default ProjectsPage;
