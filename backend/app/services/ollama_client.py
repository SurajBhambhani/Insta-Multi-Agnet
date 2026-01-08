import logging
from typing import Optional

import requests
from requests.exceptions import RequestException

logger = logging.getLogger("ollama_client")


def query_ollama(
    prompt: str,
    host: str,
    model: str,
    temperature: float,
) -> Optional[str]:
    try:
        url = f"{host.rstrip('/')}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            return None
        message = choices[0].get("message", {})
        content = message.get("content", "").strip()
        logger.info("+ Ollama request succeeded")
        return content
    except RequestException:
        logger.warning("- Ollama request failed (network)")
        return None
    except Exception:
        logger.warning("- Ollama request failed")
        return None
