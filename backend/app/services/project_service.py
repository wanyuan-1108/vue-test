from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Project, ProjectLog, ProjectVersion, User
from app.services.ai_client import AIClient
from app.services.website_generator import AIWebsiteGenerator
from app.services.zip_service import write_zip_file


def _build_generator() -> AIWebsiteGenerator:
    return AIWebsiteGenerator(AIClient())


def _default_logs() -> list[str]:
    return [
        "正在分析你的需求…",
        "正在设计页面结构…",
        "正在生成页面内容与视觉效果…",
        "页面生成完成。",
    ]


def get_status_logs(status: str) -> list[str]:
    if status == "generating":
        return [
            "正在分析你的需求...",
            "正在设计页面结构...",
            "正在生成页面内容与视觉效果...",
            "页面生成完成后会自动显示在右侧。",
        ]
    if status == "failed":
        return ["这次生成没有成功，请返回首页重新尝试。"]
    return []


def _version_to_files(version: ProjectVersion) -> dict[str, str]:
    return {
        "index.html": version.html_code,
        "styles.css": version.css_code,
        "script.js": version.js_code,
    }


def _next_version_number(db: Session, project_id: str) -> int:
    latest = db.query(func.max(ProjectVersion.version_no)).filter(ProjectVersion.project_id == project_id).scalar()
    return int(latest or 0) + 1


def _build_improvement_prompt(version: ProjectVersion, instruction: str) -> str:
    return (
        "请基于以下现有网站继续优化，并返回完整的新版本 HTML、CSS、JavaScript。\n"
        "除非用户明确要求其他语言，否则页面导航、标题、按钮、正文等文案默认继续使用简体中文。\n\n"
        f"优化要求：{instruction.strip()}\n\n"
        "当前 HTML：\n"
        f"{version.html_code}\n\n"
        "当前 CSS：\n"
        f"{version.css_code}\n\n"
        "当前 JavaScript：\n"
        f"{version.js_code}"
    )


def _fallback_title(prompt: str) -> str:
    trimmed = " ".join(prompt.strip().split())
    return trimmed[:60] or "未命名项目"


def _persist_version(
    db: Session,
    *,
    project: Project,
    version_no: int,
    prompt: str,
    html_code: str,
    css_code: str,
    js_code: str,
    preview_html: str,
    log_messages: list[str],
) -> ProjectVersion:
    version = ProjectVersion(
        project_id=project.id,
        version_no=version_no,
        prompt=prompt,
        html_code=html_code,
        css_code=css_code,
        js_code=js_code,
        preview_html=preview_html,
    )
    db.add(version)
    db.flush()

    zip_path = write_zip_file(project_id=project.id, version_no=version.version_no, files=_version_to_files(version))
    version.zip_path = str(zip_path)

    for sort_order, message in enumerate(log_messages, start=1):
        db.add(
            ProjectLog(
                project_id=project.id,
                version_id=version.id,
                message=message,
                sort_order=sort_order,
            )
        )

    project.status = "ready"
    db.add(project)
    db.commit()
    db.refresh(version)
    db.refresh(project)
    return version


def create_project(db: Session, *, user: User, prompt: str) -> Project:
    project = Project(
        user_id=user.id,
        title=_fallback_title(prompt),
        initial_prompt=prompt,
        status="generating",
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    try:
        generator = _build_generator()
        website = generator.generate(prompt)
        bundle = generator.to_bundle(website)
        project.title = website.title.strip() or _fallback_title(prompt)
        _persist_version(
            db,
            project=project,
            version_no=1,
            prompt=prompt,
            html_code=bundle.project_files["index.html"],
            css_code=bundle.project_files["styles.css"],
            js_code=bundle.project_files["script.js"],
            preview_html=bundle.preview_files["/index.html"],
            log_messages=_default_logs(),
        )
    except Exception as exc:
        project.status = "failed"
        db.add(project)
        db.commit()
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return db.get(Project, project.id)


def create_project_shell(db: Session, *, user: User, prompt: str) -> Project:
    project = Project(
        user_id=user.id,
        title=_fallback_title(prompt),
        initial_prompt=prompt,
        status="generating",
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def run_generation_for_project(project_id: str) -> None:
    db = SessionLocal()
    try:
        project = db.get(Project, project_id)
        if project is None:
            return

        generator = _build_generator()
        website = generator.generate(project.initial_prompt)
        bundle = generator.to_bundle(website)
        project.title = website.title.strip() or _fallback_title(project.initial_prompt)
        _persist_version(
            db,
            project=project,
            version_no=1,
            prompt=project.initial_prompt,
            html_code=bundle.project_files["index.html"],
            css_code=bundle.project_files["styles.css"],
            js_code=bundle.project_files["script.js"],
            preview_html=bundle.preview_files["/index.html"],
            log_messages=_default_logs(),
        )
    except Exception:
        project = db.get(Project, project_id)
        if project is not None:
            project.status = "failed"
            db.add(project)
            db.commit()
    finally:
        db.close()


def improve_project(db: Session, *, project: Project, instruction: str) -> Project:
    latest_version = get_latest_version(project)
    if latest_version is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="当前项目还没有可优化的页面版本。")

    project.status = "generating"
    db.add(project)
    db.commit()

    try:
        generator = _build_generator()
        website = generator.generate(_build_improvement_prompt(latest_version, instruction))
        bundle = generator.to_bundle(website)
        _persist_version(
            db,
            project=project,
            version_no=_next_version_number(db, project.id),
            prompt=instruction,
            html_code=bundle.project_files["index.html"],
            css_code=bundle.project_files["styles.css"],
            js_code=bundle.project_files["script.js"],
            preview_html=bundle.preview_files["/index.html"],
            log_messages=_default_logs(),
        )
    except Exception as exc:
        project.status = "failed"
        db.add(project)
        db.commit()
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return db.get(Project, project.id)


def get_project_for_user(db: Session, *, user_id: str, project_id: str) -> Project:
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在。")
    return project


def list_projects_for_user(db: Session, *, user_id: str) -> list[Project]:
    return db.query(Project).filter(Project.user_id == user_id).order_by(Project.updated_at.desc()).all()


def get_latest_version(project: Project) -> ProjectVersion | None:
    if not project.versions:
        return None
    return sorted(project.versions, key=lambda item: item.version_no)[-1]


def get_logs_for_version(version: ProjectVersion | None) -> list[str]:
    if version is None:
        return []
    ordered_logs = sorted(version.logs, key=lambda item: item.sort_order)
    return [item.message for item in ordered_logs]
