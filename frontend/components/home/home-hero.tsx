"use client";

import { PromptChips } from "@/components/home/prompt-chips";
import { PromptComposer } from "@/components/home/prompt-composer";
import type { AuthUser } from "@/types/designgen";

const EXAMPLE_PROMPTS = [
  "创建一个咖啡品牌官网",
  "制作一个 SaaS 产品落地页",
  "设计一个个人作品集网站",
];

export function HomeHero({
  user,
  prompt,
  onPromptChange,
  onSubmit,
  loading,
}: {
  user: AuthUser | null;
  prompt: string;
  onPromptChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
}) {
  return (
    <section className="relative flex flex-1 items-center justify-center overflow-hidden rounded-[40px] border border-white/10 bg-white/[0.03] px-6 py-12 backdrop-blur-xl md:px-12">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(88,120,255,0.18),transparent_34%),radial-gradient(circle_at_bottom,rgba(255,82,163,0.16),transparent_28%)]" />

      <div className="relative z-10 mx-auto flex max-w-5xl flex-col items-center text-center">
        <div className="inline-flex rounded-full border border-white/10 bg-white/[0.06] px-4 py-2 text-xs uppercase tracking-[0.28em] text-white/50">
          AI 创作
        </div>
        <h1 className="mt-8 max-w-3xl text-4xl font-semibold tracking-tight text-white md:text-6xl md:leading-[1.08]">
          准备好构建你的网站了吗，{user?.name ?? "创作者"}？
        </h1>
        <p className="mt-5 max-w-2xl text-base leading-8 text-white/58 md:text-lg">
          从一句自然语言开始，DesignGen 会帮你设计页面结构、生成网页内容，并直接给出可预览、可下载的完整网站源码。
        </p>

        <div className="mt-10 w-full">
          <PromptComposer prompt={prompt} onPromptChange={onPromptChange} onSubmit={onSubmit} loading={loading} />
          <PromptChips prompts={EXAMPLE_PROMPTS} onSelect={onPromptChange} />
        </div>
      </div>
    </section>
  );
}
