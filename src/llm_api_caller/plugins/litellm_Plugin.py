import json

import litellm

from llm_api_caller import Base_api_caller, CallResult, register


@register("litellm")
class LiteLLM_Plugin(Base_api_caller):
    def call_api(self, prompt: str) -> CallResult:  # call API via LiteLLM

        response = litellm.completion(
            model=f"{self.provider}/{self.model}",
            api_base=self.base_url,
            api_key=self.api_key,
            messages=[{"role": "user", "content": "\n\n".join(prompt)}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            timeout=self.timeout,
            stream=True,
            num_retries=self.max_retries,
            stream_options={"include_usage": True},
            **self.extra_params,
        )
        content_parts: list[str] = []
        reasoning_parts: list[str] = []
        usage = None

        for chunk in response:
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
