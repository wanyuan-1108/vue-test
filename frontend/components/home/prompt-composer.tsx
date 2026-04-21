"use client";

import { ArrowUp, Mic, Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export function PromptComposer({
  prompt,
  onPromptChange,
  onSubmit,
  loading,
}: {
  prompt: string;
  onPromptChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
}) {
  return (
    <div className="glass-floating mx-auto w-full max-w-[700px] rounded-[32px] p-3 shadow-[0_20px_80px_rgba(8,12,30,0.45)]">
      <Textarea
        value={prompt}
        onChange={(event) => onPromptChange(event.target.value)}
        placeholder="描述你想构建的网站……"
        className="min-h-[92px] border-0 bg-transparent px-3 py-3 text-base leading-7 text-white placeholder:text-white/35 focus:ring-0"
      />
      <div className="mt-2 flex items-center justify-between px-2 pb-1">
        <div className="flex items-center gap-2">
          <button type="button" className="icon-glass-button" aria-label="添加更多上下文">
            <Plus className="h-4 w-4" />
          </button>
          <button type="button" className="icon-glass-button" aria-label="语音输入">
            <Mic className="h-4 w-4" />
          </button>
        </div>
        <Button size="icon" className="h-11 w-11 rounded-[18px] bg-white text-slate-950 hover:bg-white/90" onClick={onSubmit} disabled={loading}>
          <ArrowUp className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
