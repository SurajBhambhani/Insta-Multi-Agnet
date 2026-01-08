from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.trend_pack import load_trend_pack, save_trend_pack

router = APIRouter(prefix="/trend-pack")


@router.post("", response_model=schemas.TrendPackOut)
async def upload_trend_pack(
    project_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        return schemas.TrendPackOut(items=[], count=0)

    items = save_trend_pack(project_id, file)
    return schemas.TrendPackOut(items=items, count=len(items))


@router.get("", response_model=schemas.TrendPackOut)
def get_trend_pack(project_id: str, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        return schemas.TrendPackOut(items=[], count=0)

    items = load_trend_pack(project_id)
    return schemas.TrendPackOut(items=items, count=len(items))
