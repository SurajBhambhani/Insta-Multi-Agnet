from typing import Any

from .base import AgentResult
from ..services.llm import generate_json


def run_reel_agent(context: dict[str, Any]) -> AgentResult:
    fallback = {
        "hook": "48 hours here — the spots everyone misses.",
        "storyboard": [
            "Quick establishing shot",
            "Hero moment",
            "Detail close-ups",
            "Call-to-action",
        ],
        "on_screen_text": ["48 hours here", "Save this"],
    }
    prompt = (
        "You are a travel reel director. Create a short reel plan. "
        "Return ONLY valid JSON with keys: hook, storyboard (array), on_screen_text (array).\n\n"
        f"Context: {context}"
    )
    output = generate_json(prompt, fallback)
    return AgentResult(name="ReelAgent", output=output, confidence=0.7)
