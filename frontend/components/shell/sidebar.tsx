"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FolderOpen, Home, Layers3, LogOut, Sparkles } from "lucide-react";

import { SidebarProjects } from "@/components/shell/sidebar-projects";
import { SidebarUser } from "@/components/shell/sidebar-user";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

import { useShell } from "@/components/shell/app-shell";

const primaryNav = [
  { href: "/", label: "首页", icon: Home },
  { href: "/projects", label: "项目", icon: FolderOpen },
];

export function Sidebar() {
  const pathname = usePathname();
  const { signOut, isAuthenticated } = useShell();

  return (
    <aside className="glass-shell hidden w-[292px] shrink-0 flex-col rounded-[36px] px-4 py-5 lg:flex">
      <div className="surface-elevated flex items-center gap-3 rounded-[28px] px-4 py-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-[20px] bg-[linear-gradient(135deg,rgba(132,144,255,0.95),rgba(90,202,255,0.9))] text-sm font-semibold text-slate-950 shadow-[0_16px_34px_rgba(92,115,255,0.34)]">
          AI
        </div>
        <div>
          <div className="text-[10px] uppercase tracking-[0.34em] text-white/40">AI 网页工作台</div>
          <div className="mt-1 text-lg font-semibold text-white">DesignGen</div>
        </div>
      </div>

      <div className="mt-5">
        <SidebarUser />
      </div>

      <nav className="mt-6 space-y-2 px-1">
        {primaryNav.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "group flex items-center gap-3 rounded-[22px] px-4 py-3 text-sm transition-all duration-300",
                active
                  ? "surface-elevated text-white"
                  : "text-white/62 hover:-translate-y-0.5 hover:bg-white/[0.06] hover:text-white"
              )}
            >
              <div
                className={cn(
                  "flex h-9 w-9 items-center justify-center rounded-2xl border transition-all duration-300",
                  active
                    ? "border-white/14 bg-white/[0.08] text-white"
                    : "border-transparent bg-white/[0.02] text-white/58 group-hover:border-white/10 group-hover:bg-white/[0.08] group-hover:text-white"
                )}
              >
                <Icon className="h-4 w-4" />
              </div>
              <span className="font-medium tracking-[0.01em]">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="mt-6 px-1">
        <div className="glass-panel rounded-[28px] p-4">
          <div className="flex items-center gap-2 text-sm font-medium text-white/80">
            <Sparkles className="h-4 w-4 text-sky-300" />
            <span>项目</span>
          </div>
          <SidebarProjects />
        </div>
      </div>

      <div className="mt-auto px-1 pt-6">
        <Link href="/projects" className="group flex items-center gap-3 rounded-[22px] px-4 py-3 text-sm text-white/62 transition-all duration-300 hover:-translate-y-0.5 hover:bg-white/[0.06] hover:text-white">
          <div className="flex h-9 w-9 items-center justify-center rounded-2xl bg-white/[0.04] text-white/58 transition-all duration-300 group-hover:bg-white/[0.08] group-hover:text-white">
            <Layers3 className="h-4 w-4" />
          </div>
          <span>模板</span>
        </Link>

        {isAuthenticated ? (
          <Button variant="ghost" className="mt-2 w-full justify-start rounded-[22px] px-4 py-3 text-white/62 hover:text-white" onClick={signOut}>
            <LogOut className="mr-3 h-4 w-4" />
            退出登录
          </Button>
        ) : null}
      </div>
    </aside>
  );
}
