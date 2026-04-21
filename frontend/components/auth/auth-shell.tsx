import Link from "next/link";

import { cn } from "@/lib/utils";

export function AuthShell({
  title,
  description,
  footer,
  children,
  panelClassName,
}: {
  title: string;
  description: string;
  footer: React.ReactNode;
  children: React.ReactNode;
  panelClassName?: string;
}) {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-6 py-12">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(124,92,252,0.24),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(118,229,255,0.14),transparent_22%)]" />
      <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.04),rgba(255,255,255,0))]" />
      <div className="pointer-events-none absolute left-[12%] top-[14%] h-56 w-56 rounded-full bg-[radial-gradient(circle,rgba(118,124,255,0.2),transparent_68%)] blur-3xl" />
      <div className="pointer-events-none absolute bottom-[10%] right-[12%] h-72 w-72 rounded-full bg-[radial-gradient(circle,rgba(84,198,255,0.12),transparent_70%)] blur-3xl" />

      <div className={cn("glass-shell hero-rim relative z-10 w-full max-w-md rounded-[34px] p-8", panelClassName)}>
        <Link href="/" className="mb-8 inline-flex items-center gap-3 text-white">
          <div className="flex h-11 w-11 items-center justify-center rounded-[18px] bg-[linear-gradient(135deg,rgba(129,140,248,0.92),rgba(76,201,255,0.88))] text-sm font-semibold text-slate-950 shadow-[0_16px_32px_rgba(85,108,255,0.3)]">AI</div>
          <div>
            <div className="text-[11px] uppercase tracking-[0.26em] text-white/42">AI 网页生成器</div>
            <div className="mt-1 text-lg font-semibold">DesignGen</div>
          </div>
        </Link>

        <div className="space-y-2">
          <h1 className="text-3xl font-semibold tracking-[-0.03em] text-white">{title}</h1>
          <p className="text-sm leading-6 text-white/60">{description}</p>
        </div>

        <div className="mt-8">{children}</div>
        <div className="mt-6 text-sm text-white/60">{footer}</div>
      </div>
    </div>
  );
}
