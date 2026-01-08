from .. import schemas
from .. import models
from ..utils.json_utils import load_json


def project_out(project: models.Project) -> schemas.ProjectOut:
    return schemas.ProjectOut(
        id=project.id,
        name=project.name,
        created_at=project.created_at,
        languages=load_json(project.languages, []),
        tone_profile=load_json(project.tone_profile, {}),
        privacy_settings=load_json(project.privacy_settings, {}),
    )


def asset_out(asset: models.Asset) -> schemas.AssetOut:
    return schemas.AssetOut(
        id=asset.id,
        project_id=asset.project_id,
        path=asset.path,
        type=asset.type,
        duration=asset.duration,
        resolution=asset.resolution,
        metadata=load_json(asset.metadata_json, {}),
        quality_scores=load_json(asset.quality_scores, {}),
        tags=load_json(asset.tags, []),
    )


def content_out(item: models.ContentItem) -> schemas.ContentItemOut:
    return schemas.ContentItemOut(
        id=item.id,
        project_id=item.project_id,
        concept_id=item.concept_id,
        format=item.format,
        status=item.status,
        captions=load_json(item.captions, {}),
        hashtags=load_json(item.hashtags, []),
        on_screen_text=load_json(item.on_screen_text, {}),
        sound_id=item.sound_id,
        storyboard=item.storyboard,
        compliance_notes=item.compliance_notes,
        created_at=item.created_at,
    )


def decision_out(item: models.Decision) -> schemas.DecisionOut:
    return schemas.DecisionOut(
        id=item.id,
        content_item_id=item.content_item_id,
        agent=item.agent,
        decision=load_json(item.decision, {}),
        rationale=item.rationale,
        confidence=item.confidence,
        created_at=item.created_at,
    )


def export_out(item: models.Export) -> schemas.ExportOut:
    return schemas.ExportOut(
        id=item.id,
        content_item_id=item.content_item_id,
        export_path=item.export_path,
        format=item.format,
        specs=load_json(item.specs, {}),
        created_at=item.created_at,
    )


def mcp_message_out(item: models.AgentMessage) -> schemas.MCPMessageOut:
    return schemas.MCPMessageOut(
        id=item.id,
        thread_id=item.thread_id,
        sender=item.sender,
        recipient=item.recipient,
        message=load_json(item.message, {}),
        confidence=item.confidence,
        citations=load_json(item.citations, []),
        created_at=item.created_at,
    )
