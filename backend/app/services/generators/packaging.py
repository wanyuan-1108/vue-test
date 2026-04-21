from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app.core.config import get_settings
from app.schemas.design import GeneratedBundle


def write_bundle_zip(task_id: str, bundle: GeneratedBundle) -> Path:
    settings = get_settings()
    output_dir = settings.zip_output_path
    output_dir.mkdir(parents=True, exist_ok=True)

    task_dir = output_dir / task_id
    task_dir.mkdir(parents=True, exist_ok=True)

    zip_path = task_dir / "designgen-export.zip"
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as archive:
        for relative_path, content in bundle.project_files.items():
            archive.writestr(relative_path, content)

    return zip_path
