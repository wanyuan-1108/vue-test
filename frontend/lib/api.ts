import { clearSession, getToken } from "@/lib/auth";
import type { AuthResponse, AuthUser, ProjectRecord, ProjectSummary } from "@/types/designgen";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

type ApiErrorPayload = {
  detail?: string | Array<{ loc?: Array<string | number>; msg?: string }>;
};

function normalizeErrorMessage(payload: ApiErrorPayload, fallback: string): string {
  if (typeof payload.detail === "string" && payload.detail.trim()) {
    return payload.detail;
  }

  if (Array.isArray(payload.detail) && payload.detail.length > 0) {
    return payload.detail
      .map((item) => {
        const label = item.loc?.length ? String(item.loc[item.loc.length - 1]) : "字段";
        const message = item.msg?.trim() || "输入不正确";
        return `${label}: ${message}`;
      })
      .join("；");
  }

  return fallback;
}

async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers = new Headers(options.headers ?? {});

  if (!headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  let response: Response;

  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers,
    });
  } catch {
    throw new ApiError("无法连接到服务器，请确认后端已经启动。", 0);
  }

  if (!response.ok) {
    let message = "请求失败，请稍后重试。";

    try {
      const errorPayload = (await response.json()) as ApiErrorPayload;
      message = normalizeErrorMessage(errorPayload, message);
    } catch {
      message = response.statusText || message;
    }

    if (response.status === 401) {
      clearSession();
    }

    throw new ApiError(message, response.status);
  }

  return (await response.json()) as T;
}

export async function registerUser(payload: { name: string; email: string; password: string }) {
  return apiFetch<AuthResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function loginUser(payload: { email: string; password: string }) {
  return apiFetch<AuthResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function fetchMe() {
  return apiFetch<AuthUser>("/auth/me");
}

export async function listProjects() {
  return apiFetch<ProjectSummary[]>("/projects");
}

export async function createProject(prompt: string) {
  return apiFetch<ProjectRecord>("/projects", {
    method: "POST",
    body: JSON.stringify({ prompt }),
  });
}

export async function getProject(projectId: string) {
  return apiFetch<ProjectRecord>(`/projects/${projectId}`);
}

export async function improveProject(projectId: string, prompt: string) {
  return apiFetch<ProjectRecord>(`/projects/${projectId}/improve`, {
    method: "POST",
    body: JSON.stringify({ prompt }),
  });
}

export function getDownloadUrl(projectId: string) {
  return `${API_BASE}/projects/${projectId}/download`;
}

export async function downloadProjectCode(projectId: string) {
  const token = getToken();
  const headers = new Headers();

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  let response: Response;

  try {
    response = await fetch(getDownloadUrl(projectId), {
      method: "GET",
      headers,
    });
  } catch {
    throw new ApiError("无法连接到服务器，请确认后端已经启动。", 0);
  }

  if (!response.ok) {
    let message = "下载失败，请稍后重试。";

    try {
      const errorPayload = (await response.json()) as ApiErrorPayload;
      message = normalizeErrorMessage(errorPayload, message);
    } catch {
      message = response.statusText || message;
    }

    if (response.status === 401) {
      clearSession();
    }

    throw new ApiError(message, response.status);
  }

  const blob = await response.blob();
  const fileName = response.headers.get("content-disposition")?.match(/filename=\"?([^\";]+)\"?/)?.[1] ?? `designgen-${projectId}.zip`;
  const objectUrl = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = objectUrl;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(objectUrl);
}

export { ApiError };
