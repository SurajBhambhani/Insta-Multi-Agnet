from typing import Any

from .base import AgentResult
from ..services.llm import generate_json


def run_sound_agent(context: dict[str, Any]) -> AgentResult:
    fallback = {
        "sound_style": "cinematic chill",
        "tempo_bpm": 92,
        "trend_hint": "Use mellow electronic or indie instrumental",
    }
    prompt = (
        "You are a sound trend advisor. Suggest a sound style and tempo. "
        "Return ONLY valid JSON with keys: sound_style, tempo_bpm, trend_hint.\n\n"
        f"Context: {context}"
    )
    output = generate_json(prompt, fallback)
    return AgentResult(name="SoundTrendAgent", output=output, confidence=0.58)
