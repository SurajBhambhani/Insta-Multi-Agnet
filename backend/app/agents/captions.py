from typing import Any

from .base import AgentResult
from ..services.llm import generate_json


def run_caption_agent(context: dict[str, Any]) -> AgentResult:
    fallback = {
        "captions": {
            "en": "A quick guide to a perfect travel day. Save this for later.",
            "de": "Ein kurzer Guide für den perfekten Reisetag. Speichern.",
            "hi": "परफेक्ट ट्रैवल डे का छोटा गाइड। सेव कर लो।",
        },
        "cta": "Save for your next trip",
        "hashtags": [
            "#travel",
            "#lifestyle",
            "#cityguide",
            "#wanderlust",
            "#travelgram",
            "#instatravel",
            "#discoverearth",
            "#vacation",
        ],
    }
    prompt = (
        "You are a multilingual travel copywriter. Create captions in EN/DE/HI and 6 hashtags. "
        "Return ONLY valid JSON with keys: captions (object), cta, hashtags (array).\n\n"
        f"Context: {context}"
    )
    output = generate_json(prompt, fallback)
    return AgentResult(name="CaptionAgent", output=output, confidence=0.74)
