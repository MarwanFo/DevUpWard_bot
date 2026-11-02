import axios from 'axios';
import {
  Award,
  BotSetting,
  BotTelemetry,
  ContactSubmission,
  Project,
  TeamMember,
  TeamStats,
} from '../types';

const getBaseUrl = () => {
  const saved = typeof window !== 'undefined' ? localStorage.getItem('devupward_api_url') : null;
  return saved || import.meta.env.VITE_API_URL || '';
};

const api = axios.create({
  baseURL: `${getBaseUrl()}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to attach admin key and dynamic target server URL
api.interceptors.request.use((config) => {
  const customUrl = localStorage.getItem('devupward_api_url');
  if (customUrl) {
    config.baseURL = `${customUrl.replace(/\/+$/, '')}/api/v1`;
  }
  const adminKey = localStorage.getItem('devupward_admin_key') || 'dev_admin_key_12345';
  config.headers['X-Admin-Key'] = adminKey;
  return config;
});

export const ApiService = {
  // Telemetry & Stats
  getHealth: () => {
    const base = typeof window !== 'undefined' ? localStorage.getItem('devupward_api_url') : '';
    const cleanBase = base ? base.replace(/\/+$/, '') : '';
    return axios.get(`${cleanBase}/health`);
  },
  getBotStatus: () => api.get<BotTelemetry>('/bot/status'),
  updatePresence: (status_text: string, activity_type: string = 'watching') =>
    api.post('/bot/presence', { status_text, activity_type }),
  syncCommands: (guild_id?: number) => api.post('/bot/sync', { guild_id }),
  getStats: () => api.get<TeamStats>('/stats'),

  // Team
  getTeam: () => api.get<TeamMember[]>('/team'),
  getMember: (id: number) => api.get<TeamMember>(`/team/${id}`),
  createMember: (member: Partial<TeamMember>) => api.post<TeamMember>('/team', member),
  updateMember: (id: number, member: Partial<TeamMember>) => api.put<TeamMember>(`/team/${id}`, member),
  deleteMember: (id: number) => api.delete(`/team/${id}`),

  // Projects
  getProjects: (category?: string) =>
    api.get<Project[]>('/projects', { params: { category } }),
  getProject: (identifier: string | number) => api.get<Project>(`/projects/${identifier}`),
  createProject: (project: Partial<Project>) => api.post<Project>('/projects', project),
  updateProject: (id: number, project: Partial<Project>) => api.put<Project>(`/projects/${id}`, project),
  deleteProject: (id: number) => api.delete(`/projects/${id}`),

  // Awards
  getAwards: () => api.get<Award[]>('/awards'),
  createAward: (award: Partial<Award>) => api.post<Award>('/awards', award),
  updateAward: (id: number, award: Partial<Award>) => api.put<Award>(`/awards/${id}`, award),
  deleteAward: (id: number) => api.delete(`/awards/${id}`),

  // Settings
  getSettings: () => api.get<BotSetting[]>('/settings'),
  getSettingsDict: () => api.get<Record<string, string>>('/settings/dict'),
  updateSetting: (key: string, value: string, description?: string) =>
    api.put<BotSetting>(`/settings/${key}`, { value, description }),

  // Inbox
  getInbox: (status?: string) => api.get<ContactSubmission[]>('/inbox', { params: { status } }),
  updateInboxStatus: (id: number, status: string) =>
    api.patch<ContactSubmission>(`/inbox/${id}/status`, { status }),
  deleteInboxItem: (id: number) => api.delete(`/inbox/${id}`),

  // Media / Cloudinary Uploads
  uploadImage: (file: File, folder: string = 'showcase') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('folder', folder);
    return api.post<{ success: boolean; url: string; public_id: string }>(
      '/upload/image',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
  },
};


export default ApiService;

