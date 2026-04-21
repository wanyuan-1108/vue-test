"use client";

import { Button } from "@/components/ui/button";
import type { RecommendedTemplate, TemplateIdea } from "@/lib/template-library";
import { cn } from "@/lib/utils";

type TemplatePromptCardProps = {
  template: TemplateIdea | RecommendedTemplate;
  onUse: (template: TemplateIdea) => void;
  busy?: boolean;
  featuredLabel?: string;
  showMatchSummary?: boolean;
  actionLabel?: string;
};

function hasMatchedGroups(template: TemplateIdea | RecommendedTemplate): template is RecommendedTemplate {
  return Array.isArray((template as RecommendedTemplate).matchedGroups);
}

export function TemplatePromptCard({
  template,
  onUse,
  busy = false,
  featuredLabel,
  showMatchSummary = false,
  actionLabel = "立即生成",
}: TemplatePromptCardProps) {
  const matchedGroups = hasMatchedGroups(template) ? template.matchedGroups : [];

  return (
    <div
      className={cn(
        "glass-panel flex h-full flex-col rounded-[24px] p-4 transition-all duration-300",
        featuredLabel ? "border-white/14 bg-white/[0.06]" : "hover:-translate-y-1 hover:border-white/16 hover:bg-white/[0.07]"
      )}
    >
      <div className="flex items-center justify-between gap-3">
        <div className="text-xs uppercase tracking-[0.22em] text-white/34">{featuredLabel ?? template.badge ?? "模板"}</div>
        {"recommendationScore" in template && template.recommendationScore > 0 ? (
          <div className="rounded-full border border-emerald-300/20 bg-emerald-300/10 px-3 py-1 text-[10px] uppercase tracking-[0.2em] text-emerald-200">
            {template.recommendationScore} 分匹配
          </div>
        ) : null}
      </div>

      <div className="mt-3 text-base font-medium leading-6 text-white">{template.title}</div>
      <div className="mt-2 text-sm leading-7 text-white/54">{template.description}</div>
      <div className="mt-4 rounded-[18px] border border-white/8 bg-slate-950/40 px-3 py-3 text-sm leading-6 text-white/72">{template.prompt}</div>

      {showMatchSummary && matchedGroups.length > 0 ? (
        <div className="mt-4 flex flex-wrap gap-2">
          {matchedGroups.map((match) => (
            <div key={`${template.id}-${match.key}-${match.value}`} className="rounded-full border border-sky-300/20 bg-sky-300/10 px-3 py-1 text-[11px] text-sky-100">
              {match.label} · {match.value}
            </div>
          ))}
        </div>
      ) : null}

      <div className="mt-auto pt-4">
        <Button variant="outline" size="sm" className="rounded-full" disabled={busy} onClick={() => onUse(template)}>
          {busy ? "正在创建..." : actionLabel}
        </Button>
      </div>
    </div>
  );
}
