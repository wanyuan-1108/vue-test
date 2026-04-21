"use client";

import { CodeViewer } from "@/components/project/code-viewer";
import { PreviewFrame } from "@/components/project/preview-frame";
import { ProjectToolbar } from "@/components/project/project-toolbar";
import type { ProjectRecord } from "@/types/designgen";

export function ProjectPreviewPanel({
  project,
  activeView,
  onChangeView,
  onShare,
  onDownload,
  expanded,
  onToggleExpanded,
  activeFile,
  onSelectFile,
}: {
  project: ProjectRecord;
  activeView: "preview" | "code";
  onChangeView: (view: "preview" | "code") => void;
  onShare: () => void;
  onDownload: () => void;
  expanded: boolean;
  onToggleExpanded: () => void;
  activeFile: string;
  onSelectFile: (fileName: string) => void;
}) {
  const fileNames = Object.keys(project.latest_version?.files ?? {});

  return (
    <section className="glass-subtle hero-rim flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden rounded-[36px]">
      <ProjectToolbar
        activeView={activeView}
        onChangeView={onChangeView}
        onShare={onShare}
        onDownload={onDownload}
        onToggleExpanded={onToggleExpanded}
        expanded={expanded}
        canDownload={Boolean(project.latest_version)}
      />

      <div className="min-h-0 flex-1 p-4">
        {activeView === "preview" ? (
          project.latest_version ? (
            <PreviewFrame previewHtml={project.latest_version.preview_html} />
          ) : (
            <div className="glass-panel flex h-full items-center justify-center rounded-[30px] text-center text-sm text-white/48">
              <div>
                <div className="text-base font-medium text-white/82">正在生成预览</div>
                <div className="mt-2">生成完成后，这里会显示完整的网站页面。</div>
              </div>
            </div>
          )
        ) : project.latest_version ? (
          <div className="flex h-full min-h-0 flex-col rounded-[30px] border border-white/10 bg-slate-950/70 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
            <div className="flex flex-wrap gap-2 border-b border-white/10 px-4 py-4">
              {fileNames.map((fileName) => (
                <button
                  key={fileName}
                  type="button"
                  onClick={() => onSelectFile(fileName)}
                  className={`rounded-full px-4 py-2 text-sm transition-all duration-300 ${
                    activeFile === fileName ? "bg-[linear-gradient(135deg,rgba(129,140,248,1),rgba(88,197,255,0.92))] text-slate-950 shadow-[0_12px_28px_rgba(82,112,255,0.28)]" : "border border-white/10 bg-white/[0.04] text-white/62 hover:-translate-y-0.5 hover:border-white/20 hover:text-white"
                  }`}
                >
                  {fileName}
                </button>
              ))}
            </div>
            <div className="min-h-0 flex-1 overflow-hidden rounded-b-[30px]">
              <CodeViewer fileName={activeFile} code={project.latest_version.files[activeFile] ?? ""} />
            </div>
          </div>
        ) : (
          <div className="glass-panel flex h-full items-center justify-center rounded-[30px] text-sm text-white/48">
            代码会在生成完成后自动出现。
          </div>
        )}
      </div>
    </section>
  );
}
