from abc import ABC, abstractmethod
from typing import Any, Literal, TypedDict


class CallResult(TypedDict):
    answer: Any
    reasoning: str | None
    max_tokens: int | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None


class Base_api_caller(ABC):
    name: str  # Registry-Name

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
        self.setup()

    def setup(self) -> None:
        pass  # if needed

    @abstractmethod
    def call_api(self, prompt: str) -> CallResult: ...
