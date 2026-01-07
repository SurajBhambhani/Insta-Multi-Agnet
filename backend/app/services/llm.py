import os
from typing import Any

from .settings import load_settings


def _resolve_openai_key() -> str:
    env_key = os.getenv("OPENAI_API_KEY", "").strip()
    if env_key:
        return env_key
    settings = load_settings()
    return str(settings.get("openai_api_key", "")).strip()


def _resolve_openai_model() -> str:
    env_model = os.getenv("OPENAI_MODEL", "").strip()
    if env_model:
        return env_model
    settings = load_settings()
    return str(settings.get("openai_model", "gpt-4o-mini")).strip()


def generate_text(prompt: str, fallback: str) -> str:
    api_key = _resolve_openai_key()
    if not api_key:
        return fallback

    try:
        from openai import OpenAI
    except Exception:
        return fallback

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=_resolve_openai_model(),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        content = response.choices[0].message.content
        return (content or fallback).strip()
    except Exception:
        return fallback


def generate_json(prompt: str, fallback: dict[str, Any]) -> dict[str, Any]:
    text = generate_text(prompt, "")
    if not text:
        return fallback
    try:
        import json

        return json.loads(text)
    except Exception:
        return fallback
