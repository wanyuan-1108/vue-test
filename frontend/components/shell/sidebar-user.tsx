"use client";

import Link from "next/link";

import { Button } from "@/components/ui/button";

import { useShell } from "@/components/shell/app-shell";

export function SidebarUser() {
  const { user, isAuthenticated } = useShell();

  if (!isAuthenticated || !user) {
    return (
      <div className="glass-panel rounded-[28px] p-5">
        <div className="inline-flex rounded-full border border-white/10 bg-white/[0.06] px-3 py-1 text-[10px] uppercase tracking-[0.28em] text-white/42">创作入口</div>
        <div className="mt-4 text-sm font-medium text-white">开始你的 AI 创作</div>
        <p className="mt-2 text-sm leading-6 text-white/55">登录后可以保存项目、继续优化页面，并随时回到最近创作记录。</p>
        <div className="mt-4 flex gap-2">
          <Link href="/login"><Button size="sm" variant="outline">登录</Button></Link>
          <Link href="/register"><Button size="sm">注册</Button></Link>
        </div>
      </div>
    );
  }

  const initials = user.name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("");

  return (
    <div className="glass-panel rounded-[28px] p-5">
      <div className="flex items-center gap-3">
        <div className="flex h-12 w-12 items-center justify-center rounded-[18px] bg-[linear-gradient(135deg,rgba(129,140,248,0.92),rgba(76,201,255,0.86))] text-sm font-semibold text-slate-950 shadow-[0_16px_32px_rgba(85,108,255,0.3)]">
          {initials || "DG"}
        </div>
        <div className="min-w-0">
          <div className="truncate font-medium text-white">{user.name}</div>
          <div className="truncate text-sm text-white/50">{user.email}</div>
        </div>
      </div>
    </div>
  );
}
