export interface TeamMember {
  id?: number;
  name: string;
  role: string;
  bio: string;
  avatar_url?: string;
  discord_id?: string;
  skills: string; // JSON string or array string
  github_url?: string;
  linkedin_url?: string;
  portfolio_url?: string;
  display_order: number;
  is_active: boolean;
  created_at?: string;
}

export interface Project {
  id?: number;
  title: string;
  slug: string;
  tagline: string;
  description: string;
  category: string;
  hackathon_name: string;
  hackathon_year: number;
  awards_won?: string;
  demo_url?: string;
  repo_url?: string;
  devpost_url?: string;
  banner_url?: string;
  is_featured: boolean;
  display_order: number;
  created_at?: string;
}

export interface Award {
  id?: number;
  hackathon_name: string;
  award_title: string;
  placement: number;
  category?: string;
  prize_description?: string;
  year: number;
  project_id?: number;
  icon: string;
  created_at?: string;
}

export interface BotSetting {
  key: string;
  value: string;
  description?: string;
  updated_at?: string;
}

export interface ContactSubmission {
  id: number;
  sender_name: string;
  email?: string;
  organization?: string;
  discord_tag?: string;
  message: string;
  status: 'unread' | 'reviewed' | 'archived';
  created_at: string;
}

export interface BotTelemetry {
  is_online: boolean;
  bot_user?: string | null;
  bot_id?: string | null;
  latency_ms: number;
  guild_count: number;
  uptime_seconds: number;
}

export interface TeamStats {
  total_members: number;
  total_projects: number;
  total_awards: number;
  total_hackathons: number;
  first_place_wins: number;
  podium_finishes: number;
  coffee_cups_consumed: number;
  categories_breakdown: Record<string, number>;
}

