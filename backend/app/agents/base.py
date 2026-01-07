from dataclasses import dataclass
from typing import Any


@dataclass
class AgentResult:
    name: str
    output: dict[str, Any]
    confidence: float
