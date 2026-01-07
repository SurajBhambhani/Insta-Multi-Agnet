from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_db
from ..services.serializers import project_out
from ..utils.json_utils import dump_json
from ..config import PROJECTS_DIR

router = APIRouter(prefix="/projects")


@router.post("", response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    project = models.Project(
        name=payload.name,
        languages=dump_json(payload.languages),
        tone_profile=dump_json(payload.tone_profile),
        privacy_settings=dump_json(payload.privacy_settings),
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    (PROJECTS_DIR / project.id).mkdir(parents=True, exist_ok=True)
    return project_out(project)


@router.get("", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    return [project_out(p) for p in projects]


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_out(project)
