from typing import Any

from sqlalchemy.orm import Session

from .. import models
from ..agents import (
    run_caption_agent,
    run_location_agent,
    run_reel_agent,
    run_sound_agent,
)
from ..utils.json_utils import dump_json, load_json
from .. import schemas
from .mcp_bus import list_messages, publish_message, serialize_messages


def _build_context(project: models.Project, asset: models.Asset, thread_id: str) -> dict[str, Any]:
    return {
        "project_name": project.name,
        "languages": load_json(project.languages, []),
        "tone_profile": load_json(project.tone_profile, {}),
        "privacy_settings": load_json(project.privacy_settings, {}),
        "mcp_thread_id": thread_id,
        "mcp_messages": [],
        "asset": {
            "type": asset.type,
            "resolution": asset.resolution,
            "path": asset.path.split("/")[-1],
        },
    }


DEFAULT_BANNED_HASHTAGS = {
    "#follow4follow",
    "#like4like",
    "#f4f",
    "#l4l",
}

DEFAULT_HASHTAGS = [
    "#travel",
    "#lifestyle",
    "#cityguide",
    "#wanderlust",
    "#travelgram",
    "#instatravel",
    "#discoverearth",
    "#vacation",
]


def _normalize_hashtags(tags: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        cleaned = tag.strip()
        if not cleaned:
            continue
        if not cleaned.startswith("#"):
            cleaned = f"#{cleaned}"
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(cleaned)
    return normalized


def _apply_hashtag_rules(tags: list[str]) -> list[str]:
    filtered = [tag for tag in tags if tag.lower() not in DEFAULT_BANNED_HASHTAGS]
    filtered = _normalize_hashtags(filtered)
    if len(filtered) < 8:
        filtered = _normalize_hashtags(filtered + DEFAULT_HASHTAGS)
    if len(filtered) > 20:
        filtered = filtered[:20]
    return filtered


def _record_decision(
    db: Session,
    content_item_id: str,
    agent_name: str,
    output: dict[str, Any],
    confidence: float,
) -> None:
    decision = models.Decision(
        content_item_id=content_item_id,
        agent=agent_name,
        decision=dump_json(output),
        rationale="auto-generated",
        confidence=confidence,
    )
    db.add(decision)


def _publish_event(
    db: Session,
    thread_id: str,
    sender: str,
    recipient: str,
    message: dict[str, Any],
    confidence: float,
) -> None:
    payload = schemas.MCPMessageIn(
        thread_id=thread_id,
        sender=sender,
        recipient=recipient,
        message=message,
        confidence=confidence,
        citations=[],
    )
    publish_message(db, payload)


def _refresh_mcp_context(db: Session, thread_id: str, context: dict[str, Any]) -> None:
    messages = list_messages(db, thread_id=thread_id)
    context["mcp_messages"] = serialize_messages(messages)


def run_pipeline_for_asset(
    project: models.Project,
    asset: models.Asset,
    db: Session,
) -> models.ContentItem:
    item = models.ContentItem(
        project_id=project.id,
        format="reel",
        status="draft",
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    thread_id = item.id
    context = _build_context(project, asset, thread_id)
    _publish_event(
        db,
        thread_id,
        sender="Orchestrator",
        recipient="broadcast",
        message={"event": "pipeline_start", "asset_id": asset.id},
        confidence=1.0,
    )
    _refresh_mcp_context(db, thread_id, context)

    location = run_location_agent(context)
    _publish_event(
        db,
        thread_id,
        sender=location.name,
        recipient="broadcast",
        message=location.output,
        confidence=location.confidence,
    )
    _refresh_mcp_context(db, thread_id, context)

    sound = run_sound_agent(context)
    _publish_event(
        db,
        thread_id,
        sender=sound.name,
        recipient="broadcast",
        message=sound.output,
        confidence=sound.confidence,
    )
    _refresh_mcp_context(db, thread_id, context)

    reel = run_reel_agent(context)
    _publish_event(
        db,
        thread_id,
        sender=reel.name,
        recipient="broadcast",
        message=reel.output,
        confidence=reel.confidence,
    )
    _refresh_mcp_context(db, thread_id, context)

    captions = run_caption_agent(context)
    _publish_event(
        db,
        thread_id,
        sender=captions.name,
        recipient="broadcast",
        message=captions.output,
        confidence=captions.confidence,
    )
    _refresh_mcp_context(db, thread_id, context)

    captions_out = captions.output.get("captions", {})
    hashtags_out = captions.output.get("hashtags", [])
    on_screen = reel.output.get("on_screen_text", [])
    storyboard = " -> ".join(reel.output.get("storyboard", []))
    hashtags_final = _apply_hashtag_rules([str(tag) for tag in hashtags_out])

    item.captions = dump_json(captions_out)
    item.hashtags = dump_json(hashtags_final)
    item.on_screen_text = dump_json({"en": " | ".join(on_screen)})
    item.storyboard = storyboard
    item.compliance_notes = "Generated by multi-agent pipeline"
    db.add(item)
    db.commit()
    db.refresh(item)

    for result in (location, sound, reel, captions):
        _record_decision(db, item.id, result.name, result.output, result.confidence)

    _publish_event(
        db,
        thread_id,
        sender="Orchestrator",
        recipient="broadcast",
        message={"event": "pipeline_complete", "content_item_id": item.id},
        confidence=1.0,
    )
    db.commit()
    return item
