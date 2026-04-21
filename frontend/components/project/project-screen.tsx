"use client";

import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { AppShell, useShell } from "@/components/shell/app-shell";
import { ProjectChatPanel } from "@/components/project/project-chat-panel";
import { ProjectPreviewPanel } from "@/components/project/project-preview-panel";
import { downloadProjectCode, getProject, improveProject } from "@/lib/api";
import { getToken } from "@/lib/auth";
import type { ProjectRecord } from "@/types/designgen";

function ProjectContent({ projectId }: { projectId: string }) {
  const router = useRouter();
  const { refreshProjects } = useShell();
  const [project, setProject] = useState<ProjectRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState<"preview" | "code">("preview");
  const [activeFile, setActiveFile] = useState("index.html");
  const [improvePrompt, setImprovePrompt] = useState("");
  const [improving, setImproving] = useState(false);
  const [expandedPreview, setExpandedPreview] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }

    async function loadProject() {
      try {
        const response = await getProject(projectId);
        setProject(response);
        setActiveFile(Object.keys(response.latest_version?.files ?? {})[0] ?? "index.html");
      } catch (nextError) {
        setError(nextError instanceof Error ? nextError.message : "项目加载失败，请稍后再试。");
      } finally {
        setLoading(false);
      }
    }

    loadProject();
  }, [projectId, router]);

  useEffect(() => {
    if (!notice) {
      return;
    }

    const timer = window.setTimeout(() => setNotice(null), 2500);
    return () => window.clearTimeout(timer);
  }, [notice]);

  useEffect(() => {
    if (!project || project.status !== "generating") {
      return;
    }

    const timer = window.setInterval(async () => {
      try {
        const latest = await getProject(projectId);
        setProject(latest);
        if (latest.latest_version) {
          setActiveFile(Object.keys(latest.latest_version.files)[0] ?? "index.html");
          await refreshProjects();
        }
      } catch {
        window.clearInterval(timer);
      }
    }, 2500);

    return () => window.clearInterval(timer);
  }, [project, projectId, refreshProjects]);

  const shareUrl = typeof window !== "undefined" ? window.location.href : "";
  const hasLatestVersion = Boolean(project?.latest_version);

  async function handleImprove() {
    if (!project || !project.latest_version || !improvePrompt.trim()) {
      return;
    }

    setImproving(true);
    setError(null);

    try {
      const updatedProject = await improveProject(project.id, improvePrompt.trim());
      setProject(updatedProject);
      setActiveFile(Object.keys(updatedProject.latest_version?.files ?? {})[0] ?? "index.html");
      setImprovePrompt("");
      await refreshProjects();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "优化失败，请稍后再试。");
    } finally {
      setImproving(false);
    }
  }

  async function handleShare() {
    try {
      if (navigator.share) {
        await navigator.share({
          title: project?.title ?? "DesignGen 项目",
          text: "来看看这个 DesignGen 项目",
          url: shareUrl,
        });
      } else {
        await navigator.clipboard.writeText(shareUrl);
      }
      setNotice("项目链接已复制，可以直接分享给别人。")
    } catch {
      setError("复制项目链接失败，请手动复制当前地址。");
    }
  }

  async function handleDownload() {
    if (!project?.latest_version) {
      return;
    }

    try {
      setError(null);
      await downloadProjectCode(project.id);
      setNotice("源码压缩包已开始下载。")
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "下载失败，请稍后重试。");
    }
  }

  const statusLabel = useMemo(() => {
    if (!project) return "加载中";
    if (project.status === "generating") return "生成中";
    if (project.status === "failed") return "需要重试";
    return "已完成";
  }, [project]);

  if (loading) {
    return <div className="glass-subtle hero-rim flex h-full min-h-0 flex-1 items-center justify-center rounded-[36px] text-white/56">正在打开项目...</div>;
  }

  if (!project) {
    return <div className="glass-subtle hero-rim flex h-full min-h-0 flex-1 items-center justify-center rounded-[36px] text-rose-300">{error ?? "项目不存在。"}</div>;
  }

  return (
    <div className="flex h-full min-h-0 flex-1 flex-col gap-4 overflow-hidden">
      <header className="glass-subtle hero-rim flex items-center justify-between rounded-[32px] px-6 py-5">
        <div>
          <div className="text-[10px] uppercase tracking-[0.34em] text-white/38">项目</div>
          <div className="mt-2 text-2xl font-semibold tracking-[-0.03em] text-white md:text-3xl">{project.title}</div>
          {notice ? <div className="mt-2 text-sm text-emerald-300">{notice}</div> : null}
        </div>
        <div className="premium-pill px-4 py-2 text-sm">{statusLabel}</div>
      </header>

      <div className="flex min-h-0 flex-1 gap-4">
        {!expandedPreview ? (
          <ProjectChatPanel
            project={project}
            error={error}
            improvePrompt={improvePrompt}
            onImprovePrompt={setImprovePrompt}
            onImprove={handleImprove}
            improving={improving}
            canImprove={hasLatestVersion}
          />
        ) : null}

        <ProjectPreviewPanel
          project={project}
          activeView={activeView}
          onChangeView={setActiveView}
          onShare={handleShare}
          onDownload={handleDownload}
          expanded={expandedPreview}
          onToggleExpanded={() => setExpandedPreview((value) => !value)}
          activeFile={activeFile}
          onSelectFile={setActiveFile}
        />
      </div>
    </div>
  );
}

export function ProjectScreen({ projectId }: { projectId: string }) {
  return (
    <AppShell>
      <ProjectContent projectId={projectId} />
    </AppShell>
  );
}
