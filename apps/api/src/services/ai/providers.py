from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class AIResponse:
    content: str
    usage: dict[str, int] | None = None
    model: str = ""
    finish_reason: str = "stop"


class AIProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def complete(self, prompt: str, **options: Any) -> AIResponse:
        pass

    @abstractmethod
    async def chat(self, messages: list[dict[str, str]], **options: Any) -> AIResponse:
        pass


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1"

    @property
    def name(self) -> str:
        return "openai"

    async def complete(self, prompt: str, **options: Any) -> AIResponse:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "max_tokens": options.get("max_tokens", 1000),
                    "temperature": options.get("temperature", 0.7),
                },
            )
            response.raise_for_status()
            data = response.json()
            return AIResponse(
                content=data["choices"][0]["text"],
                usage=data.get("usage"),
                model=self.model,
                finish_reason=data["choices"][0]["finish_reason"],
            )

    async def chat(self, messages: list[dict[str, str]], **options: Any) -> AIResponse:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": options.get("max_tokens", 1000),
                    "temperature": options.get("temperature", 0.7),
                },
            )
            response.raise_for_status()
            data = response.json()
            return AIResponse(
                content=data["choices"][0]["message"]["content"],
                usage=data.get("usage"),
                model=self.model,
                finish_reason=data["choices"][0]["finish_reason"],
            )


class AnthropicProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.anthropic.com/v1"

    @property
    def name(self) -> str:
        return "anthropic"

    async def complete(self, prompt: str, **options: Any) -> AIResponse:
        return await self.chat([{"role": "user", "content": prompt}], **options)

    async def chat(self, messages: list[dict[str, str]], **options: Any) -> AIResponse:
        system = options.pop("system", None)
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload: dict[str, Any] = {
                "model": self.model,
                "messages": messages,
                "max_tokens": options.get("max_tokens", 1000),
                "temperature": options.get("temperature", 0.7),
            }
            if system:
                payload["system"] = system
            response = await client.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return AIResponse(
                content=data["content"][0]["text"],
                usage={"total_tokens": data["usage"]["input_tokens"] + data["usage"]["output_tokens"]},
                model=self.model,
                finish_reason=data["stop_reason"],
            )


class GroqProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "mixtral-8x7b-32768"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"

    @property
    def name(self) -> str:
        return "groq"

    async def complete(self, prompt: str, **options: Any) -> AIResponse:
        return await self.chat([{"role": "user", "content": prompt}], **options)

    async def chat(self, messages: list[dict[str, str]], **options: Any) -> AIResponse:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": options.get("max_tokens", 1000),
                    "temperature": options.get("temperature", 0.7),
                },
            )
            response.raise_for_status()
            data = response.json()
            return AIResponse(
                content=data["choices"][0]["message"]["content"],
                usage=data.get("usage"),
                model=self.model,
                finish_reason=data["choices"][0]["finish_reason"],
            )


class OllamaProvider(AIProvider):
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model

    @property
    def name(self) -> str:
        return "ollama"

    async def complete(self, prompt: str, **options: Any) -> AIResponse:
        return await self.chat([{"role": "user", "content": prompt}], **options)

    async def chat(self, messages: list[dict[str, str]], **options: Any) -> AIResponse:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": options.get("temperature", 0.7),
                        "num_predict": options.get("max_tokens", 1000),
                    },
                },
            )
            response.raise_for_status()
            data = response.json()
            return AIResponse(
                content=data["message"]["content"],
                model=self.model,
                finish_reason=data.get("done_reason", "stop"),
            )


def get_provider(provider_type: str, **kwargs: Any) -> AIProvider:
    providers: dict[str, type[AIProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "groq": GroqProvider,
        "ollama": OllamaProvider,
    }
    if provider_type not in providers:
        raise ValueError(f"Unknown provider type: {provider_type}")
    return providers[provider_type](**kwargs)
