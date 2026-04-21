"use client";

import Link from "next/link";

import { useShell } from "@/components/shell/app-shell";

const sections = [
  { label: "所有项目", href: "/projects" },
  { label: "最近项目", href: "/projects" },
  { label: "模板", href: "/projects#templates" },
];

export function SidebarProjects() {
  const { projects } = useShell();

  return (
    <div className="mt-4 space-y-4">
      <div className="space-y-1">
        {sections.map((section) => (
          <Link key={section.label} href={section.href} className="flex items-center justify-between rounded-[18px] px-3 py-2.5 text-sm text-white/58 transition-all duration-300 hover:bg-white/[0.08] hover:text-white">
            <span>{section.label}</span>
            <span className="text-[10px] uppercase tracking-[0.2em] text-white/30">打开</span>
          </Link>
        ))}
      </div>

      <div className="space-y-2 border-t border-white/8 pt-4">
        <div className="px-3 text-xs uppercase tracking-[0.26em] text-white/34">最近</div>
        {projects.length > 0 ? (
          projects.slice(0, 4).map((project) => (
            <Link key={project.id} href={`/project/${project.id}`} className="block rounded-[20px] border border-transparent px-3 py-3 transition-all duration-300 hover:-translate-y-0.5 hover:border-white/10 hover:bg-white/[0.08]">
              <div className="line-clamp-1 text-sm font-medium text-white/84">{project.title}</div>
              <div className="mt-1 line-clamp-2 text-xs leading-5 text-white/45">{project.initial_prompt}</div>
            </Link>
          ))
        ) : (
          <div className="px-3 text-sm leading-6 text-white/42">你的最近项目会显示在这里。</div>
        )}
      </div>
    </div>
  );
}
