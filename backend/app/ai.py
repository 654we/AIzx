from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import httpx


class AIProvider(Protocol):
    def generate(self, prompt: str) -> str:
        ...


@dataclass
class ProviderConfig:
    api_key: str
    base_url: str
    model: str


class OpenAICompatProvider:
    def __init__(self, config: ProviderConfig):
        self.config = config

    def generate(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.config.api_key}"}
        payload = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = httpx.post(
            f"{self.config.base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json=payload,
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


class DeepSeekProvider(OpenAICompatProvider):
    pass


class GLMProvider(OpenAICompatProvider):
    pass
