"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { Layers3, Sparkles } from "lucide-react";

import { TemplatePreferenceEditor } from "@/components/projects/template-preference-editor";
import { TemplatePromptCard } from "@/components/projects/template-prompt-card";
import { AppShell, useShell } from "@/components/shell/app-shell";
import { createProject } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { TEMPLATE_LIBRARY, getRecommendedTemplates, type TemplateIdea } from "@/lib/template-library";
import {
  createEmptyTemplatePreferences,
  getUserTemplatePreferences,
  hasCompleteTemplatePreferences,
  saveUserTemplatePreferences,
  type UserTemplatePreferences,
} from "@/lib/template-preferences";

function ProjectsContent() {
  const router = useRouter();
  const { projects, user, isAuthenticated, refreshProjects } = useShell();
  const [templatePreferences, setTemplatePreferences] = useState<UserTemplatePreferences>(createEmptyTemplatePreferences());
  const [activeTemplateId, setActiveTemplateId] = useState<string | null>(null);
  const [templateError, setTemplateError] = useState<string | null>(null);

  const statusLabels: Record<string, string> = {
    generating: "生成中",
    ready: "已完成",
    failed: "生成失败",
  };

  useEffect(() => {
    setTemplatePreferences(getUserTemplatePreferences(user?.id));
  }, [user?.id]);

  const recommendedTemplates = useMemo(() => getRecommendedTemplates(templatePreferences, TEMPLATE_LIBRARY, 4), [templatePreferences]);
  const completeTemplatePreferences = hasCompleteTemplatePreferences(templatePreferences);

  function handleTemplatePreferencesChange(nextPreferences: UserTemplatePreferences) {
    setTemplatePreferences(nextPreferences);

    if (user?.id) {
      saveUserTemplatePreferences(user.id, nextPreferences);
    }
  }

  async function handleUseTemplate(template: TemplateIdea) {
    if (!getToken() || !isAuthenticated) {
      router.push("/login");
      return;
    }

    setActiveTemplateId(template.id);
    setTemplateError(null);

    try {
      const project = await createProject(template.prompt);
      await refreshProjects();
      router.push(`/project/${project.id}`);
    } catch (nextError) {
      setTemplateError(nextError instanceof Error ? nextError.message : "模板创建失败，请稍后再试。");
    } finally {
      setActiveTemplateId(null);
    }
  }

  return (
    <div className="flex min-h-[calc(100vh-2rem)] flex-col gap-4">
      <header className="glass-subtle hero-rim rounded-[32px] px-6 py-6">
        <div className="text-[10px] uppercase tracking-[0.34em] text-white/38">模板推荐</div>
        <h1 className="mt-3 text-3xl font-semibold tracking-[-0.03em] text-white md:text-4xl">根据你的偏好挑选网站模板</h1>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-white/58">
          中间主内容区会优先展示为你推荐的模板和完整模板库，右侧保留偏好标签面板，方便你随时调整推荐条件。已有项目记录也会继续保留在当前页面中。
        </p>
      </header>

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_360px] 2xl:grid-cols-[minmax(0,1fr)_380px]">
        <div className="flex min-w-0 flex-col gap-4">
          {templateError ? <div className="rounded-[22px] border border-rose-400/20 bg-rose-400/10 px-4 py-3 text-sm text-rose-200">{templateError}</div> : null}

          <section className="glass-subtle rounded-[34px] p-5 md:p-6">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div className="min-w-0">
                <div className="flex items-center gap-2 text-sm font-medium text-white/78">
                  <Sparkles className="h-4 w-4 text-sky-300" />
                  <span>为你推荐</span>
                </div>
                <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-white">根据你的偏好推荐的模板</h2>
                <p className="mt-3 max-w-3xl text-sm leading-7 text-white/54">
                  {completeTemplatePreferences
                    ? "这些模板会优先匹配你的行业类型、网站用途、设计风格和目标用户，并保留现有的点击生成与跳转方式。"
                    : "完善 4 类标签后，这里会给出更精准的模板排序。当前先展示默认推荐和部分匹配结果。"}
                </p>
              </div>

              <div className="shrink-0 rounded-full border border-white/10 bg-white/[0.05] px-3 py-1 text-[10px] uppercase tracking-[0.24em] text-white/40">
                {completeTemplatePreferences ? "精准推荐" : "默认推荐"}
              </div>
            </div>

            <div className="mt-5 grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
              {recommendedTemplates.map((template) => (
                <TemplatePromptCard
                  key={`recommended-${template.id}`}
                  template={template}
                  featuredLabel="为你推荐"
                  showMatchSummary
                  busy={activeTemplateId === template.id}
                  onUse={handleUseTemplate}
                />
              ))}
            </div>
          </section>

          <section className="glass-subtle rounded-[34px] p-5 md:p-6">
            <div className="flex items-center gap-2 text-sm font-medium text-white/78">
              <Layers3 className="h-4 w-4 text-fuchsia-300" />
              <span>全部模板</span>
            </div>
            <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-white">完整模板库</h2>
            <p className="mt-3 max-w-3xl text-sm leading-7 text-white/54">保留原有模板展示和使用入口，你可以直接从模板卡片生成新项目，不影响现有跳转、预览和生成流程。</p>

            <div className="mt-5 grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
              {TEMPLATE_LIBRARY.map((template) => (
                <TemplatePromptCard
                  key={template.id}
                  template={template}
                  actionLabel={isAuthenticated ? "使用模板" : "登录后使用"}
                  busy={activeTemplateId === template.id}
                  onUse={handleUseTemplate}
                />
              ))}
            </div>
          </section>

          <section className="glass-subtle rounded-[34px] p-5 md:p-6">
            <div className="flex items-center gap-2 text-sm font-medium text-white/78">
              <Sparkles className="h-4 w-4 text-sky-300" />
              <span>所有项目</span>
            </div>
            <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-white">你的历史创作项目</h2>
            <p className="mt-3 max-w-3xl text-sm leading-7 text-white/54">已有项目入口仍然保留在当前页面，你可以继续查看最近创作记录或进入项目详情页。</p>

            <div className="mt-5 grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
              {projects.length > 0 ? (
                projects.map((project) => (
                  <Link key={project.id} href={`/project/${project.id}`} className="glass-panel rounded-[28px] p-5 transition-all duration-300 hover:-translate-y-1 hover:border-white/16 hover:bg-white/[0.07]">
                    <div className="text-xs uppercase tracking-[0.22em] text-white/34">{statusLabels[project.status] ?? project.status}</div>
                    <div className="mt-4 line-clamp-2 text-lg font-medium text-white">{project.title}</div>
                    <div className="mt-3 line-clamp-3 text-sm leading-7 text-white/54">{project.initial_prompt}</div>
                  </Link>
                ))
              ) : (
                <div className="rounded-[28px] border border-dashed border-white/10 bg-white/[0.03] p-5 text-sm leading-7 text-white/48">你还没有项目。回到首页输入一句需求，马上开始创作。</div>
              )}
            </div>
          </section>
        </div>

        <aside id="templates" className="glass-subtle h-fit rounded-[34px] p-5 md:p-6 xl:sticky xl:top-4">
          <div className="text-[10px] uppercase tracking-[0.34em] text-white/38">偏好标签</div>
          <h2 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-white">调整推荐条件</h2>
          <p className="mt-3 text-sm leading-7 text-white/58">右侧只保留标签面板。每次切换行业、用途、风格或目标用户后，中间的推荐结果都会实时更新。</p>

          {isAuthenticated ? (
            <TemplatePreferenceEditor
              value={templatePreferences}
              onChange={handleTemplatePreferencesChange}
              title="你的偏好标签"
              description="修改标签后，推荐模板会立刻重新计算。所有偏好仅保存在当前前端会话中，不影响现有后端接口。"
              className="mt-5"
            />
          ) : (
            <div className="mt-5 rounded-[28px] border border-dashed border-white/10 bg-white/[0.03] p-5 text-sm leading-7 text-white/48">
              登录或注册后即可保存行业、用途、风格和目标用户标签，并获得更精准的模板推荐。
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}

export function ProjectsScreen() {
  return (
    <AppShell>
      <ProjectsContent />
    </AppShell>
  );
}
