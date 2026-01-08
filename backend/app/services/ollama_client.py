import requests
from requests.exceptions import RequestException
from typing import Optional


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
        return message.get("content", "").strip()
    except RequestException:
        return None
    except Exception:
        return None
