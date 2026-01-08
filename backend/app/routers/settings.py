from fastapi import APIRouter

from .. import schemas
from ..services.settings import load_settings, save_settings

router = APIRouter(prefix="/settings")


@router.get("/llm", response_model=schemas.LLMSettingsOut)
def get_llm_settings():
    settings = load_settings()
    ollama = settings.get("ollama", {})
    return schemas.LLMSettingsOut(
        llm_provider=str(settings.get("llm_provider", "stub")),
        openai_model=str(settings.get("openai_model", "gpt-4o-mini")),
        ollama_enabled=bool(ollama.get("enabled", False)),
        ollama_model=str(ollama.get("model", "llama3")),
        ollama_host=str(ollama.get("host", "http://127.0.0.1:11434")),
        ollama_temperature=float(ollama.get("temperature", 0.7)),
    )


@router.post("/llm", response_model=schemas.LLMSettingsOut)
def set_llm_settings(payload: schemas.LLMSettingsIn):
    settings = save_settings(
        {
            "provider": payload.provider,
            "api_key": payload.api_key,
            "model": payload.model,
            "ollama_enabled": payload.ollama_enabled,
            "ollama_model": payload.ollama_model,
            "ollama_host": payload.ollama_host,
            "ollama_temperature": payload.ollama_temperature,
        }
    )
    ollama = settings.get("ollama", {})
    return schemas.LLMSettingsOut(
        llm_provider=str(settings.get("llm_provider", "stub")),
        openai_model=str(settings.get("openai_model", "gpt-4o-mini")),
        ollama_enabled=bool(ollama.get("enabled", False)),
        ollama_model=str(ollama.get("model", "llama3")),
        ollama_host=str(ollama.get("host", "http://127.0.0.1:11434")),
        ollama_temperature=float(ollama.get("temperature", 0.7)),
    )
