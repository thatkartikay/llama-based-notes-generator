from __future__ import annotations

import json
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from study_notes.config import OllamaSettings


class OllamaClient:
    def __init__(self, settings: OllamaSettings):
        self.settings = settings

    def complete(self, prompt: str) -> str:
        url = f"{self.settings.base_url.rstrip('/')}/api/generate"
        payload = {
            "model": self.settings.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": self.settings.temperature},
        }
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=600) as response:
                data = json.loads(response.read().decode("utf-8"))
        except URLError as exc:
            raise RuntimeError(
                "Could not connect to Ollama. Install Ollama, run it, and pull the selected model."
            ) from exc

        if "response" not in data:
            raise RuntimeError(f"Ollama returned an unexpected response: {data}")
        return data["response"]


def parse_json_response(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if "```" in text:
        text = text.replace("```json", "```")
        parts = text.split("```")
        text = max(parts, key=len).strip()

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("The model did not return JSON. Try again or use a stronger model.")

    return json.loads(text[start : end + 1])

