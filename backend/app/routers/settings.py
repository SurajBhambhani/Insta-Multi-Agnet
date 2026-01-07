from fastapi import APIRouter

from .. import schemas
from ..services.settings import load_settings, save_settings

router = APIRouter(prefix="/settings")


@router.get("/llm", response_model=schemas.LLMSettingsOut)
def get_llm_settings():
    settings = load_settings()
    return schemas.LLMSettingsOut(
        llm_provider=str(settings.get("llm_provider", "stub")),
        openai_model=str(settings.get("openai_model", "gpt-4o-mini")),
    )


@router.post("/llm", response_model=schemas.LLMSettingsOut)
def set_llm_settings(payload: schemas.LLMSettingsIn):
    settings = save_settings(
        {
            "llm_provider": payload.provider,
            "openai_api_key": payload.api_key,
            "openai_model": payload.model,
        }
    )
    return schemas.LLMSettingsOut(
        llm_provider=str(settings.get("llm_provider", "stub")),
        openai_model=str(settings.get("openai_model", "gpt-4o-mini")),
    )
