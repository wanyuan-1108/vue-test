from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.design import GeneratedBundle, GenerationLog, PagePlan, PromptAnalysis, ThemeConfig


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=8)


class OptimizeRequest(BaseModel):
    task_id: str
    instruction: str = Field(min_length=3)


class TaskResponse(BaseModel):
    id: str
    status: str
    prompt: str
    parsed_prompt: Optional[PromptAnalysis] = None
    page_plan: Optional[PagePlan] = None
    theme: Optional[ThemeConfig] = None
    bundle: Optional[GeneratedBundle] = None
    logs: List[GenerationLog] = Field(default_factory=list)
    download_url: Optional[str] = None
    error_message: Optional[str] = None


class GenerateResponse(TaskResponse):
    pass
