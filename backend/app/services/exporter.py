import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.orm import Session

from .. import models
from ..config import PROJECTS_DIR
from ..utils.json_utils import dump_json, load_json


DEFAULT_PREVIEW_SIZE = (1080, 1920)


def _parse_resolution(value: str) -> tuple[int, int]:
    try:
        width, height = value.lower().split("x", maxsplit=1)
        return int(width), int(height)
    except Exception:
        return DEFAULT_PREVIEW_SIZE


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _render_preview(path: Path, title: str, resolution: str) -> None:
    size = _parse_resolution(resolution)
    image = Image.new("RGB", size, color=(248, 243, 236))
    draw = ImageDraw.Draw(image)
    text = f"Preview\n{title}\n{resolution}"
    draw.multiline_text((40, 60), text, fill=(30, 27, 22))
    image.save(path, format="JPEG")


def _extract_decision_payloads(decisions: list[models.Decision]) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for decision in decisions:
        payloads.append(
            {
                "agent": decision.agent,
                "confidence": decision.confidence,
                "output": load_json(decision.decision, {}),
                "rationale": decision.rationale,
                "created_at": decision.created_at,
            }
        )
    return payloads


def _find_sound(decision_payloads: list[dict[str, Any]]) -> dict[str, Any]:
    for payload in decision_payloads:
        if payload.get("agent") == "SoundTrendAgent":
            return payload.get("output", {})
    return {}


def create_export(
    db: Session,
    project: models.Project,
    content_item: models.ContentItem,
    decisions: list[models.Decision],
    export_format: str,
    resolution: str,
) -> models.Export:
    export_id = models._uuid()
    export_dir = (
        PROJECTS_DIR
        / project.id
        / "exports"
        / content_item.id
        / export_id
    )
    export_dir.mkdir(parents=True, exist_ok=True)

    captions = load_json(content_item.captions, {})
    hashtags = load_json(content_item.hashtags, [])
    on_screen = load_json(content_item.on_screen_text, {})

    decision_payloads = _extract_decision_payloads(decisions)
    sound = _find_sound(decision_payloads)

    metadata = {
        "project_id": project.id,
        "project_name": project.name,
        "content_item_id": content_item.id,
        "format": content_item.format,
        "status": content_item.status,
        "captions": captions,
        "hashtags": hashtags,
        "on_screen_text": on_screen,
        "storyboard": content_item.storyboard,
        "sound": sound,
        "decisions": decision_payloads,
        "export": {
            "format": export_format,
            "resolution": resolution,
        },
    }

    _write_text(export_dir / "metadata.json", json.dumps(metadata, indent=2))
    _write_text(
        export_dir / "caption.md",
        "# Instagram Draft\n\n"
        f"## EN\n{captions.get('en', '')}\n\n"
        f"## DE\n{captions.get('de', '')}\n\n"
        f"## HI\n{captions.get('hi', '')}\n",
    )
    _write_text(export_dir / "hashtags.txt", "\n".join(hashtags))
    _write_text(export_dir / "storyboard.md", content_item.storyboard or "")
    _write_text(export_dir / "decision_log.json", json.dumps(decision_payloads, indent=2))
    _render_preview(export_dir / "preview.jpg", project.name, resolution)

    export = models.Export(
        id=export_id,
        content_item_id=content_item.id,
        export_path=str(export_dir),
        format=export_format,
        specs=dump_json({"resolution": resolution}),
    )
    db.add(export)
    db.commit()
    db.refresh(export)
    return export
