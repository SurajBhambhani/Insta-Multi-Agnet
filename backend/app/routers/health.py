from fastapi import APIRouter

from .. import schemas

router = APIRouter()


@router.get("/health", response_model=schemas.Health)
def health() -> schemas.Health:
    return schemas.Health(status="ok", version="0.1.0")
