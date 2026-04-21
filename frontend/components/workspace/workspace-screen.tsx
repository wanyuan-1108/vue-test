"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { PreviewFrame } from "@/components/project/preview-frame";
import { CodeEditor } from "@/components/workspace/code-editor";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { getDownloadUrl, getProject, improveProject } from "@/lib/api";
import { getToken } from "@/lib/auth";
import type { ProjectRecord } from "@/types/designgen";

export function WorkspaceScreen({ projectId }: { projectId: string }) {
  const router = useRouter();
  const [project, setProject] = useState<ProjectRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [improving, setImproving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [improvePrompt, setImprovePrompt] = useState("");
  const [activeFile, setActiveFile] = useState("index.html");

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }

    getProject(projectId)
      .then((response) => {
        setProject(response);
        setActiveFile(Object.keys(response.latest_version?.files ?? {})[0] ?? "index.html");
      })
      .catch((nextError) => {
        setError(nextError instanceof Error ? nextError.message : "项目加载失败。");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [projectId, router]);

  useEffect(() => {
    if (!project || project.status !== "generating") {
      return;
    }

    const timer = window.setInterval(async () => {
      try {
        const latest = await getProject(projectId);
        setProject(latest);
        if (latest.latest_version) {
          setActiveFile(Object.keys(latest.latest_version.files)[0] ?? "index.html");
        }
      } catch {
        window.clearInterval(timer);
      }
    }, 2500);

    return () => window.clearInterval(timer);
  }, [project, projectId]);

  const fileNames = useMemo(() => Object.keys(project?.latest_version?.files ?? {}), [project]);

  async function handleImprove() {
    if (!project || !project.latest_version || !improvePrompt.trim()) return;

    setImproving(true);
    setError(null);

    try {
      const updatedProject = await improveProject(project.id, improvePrompt.trim());
      setProject(updatedProject);
      setActiveFile(Object.keys(updatedProject.latest_version?.files ?? {})[0] ?? "index.html");
      setImprovePrompt("");
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "优化失败，请稍后再试。");
    } finally {
      setImproving(false);
    }
  }

  if (loading) {
    return <div className="flex min-h-screen items-center justify-center text-white/70">正在加载工作台...</div>;
  }

  if (!project) {
    return <div className="flex min-h-screen items-center justify-center text-rose-300">{error ?? "项目不存在。"}</div>;
  }

  return (
    <div className="min-h-screen px-6 py-6 text-white">
      <div className="mx-auto flex max-w-7xl flex-col gap-6">
        <header className="flex flex-col gap-4 rounded-[32px] border border-white/10 bg-white/5 p-5 backdrop-blur-xl lg:flex-row lg:items-center lg:justify-between">
          <div>
            <Link href="/" className="text-sm text-white/45 transition hover:text-white/70">← 返回首页</Link>
            <h1 className="mt-3 text-3xl font-semibold">{project.title}</h1>
            <p className="mt-2 max-w-3xl text-sm leading-7 text-white/60">{project.initial_prompt}</p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Button variant="outline" onClick={() => window.open(getDownloadUrl(project.id), "_blank")}>下载代码</Button>
            <div className="rounded-full border border-white/10 bg-black/20 px-4 py-2 text-sm text-white/60">
              版本 {project.latest_version?.version_no ?? 0}
            </div>
          </div>
        </header>

        <div className="grid gap-6 xl:grid-cols-[360px_minmax(0,1fr)]">
          <Card className="rounded-[32px]">
            <CardHeader>
              <CardTitle>生成进度</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {project.logs.map((log, index) => (
                <div key={`${log}-${index}`} className="rounded-3xl border border-white/10 bg-black/20 p-4 text-sm leading-7 text-white/75">
                  {log}
                </div>
              ))}

              <div className="rounded-3xl border border-dashed border-white/10 p-4 text-sm leading-7 text-white/50">
                继续输入新的优化指令，DesignGen 会在当前页面基础上生成一个新版本。
              </div>
            </CardContent>
          </Card>

          <Card className="rounded-[32px]">
            <CardHeader className="pb-0">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <CardTitle>实时预览</CardTitle>
                <div className="text-sm text-white/50">预览 / 代码</div>
              </div>
            </CardHeader>
            <CardContent className="pt-4">
              <Tabs defaultValue="preview" className="flex h-[720px] flex-col">
                <TabsList>
                  <TabsTrigger value="preview">预览</TabsTrigger>
                  <TabsTrigger value="code">代码</TabsTrigger>
                </TabsList>

                <TabsContent value="preview" className="min-h-0 flex-1">
                  <div className="h-full">
                    {project.latest_version ? (
                      <PreviewFrame previewHtml={project.latest_version.preview_html} />
                    ) : (
                      <div className="flex h-full items-center justify-center bg-slate-950 text-center text-sm text-slate-300">
                        <div>
                          <div className="text-base font-medium">正在生成页面</div>
                          <div className="mt-2 text-slate-400">项目已创建，稍等几秒后会自动显示预览。</div>
                        </div>
                      </div>
                    )}
                  </div>
                </TabsContent>

                <TabsContent value="code" className="flex h-full flex-1 flex-col">
                  <div className="mb-4 flex flex-wrap gap-2">
                    {fileNames.map((fileName) => (
                      <button
                        key={fileName}
                        type="button"
                        onClick={() => setActiveFile(fileName)}
                        className={`rounded-full px-4 py-2 text-sm transition ${
                          activeFile === fileName ? "bg-white text-slate-900" : "border border-white/10 bg-white/5 text-white/70"
                        }`}
                      >
                        {fileName}
                      </button>
                    ))}
                  </div>
                  <div className="min-h-0 flex-1 overflow-hidden rounded-[28px] border border-white/10">
                    {project.latest_version ? (
                      <CodeEditor fileName={activeFile} code={project.latest_version.files[activeFile] ?? ""} />
                    ) : (
                      <div className="flex h-full items-center justify-center bg-slate-950 text-sm text-slate-400">
                        代码会在页面生成完成后自动出现。
                      </div>
                    )}
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>

        <Card className="rounded-[32px]">
          <CardHeader>
            <CardTitle>继续优化页面</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Textarea
                className="min-h-[140px]"
                placeholder="例如：让首屏更高级，增加用户评价区，并优化移动端排版"
                value={improvePrompt}
                onChange={(event) => setImprovePrompt(event.target.value)}
              />
              {error ? <p className="text-sm text-rose-300">{error}</p> : null}
              <div className="flex justify-end">
                <Button size="lg" onClick={handleImprove} disabled={improving || !improvePrompt.trim() || !project.latest_version}>
                  {improving ? "正在优化..." : "继续优化"}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
