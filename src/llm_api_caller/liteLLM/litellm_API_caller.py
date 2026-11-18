import json
from pathlib import Path
from typing import Any, Literal

import litellm


class litellm_API_caller:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        temperature: float,
        timeout: int,
        max_retries: int,
        max_tokens: int | None = None,
        top_p: float | None = None,
        provider: Literal["openai", "anthropic", "gemini"] = "openai",
        **extra_params: Any,
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.extra_params = extra_params
        self.provider = provider
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.timeout = timeout
        self.max_retries = max_retries

    def llm_call(
        self,
        prompt: str,
        files: dict[str, str],
        schema: list[Path] | None = None,  # make it required
    ) -> dict[str, Any]:

        # Fusion of the prompt, schema, and data
        parts = [prompt]
        for p in schema or []:
            parts.append(f"--- Datei: {p.name} ---\n{p.read_text(encoding='utf-8')}")
            # Add extracted Markdown content directly
        for filename, content in (files or {}).items():
            parts.append(f"--- Datei: {filename} ---\n{content}")

        # call API via LiteLLM
        response = litellm.completion(
            model=f"{self.provider}/{self.model}",
            api_base=self.base_url,
            api_key=self.api_key,
            messages=[{"role": "user", "content": "\n\n".join(parts)}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            timeout=self.timeout,
            stream=True,
            max_retries=self.max_retries,
            **self.extra_params,
        )
        # Stream einsammeln
        content_parts: list[str] = []
        reasoning_parts: list[str] = []
        usage = None

        for chunk in response:  # bei dir heißt die Variable "response", nicht "stream"
            if chunk.choices:
                delta = chunk.choices[0].delta
                if getattr(delta, "content", None):
                    content_parts.append(delta.content)
                if getattr(delta, "reasoning_content", None):
                    reasoning_parts.append(delta.reasoning_content)
            if getattr(chunk, "usage", None):
                usage = chunk.usage

        content = "".join(content_parts)
        reasoning = "".join(reasoning_parts) or None

        # Antwort als JSON zurückgeben
        try:
            answer = json.loads(content)
        except json.JSONDecodeError:
            answer = content

        return {
            "answer": answer,
            "reasoning": reasoning,
            "max_tokens": self.max_tokens,
            "prompt_tokens": getattr(usage, "prompt_tokens", None),
            "completion_tokens": getattr(usage, "completion_tokens", None),
            "total_tokens": getattr(usage, "total_tokens", None),
        }
