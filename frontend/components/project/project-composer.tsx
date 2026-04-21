"use client";

import { WandSparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export function ProjectComposer({
  value,
  onChange,
  onSubmit,
  loading,
  disabled,
}: {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
  disabled: boolean;
}) {
  return (
    <div className="border-t border-white/10 px-5 py-4">
      <div className="glass-panel rounded-[28px] p-3">
        <Textarea
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder="继续描述你想优化的内容，例如：把首屏做得更高级，并增加用户评价区域"
          className="min-h-[120px] border-0 bg-transparent px-2 py-2 text-sm leading-7 text-white placeholder:text-white/34 focus:ring-0"
        />
        <div className="mt-3 flex justify-end">
          <Button onClick={onSubmit} disabled={loading || disabled || !value.trim()} className="rounded-full">
            <WandSparkles className="mr-2 h-4 w-4" />
            {loading ? "正在优化..." : "继续优化"}
          </Button>
        </div>
      </div>
    </div>
  );
}
