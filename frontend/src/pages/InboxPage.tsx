import React, { useEffect, useState } from 'react';
import { Mail, CheckCircle2, Archive, Trash2, ExternalLink } from 'lucide-react';
import { ContactSubmission } from '../types';
import ApiService from '../services/api';

export const InboxPage: React.FC = () => {
  const [inquiries, setInquiries] = useState<ContactSubmission[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');

  const fetchInbox = async (status?: string) => {
    try {
      setLoading(true);
      const param = status && status !== 'all' ? status : undefined;
      const res = await ApiService.getInbox(param);
      setInquiries(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInbox(filter);
  }, [filter]);

  const handleStatusChange = async (id: number, newStatus: string) => {
    try {
      await ApiService.updateInboxStatus(id, newStatus);
      fetchInbox(filter);
    } catch (err) {
      alert('Failed to update status.');
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete this message?')) return;
    try {
      await ApiService.deleteInboxItem(id);
      fetchInbox(filter);
    } catch (err) {
      alert('Failed to delete message.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">Visitor Inquiries Inbox</h2>
          <p className="text-xs text-slate-400">
            Messages and collaboration proposals submitted by guests via the Discord `/contact` Modal
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex gap-2">
          {['all', 'unread', 'reviewed', 'archived'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium capitalize transition-all ${
                filter === f
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="text-center py-16 text-slate-500 text-sm">Loading visitor inquiries...</div>
      ) : inquiries.length === 0 ? (
        <div className="text-center py-16 bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-3">
          <p className="text-slate-400 text-sm">No messages found in this folder.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {inquiries.map((inq) => (
            <div
              key={inq.id}
              className={`bg-slate-900 border rounded-2xl p-6 shadow-xl space-y-4 transition-colors ${
                inq.status === 'unread'
                  ? 'border-indigo-500/40 bg-slate-900/90'
                  : 'border-slate-800'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-center text-slate-300">
                    <Mail className="w-4 h-4 text-indigo-400" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-bold text-white text-sm">{inq.sender_name}</h3>
                      {inq.organization && (
                        <span className="text-xs text-slate-400 font-normal">
                          • {inq.organization}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-3 text-[11px] text-slate-400">
                      {inq.email && <span>📧 {inq.email}</span>}
                      {inq.discord_tag && <span>💬 {inq.discord_tag}</span>}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 self-start sm:self-center">
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider ${
                      inq.status === 'unread'
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        : inq.status === 'reviewed'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {inq.status}
                  </span>
                  <span className="text-xs text-slate-500 font-mono">
                    {new Date(inq.created_at).toLocaleString()}
                  </span>
                </div>
              </div>

              {/* Message content */}
              <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap bg-slate-950/60 p-4 rounded-xl border border-slate-800/60 font-sans">
                {inq.message}
              </p>

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-1">
                <div className="flex items-center gap-2">
                  {inq.email && (
                    <a
                      href={`mailto:${inq.email}?subject=Regarding your message to DevUpward`}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-600/20 text-indigo-400 hover:bg-indigo-600 hover:text-white border border-indigo-500/30 text-xs font-semibold transition-colors"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                      Reply via Email
                    </a>
                  )}
                </div>

                <div className="flex items-center gap-1.5">
                  {inq.status !== 'reviewed' && (
                    <button
                      onClick={() => handleStatusChange(inq.id, 'reviewed')}
                      className="inline-flex items-center gap-1 px-3 py-1.5 rounded-xl text-xs font-medium text-emerald-400 hover:bg-emerald-500/10 border border-emerald-500/20 transition-colors"
                      title="Mark Reviewed"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Reviewed</span>
                    </button>
                  )}

                  {inq.status !== 'archived' && (
                    <button
                      onClick={() => handleStatusChange(inq.id, 'archived')}
                      className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                      title="Archive"
                    >
                      <Archive className="w-4 h-4" />
                    </button>
                  )}

                  <button
                    onClick={() => handleDelete(inq.id)}
                    className="p-1.5 rounded-lg text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 transition-colors"
                    title="Delete Message"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default InboxPage;

