from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import GenerationRecord
from app.schemas.api import GenerateRequest, GenerateResponse, OptimizeRequest, TaskResponse
from app.schemas.design import GeneratedBundle, GenerationLog, PagePlan, PromptAnalysis, ThemeConfig
from app.services.graph import DesignGraphService


router = APIRouter()
graph_service = DesignGraphService()


def _record_to_response(record: GenerationRecord) -> TaskResponse:
    bundle = None
    if record.project_files and record.preview_files:
        bundle = GeneratedBundle(project_files=record.project_files, preview_files=record.preview_files)

    parsed_prompt = PromptAnalysis(**record.parsed_prompt) if record.parsed_prompt else None
    page_plan = PagePlan(**record.page_plan) if record.page_plan else None
    theme = ThemeConfig(**record.theme) if record.theme else None
    logs = [GenerationLog(**log) for log in (record.execution_logs or [])]

    return TaskResponse(
        id=record.id,
        status=record.status,
        prompt=record.prompt,
        parsed_prompt=parsed_prompt,
        page_plan=page_plan,
        theme=theme,
        bundle=bundle,
        logs=logs,
        download_url=f"/api/download/{record.id}" if record.zip_path else None,
        error_message=record.error_message,
    )


def _apply_state_to_record(record: GenerationRecord, state: dict) -> None:
    parsed_prompt = state.get("parsed_prompt")
    page_plan = state.get("page_plan")
    theme = state.get("theme")
    bundle = state.get("bundle")

    record.status = "completed"
    record.parsed_prompt = parsed_prompt.model_dump() if parsed_prompt else None
    record.page_plan = page_plan.model_dump() if page_plan else None
    record.theme = theme.model_dump() if theme else None
    record.project_files = bundle.project_files if bundle else None
    record.preview_files = bundle.preview_files if bundle else None
    record.execution_logs = state.get("logs", [])
    record.zip_path = state.get("zip_path")


@router.post("", response_model=GenerateResponse)
@router.post("/generate", response_model=GenerateResponse)
def generate(payload: GenerateRequest, db: Session = Depends(get_db)):
    record = GenerationRecord(status="running", prompt=payload.prompt, execution_logs=[])
    db.add(record)
    db.commit()
    db.refresh(record)

    try:
        state = graph_service.run(prompt=payload.prompt, task_id=record.id)
        _apply_state_to_record(record, state)
    except Exception as exc:
        record.status = "failed"
        record.error_message = str(exc)
        record.execution_logs = [{"stage": "system", "status": "failed", "detail": str(exc)}]
        db.add(record)
        db.commit()
        raise HTTPException(status_code=500, detail=f"生成失败：{exc}") from exc

    db.add(record)
    db.commit()
    db.refresh(record)
    response = _record_to_response(record)
    return GenerateResponse(**response.model_dump())


@router.get("/task/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    record = db.get(GenerationRecord, task_id)
    if not record:
        raise HTTPException(status_code=404, detail="任务不存在")
    return _record_to_response(record)


@router.get("/download/{task_id}")
def download(task_id: str, db: Session = Depends(get_db)):
    record = db.get(GenerationRecord, task_id)
    if not record or not record.zip_path:
        raise HTTPException(status_code=404, detail="压缩包不存在")

    zip_path = Path(record.zip_path)
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="磁盘中的压缩包文件不存在")

    return FileResponse(zip_path, media_type="application/zip", filename=f"designgen-{task_id}.zip")


@router.post("/optimize", response_model=GenerateResponse)
def optimize(payload: OptimizeRequest, db: Session = Depends(get_db)):
    base_record = db.get(GenerationRecord, payload.task_id)
    if not base_record:
        raise HTTPException(status_code=404, detail="基础任务不存在")

    merged_prompt = f"{base_record.prompt}\n\n继续优化要求：{payload.instruction}\n请继续保持页面文案默认使用简体中文。"
    new_record = GenerationRecord(status="running", prompt=merged_prompt, parent_task_id=base_record.id, execution_logs=[])
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    try:
        state = graph_service.run(prompt=merged_prompt, task_id=new_record.id)
        _apply_state_to_record(new_record, state)
    except Exception as exc:
        new_record.status = "failed"
        new_record.error_message = str(exc)
        new_record.execution_logs = [{"stage": "optimize", "status": "failed", "detail": str(exc)}]
        db.add(new_record)
        db.commit()
        raise HTTPException(status_code=500, detail=f"优化失败：{exc}") from exc

    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    response = _record_to_response(new_record)
    return GenerateResponse(**response.model_dump())
