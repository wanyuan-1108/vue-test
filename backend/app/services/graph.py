from __future__ import annotations

from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, StateGraph

from app.schemas.design import GeneratedBundle, GeneratedWebsite
from app.services.ai_client import AIClient
from app.services.generators.packaging import write_bundle_zip
from app.services.website_generator import AIWebsiteGenerator


class GraphState(TypedDict, total=False):
    prompt: str
    task_id: str
    website: GeneratedWebsite
    bundle: GeneratedBundle
    logs: List[Dict[str, str]]
    zip_path: str
    error_message: str


def _append_log(state: GraphState, stage: str, status: str, detail: str) -> Dict[str, List[Dict[str, str]]]:
    logs = list(state.get("logs", []))
    logs.append({"stage": stage, "status": status, "detail": detail})
    return {"logs": logs}


class DesignGraphService:
    def __init__(self) -> None:
        self.ai_client = AIClient()
        self.website_generator = AIWebsiteGenerator(self.ai_client)
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(GraphState)

        graph.add_node("ai_codegen", self.ai_codegen)
        graph.add_node("bundle_packaging", self.bundle_packaging)

        graph.set_entry_point("ai_codegen")
        graph.add_edge("ai_codegen", "bundle_packaging")
        graph.add_edge("bundle_packaging", END)

        return graph.compile()

    def ai_codegen(self, state: GraphState) -> Dict[str, Any]:
        website = self.website_generator.generate(state["prompt"])
        bundle = self.website_generator.to_bundle(website)
        return {
            "website": website,
            "bundle": bundle,
            **_append_log(
                state,
                "ai_codegen",
                "completed",
                f"AI 已根据需求直接生成完整网页代码：{len(bundle.project_files)} 个源码文件，可直接渲染 HTML/CSS/JavaScript。",
            ),
        }

    def bundle_packaging(self, state: GraphState) -> Dict[str, Any]:
        zip_path = write_bundle_zip(state.get("task_id", "preview-task"), state["bundle"])
        return {
            "zip_path": str(zip_path),
            **_append_log(state, "bundle_packaging", "completed", "已打包生成结果，前端可直接使用返回的 HTML / CSS / JavaScript 进行渲染。"),
        }

    def run(self, *, prompt: str, task_id: str) -> GraphState:
        initial_state: GraphState = {
            "prompt": prompt,
            "logs": [{"stage": "system", "status": "running", "detail": "开始调用外部 AI 生成网页代码。"}],
            "task_id": task_id,
        }
        final_state = self.graph.invoke(initial_state)
        final_logs = list(final_state.get("logs", []))
        final_logs.append({"stage": "system", "status": "completed", "detail": "任务完成，已返回源码文件和预览文档。"})
        final_state["logs"] = final_logs
        return final_state
