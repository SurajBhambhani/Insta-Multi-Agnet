from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.serializers import decision_out

router = APIRouter(prefix="/decisions")


@router.get("", response_model=list[schemas.DecisionOut])
def list_decisions(content_item_id: str, db: Session = Depends(get_db)):
    items = (
        db.query(models.Decision)
        .filter(models.Decision.content_item_id == content_item_id)
        .all()
    )
    return [decision_out(item) for item in items]
