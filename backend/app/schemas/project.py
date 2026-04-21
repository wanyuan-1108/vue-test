from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    prompt: str = Field(min_length=8, max_length=4000)


class ProjectImproveRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=4000)


class ProjectSummaryResponse(BaseModel):
    id: str
    title: str
    status: str
    initial_prompt: str
    updated_at: datetime


class ProjectVersionResponse(BaseModel):
    id: str
    version_no: int
    prompt: str
    files: dict[str, str]
    preview_html: str
    created_at: datetime


class ProjectResponse(BaseModel):
    id: str
    title: str
    status: str
    initial_prompt: str
    created_at: datetime
    updated_at: datetime
    logs: list[str]
    latest_version: ProjectVersionResponse | None = None
    download_url: str | None = None
