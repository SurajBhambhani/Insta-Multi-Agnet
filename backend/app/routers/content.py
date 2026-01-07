from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.serializers import content_out
from ..utils.json_utils import dump_json
from ..services.orchestrator import run_pipeline_for_asset

router = APIRouter(prefix="/content")


@router.post("", response_model=schemas.ContentItemOut)
def create_content(payload: schemas.ContentItemCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    item = models.ContentItem(
        project_id=payload.project_id,
        format=payload.format,
        status=payload.status,
        captions=dump_json(payload.captions),
        hashtags=dump_json(payload.hashtags),
        on_screen_text=dump_json(payload.on_screen_text),
        storyboard=payload.storyboard,
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return content_out(item)


@router.post("/generate", response_model=schemas.ContentItemOut)
def generate_content(payload: schemas.GenerateDraftIn, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    asset = (
        db.query(models.Asset)
        .filter(
            models.Asset.id == payload.asset_id,
            models.Asset.project_id == payload.project_id,
        )
        .first()
    )
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    item = run_pipeline_for_asset(project, asset, db)
    return content_out(item)


@router.get("", response_model=list[schemas.ContentItemOut])
def list_content(project_id: str, db: Session = Depends(get_db)):
    items = db.query(models.ContentItem).filter(models.ContentItem.project_id == project_id).all()
    return [content_out(item) for item in items]
