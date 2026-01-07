from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.assets import ingest_uploads
from ..services.serializers import asset_out

router = APIRouter(prefix="/assets")


@router.post("/ingest", response_model=schemas.IngestResponse)
async def ingest_assets(
    project_id: str = Form(...),
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    created, skipped = ingest_uploads(project_id, files, db)
    return schemas.IngestResponse(
        assets=[asset_out(asset) for asset in created],
        skipped=skipped,
    )


@router.get("", response_model=list[schemas.AssetOut])
def list_assets(project_id: str, db: Session = Depends(get_db)):
    assets = db.query(models.Asset).filter(models.Asset.project_id == project_id).all()
    return [asset_out(asset) for asset in assets]
