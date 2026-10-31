import React, { useEffect, useState } from 'react';
import { Edit2, Trash2, Globe, UserPlus } from 'lucide-react';
import { TeamMember } from '../types';
import ApiService from '../services/api';
import { MemberModal } from '../components/MemberModal';
import { GithubIcon, LinkedinIcon } from '../components/Icons';


export const RosterPage: React.FC = () => {
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingMember, setEditingMember] = useState<TeamMember | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const fetchMembers = async () => {
    try {
      setLoading(true);
      const res = await ApiService.getTeam();
      setMembers(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMembers();
  }, []);

  const handleSave = async (data: Partial<TeamMember>) => {
    if (editingMember?.id) {
      await ApiService.updateMember(editingMember.id, data);
    } else {
      await ApiService.createMember(data);
    }
    fetchMembers();
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to remove this squad member?')) return;
    try {
      await ApiService.deleteMember(id);
      fetchMembers();
    } catch (err) {
      alert('Failed to delete member.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">Squad Roster Management</h2>
          <p className="text-xs text-slate-400">
            Manage profiles, roles, and links that appear in Discord `/team` and `/member`
          </p>
        </div>
        <button
          onClick={() => {
            setEditingMember(null);
            setModalOpen(true);
          }}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/20 transition-all"
        >
          <UserPlus className="w-4 h-4" />
          <span>Add Squad Member</span>
        </button>
      </div>

      {loading ? (
        <div className="text-center py-16 text-slate-500 text-sm">Loading squad members...</div>
      ) : members.length === 0 ? (
        <div className="text-center py-16 bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-3">
          <p className="text-slate-400 text-sm">No squad members recorded yet.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-5">
          {members.map((member) => {
            let skills: string[] = [];
            try {
              skills = typeof member.skills === 'string' && member.skills.startsWith('[')
                ? JSON.parse(member.skills)
                : member.skills ? [member.skills] : [];
            } catch {
              skills = [];
            }

            return (
              <div
                key={member.id}
                className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between space-y-5 hover:border-slate-700 transition-colors"
              >
                <div className="flex items-start gap-4">
                  <img
                    src={
                      member.avatar_url ||
                      'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80'
                    }
                    alt={member.name}
                    className="w-16 h-16 rounded-2xl object-cover border border-slate-700 shrink-0 shadow-md"
                  />
                  <div className="space-y-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <h3 className="font-bold text-white text-base truncate">{member.name}</h3>
                      {!member.is_active && (
                        <span className="px-2 py-0.5 text-[10px] rounded-full bg-slate-800 text-slate-400 font-medium">
                          Inactive
                        </span>
                      )}
                    </div>
                    <span className="inline-block px-2.5 py-0.5 rounded-lg text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                      {member.role}
                    </span>
                    <p className="text-xs text-slate-400 line-clamp-2 pt-1">{member.bio}</p>
                  </div>
                </div>

                {skills.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {skills.map((s, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 rounded-md text-[11px] font-mono bg-slate-950 text-slate-300 border border-slate-800"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                )}

                <div className="flex items-center justify-between border-t border-slate-800/80 pt-4">
                  <div className="flex items-center gap-2 text-slate-400">
                    {member.portfolio_url && (
                      <a
                        href={member.portfolio_url}
                        target="_blank"
                        rel="noreferrer"
                        className="hover:text-white p-1 rounded hover:bg-slate-800"
                        title="Portfolio"
                      >
                        <Globe className="w-4 h-4" />
                      </a>
                    )}
                    {member.github_url && (
                      <a
                        href={member.github_url}
                        target="_blank"
                        rel="noreferrer"
                        className="hover:text-white p-1 rounded hover:bg-slate-800"
                        title="GitHub"
                      >
                        <GithubIcon className="w-4 h-4" />
                      </a>
                    )}
                    {member.linkedin_url && (
                      <a
                        href={member.linkedin_url}
                        target="_blank"
                        rel="noreferrer"
                        className="hover:text-white p-1 rounded hover:bg-slate-800"
                        title="LinkedIn"
                      >
                        <LinkedinIcon className="w-4 h-4" />
                      </a>
                    )}

                  </div>

                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => {
                        setEditingMember(member);
                        setModalOpen(true);
                      }}
                      className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                      title="Edit Member"
                    >
                      <Edit2 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => member.id && handleDelete(member.id)}
                      className="p-1.5 rounded-lg text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 transition-colors"
                      title="Delete Member"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      <MemberModal
        isOpen={modalOpen}
        member={editingMember}
        onClose={() => setModalOpen(false)}
        onSave={handleSave}
      />
    </div>
  );
};

export default RosterPage;
