import shutil
from pathlib import Path
from typing import Iterable

from fastapi import UploadFile
from PIL import Image
from sqlalchemy.orm import Session

from ..config import PROJECTS_DIR
from .. import models
from ..utils.json_utils import dump_json

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".avi", ".mkv"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".webp"}


def asset_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in VIDEO_EXTS:
        return "video"
    if ext in IMAGE_EXTS:
        return "photo"
    return "unknown"


def image_resolution(path: Path) -> str:
    try:
        with Image.open(path) as img:
            return f"{img.width}x{img.height}"
    except Exception:
        return ""


def ingest_uploads(
    project_id: str,
    files: Iterable[UploadFile],
    db: Session,
) -> tuple[list[models.Asset], list[str]]:
    project_dir = PROJECTS_DIR / project_id / "assets"
    project_dir.mkdir(parents=True, exist_ok=True)

    created: list[models.Asset] = []
    skipped: list[str] = []

    for upload in files:
        filename = Path(upload.filename or "")
        if not filename.name:
            skipped.append("unnamed")
            continue

        dest_path = project_dir / filename.name
        with dest_path.open("wb") as out_file:
            shutil.copyfileobj(upload.file, out_file)

        kind = asset_type(dest_path)
        if kind == "unknown":
            skipped.append(filename.name)
            dest_path.unlink(missing_ok=True)
            continue

        resolution = ""
        if kind == "photo":
            resolution = image_resolution(dest_path)

        metadata = {
            "original_name": filename.name,
            "size_bytes": dest_path.stat().st_size,
            "content_type": upload.content_type or "",
        }

        asset = models.Asset(
            project_id=project_id,
            path=str(dest_path),
            type=kind,
            duration=0.0,
            resolution=resolution,
            metadata_json=dump_json(metadata),
            quality_scores=dump_json({"lighting": 0, "shaky": 0}),
            tags=dump_json([]),
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)
        created.append(asset)

    return created, skipped
