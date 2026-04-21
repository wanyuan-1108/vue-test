"use client";

import { ScrollArea } from "@/components/ui/scroll-area";
import type { ProjectRecord } from "@/types/designgen";

import { ProjectComposer } from "@/components/project/project-composer";

export function ProjectChatPanel({
  project,
  error,
  improvePrompt,
  onImprovePrompt,
  onImprove,
  improving,
  canImprove,
}: {
  project: ProjectRecord;
  error: string | null;
  improvePrompt: string;
  onImprovePrompt: (value: string) => void;
  onImprove: () => void;
  improving: boolean;
  canImprove: boolean;
}) {
  return (
    <section className="glass-subtle hero-rim flex min-h-0 w-[420px] shrink-0 flex-col overflow-hidden rounded-[36px]">
      <div className="border-b border-white/10 px-6 py-6">
        <div className="text-[10px] uppercase tracking-[0.34em] text-white/38">AI 工作台</div>
        <h1 className="mt-3 text-2xl font-semibold tracking-[-0.03em] text-white">{project.title}</h1>
        <p className="mt-3 text-sm leading-7 text-white/56">{project.initial_prompt}</p>
      </div>

      <ScrollArea className="min-h-0 flex-1 px-6 py-5">
        <div className="space-y-4">
          {project.logs.map((log, index) => (
            <div key={`${log}-${index}`} className="glass-panel rounded-[28px] px-4 py-4 text-sm leading-7 text-white/78">
              {log}
            </div>
          ))}

          {!project.latest_version ? (
            <div className="rounded-[28px] border border-dashed border-white/10 bg-white/[0.03] px-4 py-5 text-sm leading-7 text-white/48">
              页面正在生成中。你可以先观察右侧预览区域，生成完成后内容会自动出现。
            </div>
          ) : null}

          {error ? <div className="rounded-[28px] border border-rose-400/20 bg-rose-400/10 px-4 py-4 text-sm text-rose-200">{error}</div> : null}
        </div>
      </ScrollArea>

      <ProjectComposer value={improvePrompt} onChange={onImprovePrompt} onSubmit={onImprove} loading={improving} disabled={!canImprove} />
    </section>
  );
}
