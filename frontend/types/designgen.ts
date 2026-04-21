export interface AuthUser {
  id: string;
  name: string;
  email: string;
  avatar_url?: string | null;
  created_at: string;
}

export interface AuthResponse {
  user: AuthUser;
  access_token: string;
  token_type: string;
}

export interface ProjectSummary {
  id: string;
  title: string;
  status: string;
  initial_prompt: string;
  updated_at: string;
}

export interface ProjectVersion {
  id: string;
  version_no: number;
  prompt: string;
  files: Record<string, string>;
  preview_html: string;
  created_at: string;
}

export interface ProjectRecord {
  id: string;
  title: string;
  status: string;
  initial_prompt: string;
  created_at: string;
  updated_at: string;
  logs: string[];
  latest_version?: ProjectVersion | null;
  download_url?: string | null;
}
