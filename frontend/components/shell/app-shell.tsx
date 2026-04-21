"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { fetchMe, listProjects } from "@/lib/api";
import { clearSession, getStoredUser, getToken, saveSession } from "@/lib/auth";
import type { AuthUser, ProjectSummary } from "@/types/designgen";

import { Sidebar } from "@/components/shell/sidebar";

type ShellContextValue = {
  user: AuthUser | null;
  projects: ProjectSummary[];
  loading: boolean;
  isAuthenticated: boolean;
  refreshProjects: () => Promise<void>;
  signOut: () => void;
};

const ShellContext = createContext<ShellContextValue | null>(null);

export function AppShell({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [loading, setLoading] = useState(true);

  const refreshProjects = useCallback(async () => {
    if (!getToken()) {
      setProjects([]);
      return;
    }

    try {
      const projectList = await listProjects();
      setProjects(projectList);
    } catch {
      setProjects([]);
    }
  }, []);

  useEffect(() => {
    const cachedUser = getStoredUser();
    if (cachedUser) {
      setUser(cachedUser);
    }

    async function bootstrap() {
      if (!getToken()) {
        setLoading(false);
        return;
      }

      try {
        const [currentUser, projectList] = await Promise.all([fetchMe(), listProjects()]);
        saveSession(getToken() ?? "", currentUser);
        setUser(currentUser);
        setProjects(projectList);
      } catch {
        clearSession();
        setUser(null);
        setProjects([]);
      } finally {
        setLoading(false);
      }
    }

    bootstrap();
  }, []);

  function signOut() {
    clearSession();
    setUser(null);
    setProjects([]);
  }

  const value = useMemo<ShellContextValue>(
    () => ({
      user,
      projects,
      loading,
      isAuthenticated: Boolean(user && getToken()),
      refreshProjects,
      signOut,
    }),
    [loading, projects, refreshProjects, user]
  );

  return (
    <ShellContext.Provider value={value}>
      <div className="relative min-h-screen overflow-hidden px-4 py-4 text-white md:px-5 md:py-5">
        <div className="app-gradient-bg absolute inset-0" />
        <div className="app-grid-overlay absolute inset-0 opacity-30" />
        <div className="pointer-events-none absolute left-[12%] top-[10%] h-64 w-64 rounded-full bg-[radial-gradient(circle,rgba(118,124,255,0.22),transparent_68%)] blur-3xl" />
        <div className="pointer-events-none absolute bottom-[8%] right-[8%] h-72 w-72 rounded-full bg-[radial-gradient(circle,rgba(84,198,255,0.16),transparent_70%)] blur-3xl" />
        <div className="pointer-events-none absolute inset-x-0 top-0 h-56 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_70%)]" />

        <div className="relative z-10 flex min-h-[calc(100vh-2rem)] gap-4 xl:gap-5">
          <Sidebar />
          <main className="flex min-w-0 flex-1 flex-col">{children}</main>
        </div>
      </div>
    </ShellContext.Provider>
  );
}

export function useShell() {
  const context = useContext(ShellContext);
  if (!context) {
    throw new Error("useShell must be used within AppShell");
  }
  return context;
}
