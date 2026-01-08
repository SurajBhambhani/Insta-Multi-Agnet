from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.instagram import publish_instagram_draft
from ..services.settings import load_settings, update_instagram_settings

router = APIRouter(prefix="/instagram")


@router.get("/settings", response_model=schemas.InstagramSettingsOut)
def get_instagram_settings():
    settings = load_settings().get("instagram", {})
    ig_user_id = str(settings.get("ig_user_id", "")).strip()
    configured = bool(ig_user_id and str(settings.get("access_token", "")).strip())
    return schemas.InstagramSettingsOut(
        configured=configured,
        ig_user_id=ig_user_id,
        dry_run=bool(settings.get("dry_run", True)),
    )


@router.post("/settings", response_model=schemas.InstagramSettingsOut)
def set_instagram_settings(payload: schemas.InstagramSettingsIn):
    settings = update_instagram_settings(
        {
            "access_token": payload.access_token,
            "ig_user_id": payload.ig_user_id,
            "app_id": payload.app_id or "",
            "app_secret": payload.app_secret or "",
            "dry_run": payload.dry_run,
        }
    )
    instagram = settings.get("instagram", {})
    ig_user_id = str(instagram.get("ig_user_id", "")).strip()
    configured = bool(ig_user_id and str(instagram.get("access_token", "")).strip())
    return schemas.InstagramSettingsOut(
        configured=configured,
        ig_user_id=ig_user_id,
        dry_run=bool(instagram.get("dry_run", True)),
    )


@router.post("/publish", response_model=schemas.InstagramPublishOut)
def publish_instagram(payload: schemas.InstagramPublishIn, db: Session = Depends(get_db)):
    content_item = (
        db.query(models.ContentItem)
        .filter(models.ContentItem.id == payload.content_item_id)
        .first()
    )
    if not content_item:
        raise HTTPException(status_code=404, detail="Content item not found")

    status, post_id, container_id, message = publish_instagram_draft(
        content_item,
        payload.media_url,
        dry_run_override=payload.dry_run,
    )

    if status == "error":
        raise HTTPException(status_code=400, detail=message)

    return schemas.InstagramPublishOut(
        status=status,
        post_id=post_id or None,
        container_id=container_id or None,
        message=message,
        used_media_url=payload.media_url,
    )
