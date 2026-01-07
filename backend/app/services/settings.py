import json
from typing import Any

from ..config import SETTINGS_PATH, ensure_dirs

DEFAULT_SETTINGS = {
    "llm_provider": "stub",
    "openai_api_key": "",
    "openai_model": "gpt-4o-mini",
}


def load_settings() -> dict[str, Any]:
    ensure_dirs()
    if not SETTINGS_PATH.exists():
        return DEFAULT_SETTINGS.copy()
    try:
        return json.loads(SETTINGS_PATH.read_text())
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(payload: dict[str, Any]) -> dict[str, Any]:
    ensure_dirs()
    settings = DEFAULT_SETTINGS.copy()
    settings.update(payload)
    SETTINGS_PATH.write_text(json.dumps(settings, ensure_ascii=True, indent=2))
    return settings
