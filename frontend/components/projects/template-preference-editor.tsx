"use client";

import { TEMPLATE_PREFERENCE_GROUPS, type UserTemplatePreferences } from "@/lib/template-preferences";
import { cn } from "@/lib/utils";

export function TemplatePreferenceEditor({
  value,
  onChange,
  title = "兴趣标签",
  description = "完善偏好后，我们会优先推荐更贴近你需求的网站模板。",
  className,
}: {
  value: UserTemplatePreferences;
  onChange: (nextValue: UserTemplatePreferences) => void;
  title?: string;
  description?: string;
  className?: string;
}) {
  function handleSelect(groupKey: keyof UserTemplatePreferences, option: string) {
    const nextValue = value[groupKey] === option ? "" : option;
    onChange({
      ...value,
      [groupKey]: nextValue,
    });
  }

  return (
    <section className={cn("rounded-[28px] border border-white/10 bg-white/[0.03] p-5", className)}>
      <div>
        <div className="text-sm font-medium text-white">{title}</div>
        <p className="mt-2 text-sm leading-6 text-white/54">{description}</p>
      </div>

      <div className="mt-5 space-y-5">
        {TEMPLATE_PREFERENCE_GROUPS.map((group) => (
          <div key={group.key}>
            <div className="flex items-center justify-between gap-3">
              <div className="text-sm font-medium text-white/82">{group.label}</div>
              <div className="text-[10px] uppercase tracking-[0.24em] text-white/30">单选</div>
            </div>
            <div className="mt-1 text-xs leading-5 text-white/42">{group.description}</div>
            <div className="mt-3 flex flex-wrap gap-2">
              {group.options.map((option) => {
                const active = value[group.key] === option;

                return (
                  <button
                    key={option}
                    type="button"
                    onClick={() => handleSelect(group.key, option)}
                    className={cn(
                      "rounded-full px-3 py-2 text-xs transition-all duration-300",
                      active
                        ? "bg-[linear-gradient(135deg,rgba(129,140,248,1),rgba(88,197,255,0.92))] text-slate-950 shadow-[0_10px_24px_rgba(82,112,255,0.24)]"
                        : "border border-white/10 bg-white/[0.05] text-white/62 hover:-translate-y-0.5 hover:border-white/20 hover:bg-white/[0.08] hover:text-white"
                    )}
                  >
                    {option}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
