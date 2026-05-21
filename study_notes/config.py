from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OllamaSettings:
    model: str = "llama3.1:8b"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.25


@dataclass
class AppSettings:
    ollama: OllamaSettings = field(default_factory=OllamaSettings)

