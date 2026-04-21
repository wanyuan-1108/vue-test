"use client";

import { Download, Expand, Share2, Shrink } from "lucide-react";

import { Button } from "@/components/ui/button";

export function ProjectToolbar({
  activeView,
  onChangeView,
  onShare,
  onDownload,
  onToggleExpanded,
  expanded,
  canDownload,
}: {
  activeView: "preview" | "code";
  onChangeView: (view: "preview" | "code") => void;
  onShare: () => void;
  onDownload: () => void;
  onToggleExpanded: () => void;
  expanded: boolean;
  canDownload: boolean;
}) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 px-5 py-4">
      <div className="inline-flex items-center rounded-full border border-white/10 bg-white/[0.05] p-1 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
        <button
          type="button"
          onClick={() => onChangeView("preview")}
          className={`rounded-full px-4 py-2 text-sm transition-all duration-300 ${activeView === "preview" ? "bg-[linear-gradient(135deg,rgba(129,140,248,1),rgba(88,197,255,0.92))] text-slate-950 shadow-[0_10px_24px_rgba(82,112,255,0.24)]" : "text-white/62 hover:text-white"}`}
        >
          预览
        </button>
        <button
          type="button"
          onClick={() => onChangeView("code")}
          className={`rounded-full px-4 py-2 text-sm transition-all duration-300 ${activeView === "code" ? "bg-[linear-gradient(135deg,rgba(129,140,248,1),rgba(88,197,255,0.92))] text-slate-950 shadow-[0_10px_24px_rgba(82,112,255,0.24)]" : "text-white/62 hover:text-white"}`}
        >
          代码
        </button>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <Button variant="outline" size="sm" className="rounded-full" onClick={onShare}>
          <Share2 className="mr-2 h-4 w-4" />
          分享
        </Button>
        <Button variant="outline" size="sm" className="rounded-full" onClick={onDownload} disabled={!canDownload}>
          <Download className="mr-2 h-4 w-4" />
          下载
        </Button>
        <Button variant="outline" size="sm" className="rounded-full" onClick={onToggleExpanded}>
          {expanded ? <Shrink className="mr-2 h-4 w-4" /> : <Expand className="mr-2 h-4 w-4" />}
          {expanded ? "显示对话区" : "放大预览"}
        </Button>
      </div>
    </div>
  );
}
