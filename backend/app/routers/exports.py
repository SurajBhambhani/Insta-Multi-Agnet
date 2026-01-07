from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.exporter import create_export
from ..services.serializers import export_out

router = APIRouter(prefix="/exports")


@router.post("", response_model=schemas.ExportOut)
def export_content(payload: schemas.ExportCreate, db: Session = Depends(get_db)):
    content_item = (
        db.query(models.ContentItem)
        .filter(models.ContentItem.id == payload.content_item_id)
        .first()
    )
    if not content_item:
        raise HTTPException(status_code=404, detail="Content item not found")

    project = (
        db.query(models.Project)
        .filter(models.Project.id == content_item.project_id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    decisions = (
        db.query(models.Decision)
        .filter(models.Decision.content_item_id == content_item.id)
        .all()
    )

    export = create_export(
        db,
        project,
        content_item,
        decisions,
        payload.format,
        payload.resolution,
    )
    return export_out(export)


@router.get("", response_model=list[schemas.ExportOut])
def list_exports(content_item_id: str, db: Session = Depends(get_db)):
    exports = (
        db.query(models.Export)
        .filter(models.Export.content_item_id == content_item_id)
        .all()
    )
    return [export_out(item) for item in exports]
