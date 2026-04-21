from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import Project, User
from app.schemas.project import (
    ProjectCreateRequest,
    ProjectImproveRequest,
    ProjectResponse,
    ProjectSummaryResponse,
    ProjectVersionResponse,
)
from app.services.project_service import (
    create_project_shell,
    get_latest_version,
    get_logs_for_version,
    get_project_for_user,
    get_status_logs,
    improve_project,
    list_projects_for_user,
    run_generation_for_project,
)


router = APIRouter(prefix="/projects", tags=["projects"])


def _serialize_project(project: Project) -> ProjectResponse:
    latest_version = get_latest_version(project)
    if latest_version is None:
        return ProjectResponse(
            id=project.id,
            title=project.title,
            status=project.status,
            initial_prompt=project.initial_prompt,
            created_at=project.created_at,
            updated_at=project.updated_at,
            logs=get_status_logs(project.status),
            latest_version=None,
            download_url=None,
        )

    return ProjectResponse(
        id=project.id,
        title=project.title,
        status=project.status,
        initial_prompt=project.initial_prompt,
        created_at=project.created_at,
        updated_at=project.updated_at,
        logs=get_logs_for_version(latest_version),
        latest_version=ProjectVersionResponse(
            id=latest_version.id,
            version_no=latest_version.version_no,
            prompt=latest_version.prompt,
            files={
                "index.html": latest_version.html_code,
                "styles.css": latest_version.css_code,
                "script.js": latest_version.js_code,
            },
            preview_html=latest_version.preview_html,
            created_at=latest_version.created_at,
        ),
        download_url=f"/api/projects/{project.id}/download" if latest_version.zip_path else None,
    )


@router.get("", response_model=list[ProjectSummaryResponse])
def list_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = list_projects_for_user(db, user_id=current_user.id)
    return [
        ProjectSummaryResponse(
            id=project.id,
            title=project.title,
            status=project.status,
            initial_prompt=project.initial_prompt,
            updated_at=project.updated_at,
        )
        for project in projects
    ]


@router.post("", response_model=ProjectResponse)
def create(
    payload: ProjectCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = create_project_shell(db, user=current_user, prompt=payload.prompt)
    background_tasks.add_task(run_generation_for_project, project.id)
    return _serialize_project(project)


@router.get("/{project_id}", response_model=ProjectResponse)
def detail(project_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = get_project_for_user(db, user_id=current_user.id, project_id=project_id)
    return _serialize_project(project)


@router.post("/{project_id}/improve", response_model=ProjectResponse)
def improve(
    project_id: str,
    payload: ProjectImproveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = get_project_for_user(db, user_id=current_user.id, project_id=project_id)
    project = improve_project(db, project=project, instruction=payload.prompt)
    return _serialize_project(project)


@router.get("/{project_id}/download")
def download(project_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = get_project_for_user(db, user_id=current_user.id, project_id=project_id)
    latest_version = get_latest_version(project)
    if latest_version is None or not latest_version.zip_path:
        raise HTTPException(status_code=404, detail="当前项目还没有可下载的源码。")

    file_path = Path(latest_version.zip_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="源码压缩包不存在。")

    return FileResponse(path=file_path, filename=file_path.name, media_type="application/zip")
