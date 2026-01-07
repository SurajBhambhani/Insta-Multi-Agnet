import json
from typing import Any


def load_json(raw: str, default: Any) -> Any:
    try:
        return json.loads(raw)
    except Exception:
        return default


def dump_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=True)
