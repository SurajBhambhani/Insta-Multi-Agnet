import copy
import json
from typing import Any

from ..config import SETTINGS_PATH, ensure_dirs

DEFAULT_SETTINGS = {
    "llm_provider": "stub",
    "openai_api_key": "",
    "openai_model": "gpt-4o-mini",
    "instagram": {
        "access_token": "",
        "ig_user_id": "",
        "app_id": "",
        "app_secret": "",
        "dry_run": True,
    },
    "ollama": {
        "enabled": False,
        "host": "http://127.0.0.1:11434",
        "model": "llama3",
        "temperature": 0.7,
    },
}


def _merge_nested(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = base.copy()
    merged.update(override or {})
    return merged


def load_settings() -> dict[str, Any]:
    ensure_dirs()
    if not SETTINGS_PATH.exists():
        return copy.deepcopy(DEFAULT_SETTINGS)
    try:
        raw = json.loads(SETTINGS_PATH.read_text())
        settings = copy.deepcopy(DEFAULT_SETTINGS)
        settings.update(raw or {})
        settings["instagram"] = _merge_nested(
            DEFAULT_SETTINGS["instagram"], raw.get("instagram", {})
        )
        settings["ollama"] = _merge_nested(
            DEFAULT_SETTINGS["ollama"], raw.get("ollama", {})
        )
        return settings
    except Exception:
        return copy.deepcopy(DEFAULT_SETTINGS)


def save_settings(payload: dict[str, Any]) -> dict[str, Any]:
    ensure_dirs()
    settings = load_settings()
    if "provider" in payload:
        settings["llm_provider"] = payload["provider"]
    if "api_key" in payload:
        settings["openai_api_key"] = str(payload["api_key"]).strip()
    if "model" in payload:
        settings["openai_model"] = str(payload["model"]).strip()
    ollama = settings.get("ollama", {}).copy()
    if "ollama_enabled" in payload:
        ollama["enabled"] = bool(payload["ollama_enabled"])
    if "ollama_host" in payload:
        ollama["host"] = str(payload["ollama_host"]).strip()
    if "ollama_model" in payload:
        ollama["model"] = str(payload["ollama_model"]).strip()
    if "ollama_temperature" in payload:
        ollama["temperature"] = float(payload["ollama_temperature"])
    settings["ollama"] = ollama
    SETTINGS_PATH.write_text(json.dumps(settings, ensure_ascii=True, indent=2))
    return settings


def update_instagram_settings(payload: dict[str, Any]) -> dict[str, Any]:
    settings = load_settings()
    instagram = settings.get("instagram", {}).copy()
    instagram.update(payload)
    settings["instagram"] = instagram
    SETTINGS_PATH.write_text(json.dumps(settings, ensure_ascii=True, indent=2))
    return settings
