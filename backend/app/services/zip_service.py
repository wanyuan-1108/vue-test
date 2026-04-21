from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app.core.config import get_settings


def build_zip_bytes(files: dict[str, str]) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as zip_file:
        for filename, content in files.items():
            zip_file.writestr(filename, content)
    buffer.seek(0)
    return buffer.read()


def write_zip_file(*, project_id: str, version_no: int, files: dict[str, str]) -> Path:
    settings = get_settings()
    output_dir = settings.zip_output_path / project_id
    output_dir.mkdir(parents=True, exist_ok=True)

    zip_path = output_dir / f"designgen-v{version_no}.zip"
    zip_path.write_bytes(build_zip_bytes(files))
    return zip_path
