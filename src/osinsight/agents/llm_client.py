from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
try:
    from openai import OpenAI
except ImportError:  # Optional until an online LLM call is requested.
    OpenAI = None  # type: ignore[assignment,misc]


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    model: str
    base_url: str | None = None
    timeout: float = 60.0
    max_retries: int = 2

    @classmethod
    def from_env(cls) -> "LLMConfig":
        load_dotenv()
        api_key = os.getenv("LLM_API_KEY", "").strip()
        model = os.getenv("LLM_MODEL", "").strip()
        if not api_key:
            raise ValueError("LLM_API_KEY is not configured")
        if not model:
            raise ValueError("LLM_MODEL is not configured")
        return cls(
            api_key=api_key,
            model=model,
            base_url=os.getenv("LLM_BASE_URL") or None,
            timeout=float(os.getenv("LLM_TIMEOUT", "60")),
            max_retries=int(os.getenv("LLM_MAX_RETRIES", "2")),
        )


class LLMClient:
    """Single OpenAI-compatible entry point for all agent model calls."""

    def __init__(self, config: LLMConfig):
        if OpenAI is None:
            raise RuntimeError("Install project dependencies before creating an LLMClient")
        client_args: dict[str, Any] = {
            "api_key": config.api_key,
            "timeout": config.timeout,
            "max_retries": 0,
        }
        if config.base_url:
            client_args["base_url"] = config.base_url
        self._client = OpenAI(**client_args)
        self.config = config

    def ask(self, prompt: str, *, system: str | None = None, temperature: float = 0.0) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        last_error: Exception | None = None
        for attempt in range(self.config.max_retries + 1):
            try:
                response = self._client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    temperature=temperature,
                )
                content = response.choices[0].message.content
                if not content:
                    raise RuntimeError("LLM returned an empty response")
                return content
            except Exception as error:
                last_error = error
                if attempt < self.config.max_retries:
                    time.sleep(2**attempt)
        raise RuntimeError("LLM request failed after retries") from last_error

