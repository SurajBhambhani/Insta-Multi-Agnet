from typing import Any, Optional

import requests

from ..utils.json_utils import load_json
from .settings import load_settings
from .. import models


GRAPH_BASE = "https://graph.facebook.com/v19.0"


def _get_instagram_settings() -> dict[str, Any]:
    settings = load_settings()
    return settings.get("instagram", {})


def _build_caption(item: models.ContentItem) -> str:
    captions = load_json(item.captions, {})
    hashtags = load_json(item.hashtags, [])

    lines = []
    if captions.get("en"):
        lines.append(captions.get("en"))
    if captions.get("de"):
        lines.append(captions.get("de"))
    if captions.get("hi"):
        lines.append(captions.get("hi"))

    tags = " ".join(hashtags)
    if tags:
        lines.append("")
        lines.append(tags)

    return "\n".join(lines).strip()


def validate_instagram_settings() -> tuple[bool, str, dict[str, Any]]:
    settings = _get_instagram_settings()
    access_token = str(settings.get("access_token", "")).strip()
    ig_user_id = str(settings.get("ig_user_id", "")).strip()

    if not access_token or not ig_user_id:
        return False, "Instagram access token and IG user id are required", settings

    return True, "ok", settings


def create_media_container(
    ig_user_id: str,
    access_token: str,
    media_url: str,
    caption: str,
) -> str:
    response = requests.post(
        f"{GRAPH_BASE}/{ig_user_id}/media",
        data={
            "image_url": media_url,
            "caption": caption,
            "access_token": access_token,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("id", "")


def publish_media(
    ig_user_id: str,
    access_token: str,
    creation_id: str,
) -> str:
    response = requests.post(
        f"{GRAPH_BASE}/{ig_user_id}/media_publish",
        data={
            "creation_id": creation_id,
            "access_token": access_token,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("id", "")


def publish_instagram_draft(
    item: models.ContentItem,
    media_url: str,
    dry_run_override: Optional[bool] = None,
) -> tuple[str, str, str, str]:
    valid, message, settings = validate_instagram_settings()
    if not valid:
        return "error", "", "", message

    access_token = str(settings.get("access_token", "")).strip()
    ig_user_id = str(settings.get("ig_user_id", "")).strip()
    dry_run = bool(settings.get("dry_run", True))
    if dry_run_override is not None:
        dry_run = dry_run_override

    caption = _build_caption(item)
    if dry_run:
        return "dry_run", "", "", "Dry run enabled, no post created"

    container_id = create_media_container(ig_user_id, access_token, media_url, caption)
    if not container_id:
        return "error", "", "", "Failed to create media container"

    post_id = publish_media(ig_user_id, access_token, container_id)
    if not post_id:
        return "error", "", container_id, "Failed to publish media"

    return "published", post_id, container_id, "Published"
