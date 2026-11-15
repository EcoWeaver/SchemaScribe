import json
from pathlib import Path
from typing import Any

import litellm
from pydantic import BaseModel

class litellm_API_daller:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        temperature: float = 0.7, 
        max_tokens: int | None = None, 
        top_p: float | None = None,
        compatibility: bool | None  = None, 
        **extra_params: Any,
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.extra_params = extra_params
        self.compatibility = compatibility
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

    def llm_call(
        self,
        prompt: str, 
        files: list[Path] | None = None,
        schema: list[Path] | None = None,  
    ) -> dict[str, Any]:
    
        #Fusion of the prompt, schema, and data
        parts = [prompt]
        for p in schema or []:
            parts.append(f"--- Datei: {p.name} ---\n{p.read_text(encoding='utf-8')}")
        for p in files or []:
            parts.append(f"--- Datei: {p.name} ---\n{p.read_text(encoding='utf-8')}")

        # provider prefix: None = OpenAI, True = Anthropic, False = Gemini
        provider = {None: "openai", True: "anthropic", False: "gemini"}[self.compatibility]
        
        #call API via LiteLLM 
        response = litellm.completion(
            model=f"{provider}/{self.model}",
            api_base=self.base_url,
            api_key=self.api_key,
            messages=[{"role": "user", "content": "\n\n".join(parts)}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            **self.extra_params,
        )

        # returning answer as jason 
        msg = response.choices[0].message
        usage = response.usage
        content = msg.content or ""
        try:
            answer = json.loads(content)
        except json.JSONDecodeError:
            answer = content
        return {
            "answer": answer,
            "reasoning": getattr(msg, "reasoning_content", None),
            "max_tokens": self.max_tokens,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        }