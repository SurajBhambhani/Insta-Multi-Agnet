from fastapi import APIRouter, Depends, HTTPException

from .. import schemas
from ..services import ollama_client
from ..services.settings import load_settings

router = APIRouter(prefix="/ollama")


@router.post("/chat", response_model=schemas.OllamaChatOut)
def chat(payload: schemas.OllamaChatIn):
    settings = load_settings()
    ollama = settings.get("ollama", {})

    if not ollama.get("enabled"):
        raise HTTPException(status_code=503, detail="Ollama provider is disabled")

    response = ollama_client.query_ollama(
        payload.prompt,
        host=ollama.get("host", "http://127.0.0.1:11434"),
        model=ollama.get("model", "llama3"),
        temperature=float(ollama.get("temperature", 0.7)),
    )
    if response is None:
        raise HTTPException(status_code=502, detail="Ollama query failed")

    return schemas.OllamaChatOut(response=response)
