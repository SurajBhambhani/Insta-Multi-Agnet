import csv
from pathlib import Path
from typing import Any

from fastapi import UploadFile

from ..config import TREND_PACK_DIR, ensure_dirs


def _pack_path(project_id: str) -> Path:
    return TREND_PACK_DIR / project_id / "trend_pack.csv"


def save_trend_pack(project_id: str, upload: UploadFile) -> list[dict[str, Any]]:
    ensure_dirs()
    pack_dir = TREND_PACK_DIR / project_id
    pack_dir.mkdir(parents=True, exist_ok=True)
    pack_path = _pack_path(project_id)
    with pack_path.open("wb") as out_file:
        out_file.write(upload.file.read())
    return load_trend_pack(project_id)


def load_trend_pack(project_id: str) -> list[dict[str, Any]]:
    pack_path = _pack_path(project_id)
    if not pack_path.exists():
        return []

    with pack_path.open("r", encoding="utf-8", errors="ignore") as handle:
        reader = csv.DictReader(handle)
        items: list[dict[str, Any]] = []
        for row in reader:
            normalized = {key.strip().lower(): value.strip() for key, value in row.items()}
            items.append(normalized)
        return items
