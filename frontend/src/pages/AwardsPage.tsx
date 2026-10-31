import React, { useEffect, useState } from 'react';
import { Plus, Edit2, Trash2 } from 'lucide-react';
import { Award, Project } from '../types';

import ApiService from '../services/api';
import { AwardModal } from '../components/AwardModal';

export const AwardsPage: React.FC = () => {
  const [awards, setAwards] = useState<Award[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingAward, setEditingAward] = useState<Award | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const fetchAwards = async () => {
    try {
      setLoading(true);
      const [awardsRes, projectsRes] = await Promise.all([
        ApiService.getAwards(),
        ApiService.getProjects(),
      ]);
      setAwards(awardsRes.data);
      setProjects(projectsRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAwards();
  }, []);

  const handleSave = async (data: Partial<Award>) => {
    if (editingAward?.id) {
      await ApiService.updateAward(editingAward.id, data);
    } else {
      await ApiService.createAward(data);
    }
    fetchAwards();
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete this award from the Hall of Fame?')) return;
    try {
      await ApiService.deleteAward(id);
      fetchAwards();
    } catch (err) {
      alert('Failed to delete award.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">Hackathon Hall of Fame (Palmarès)</h2>
          <p className="text-xs text-slate-400">
            Chronological record of competition victories displayed in Discord `/awards` and `/stats`
          </p>
        </div>
        <button
          onClick={() => {
            setEditingAward(null);
            setModalOpen(true);
          }}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold shadow-lg shadow-amber-600/20 transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>Record New Award</span>
        </button>
      </div>

      {loading ? (
        <div className="text-center py-16 text-slate-500 text-sm">Loading Hall of Fame records...</div>
      ) : awards.length === 0 ? (
        <div className="text-center py-16 bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-3">
          <p className="text-slate-400 text-sm">No awards recorded yet.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {awards.map((award) => {
            const linkedProj = projects.find((p) => p.id === award.project_id);

            return (
              <div
                key={award.id}
                className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:border-slate-700 transition-colors"
              >
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-slate-950 border border-slate-800 flex items-center justify-center text-2xl shrink-0 shadow-inner">
                    {award.icon || '🏆'}
                  </div>

                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="font-bold text-white text-base">{award.award_title}</h3>
                      {award.category && (
                        <span className="px-2 py-0.5 rounded-md text-[11px] font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                          {award.category}
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-3 text-xs text-slate-400">
                      <span className="font-medium text-slate-200">
                        🏛️ {award.hackathon_name} ({award.year})
                      </span>
                      {award.prize_description && (
                        <>
                          <span>•</span>
                          <span className="text-emerald-400 font-mono">
                            💰 {award.prize_description}
                          </span>
                        </>
                      )}
                    </div>

                    {linkedProj && (
                      <div className="text-xs text-slate-500 flex items-center gap-1 pt-1">
                        <span>Associated Project:</span>
                        <span className="text-indigo-400 font-medium">"{linkedProj.title}"</span>
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-1.5 self-end sm:self-center border-t sm:border-t-0 border-slate-800 pt-3 sm:pt-0">
                  <button
                    onClick={() => {
                      setEditingAward(award);
                      setModalOpen(true);
                    }}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                    title="Edit Award"
                  >
                    <Edit2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => award.id && handleDelete(award.id)}
                    className="p-1.5 rounded-lg text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 transition-colors"
                    title="Delete Award"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      <AwardModal
        isOpen={modalOpen}
        award={editingAward}
        projects={projects}
        onClose={() => setModalOpen(false)}
        onSave={handleSave}
      />
    </div>
  );
};

export default AwardsPage;
