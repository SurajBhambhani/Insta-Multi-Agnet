from typing import Any

from .base import AgentResult
from ..services.llm import generate_json


def run_location_agent(context: dict[str, Any]) -> AgentResult:
    fallback = {
        "location_hint": "Unknown",
        "key_questions": [
            "Where is this location and why is it special?",
            "What is the best time to visit?",
            "How do you get here and what should you budget?",
            "What local experience makes this unique?",
        ],
    }
    prompt = (
        "You are a travel content analyst. Given the asset context below, "
        "infer a likely location hint and list 4 key audience questions. "
        "Return ONLY valid JSON with keys: location_hint, key_questions.\n\n"
        f"Context: {context}"
    )
    output = generate_json(prompt, fallback)
    return AgentResult(name="LocationAgent", output=output, confidence=0.62)
