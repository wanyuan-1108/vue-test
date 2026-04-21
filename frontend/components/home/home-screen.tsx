"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { AppShell, useShell } from "@/components/shell/app-shell";
import { HomeHero } from "@/components/home/home-hero";
import { Button } from "@/components/ui/button";
import { createProject } from "@/lib/api";
import { getToken } from "@/lib/auth";

function HomeContent() {
  const router = useRouter();
  const { user, isAuthenticated, refreshProjects } = useShell();
  const [prompt, setPrompt] = useState("创建一个咖啡品牌官网");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate() {
    if (!prompt.trim()) {
      return;
    }

    if (!getToken() || !isAuthenticated) {
      router.push("/login");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const project = await createProject(prompt.trim());
      await refreshProjects();
      router.push(`/project/${project.id}`);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "生成失败，请稍后再试。");
      setLoading(false);
    }
  }

  return (
    <>
      <header className="glass-subtle flex items-center justify-between rounded-[28px] px-5 py-4">
        <div>
          <div className="text-xs uppercase tracking-[0.28em] text-white/42">DesignGen</div>
          <div className="mt-1 text-base text-white/72">AI 网页生成器</div>
        </div>
        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <div className="rounded-full border border-white/10 bg-white/[0.06] px-4 py-2 text-sm text-white/70">{user?.name}</div>
          ) : (
            <>
              <Link href="/login"><Button variant="ghost">登录</Button></Link>
              <Link href="/register"><Button>注册</Button></Link>
            </>
          )}
        </div>
      </header>

      <div className="mt-4 flex min-h-0 flex-1 flex-col">
        <HomeHero user={user} prompt={prompt} onPromptChange={setPrompt} onSubmit={handleGenerate} loading={loading} />
        {error ? <p className="mt-4 text-center text-sm text-rose-300">{error}</p> : null}
      </div>
    </>
  );
}

export function HomeScreen() {
  return (
    <AppShell>
      <HomeContent />
    </AppShell>
  );
}
