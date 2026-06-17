import json
import time
import threading
import logging
from enum import Enum
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class ProviderType(Enum):
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


CANONICAL_MODELS = {
    ProviderType.GEMINI: {"fast": "gemini-2.5-flash-lite", "accurate": "gemini-2.5-flash"},
    ProviderType.ANTHROPIC: {"fast": "claude-haiku-4-5-20251001", "accurate": "claude-sonnet-4-6"},
    ProviderType.OPENAI: {"fast": "gpt-4o-mini", "accurate": "gpt-4o"},
}


def detect_provider(api_key: str) -> ProviderType:
    key = api_key.strip()
    if key.startswith("AIza"):
        return ProviderType.GEMINI
    if key.startswith("sk-ant"):
        return ProviderType.ANTHROPIC
    if key.startswith("sk-"):
        return ProviderType.OPENAI
    raise ValueError(f"No se pudo detectar el proveedor para la API key: {key[:10]}...")


def resolve_model(model: str, provider: ProviderType) -> str:
    canonical = CANONICAL_MODELS.get(provider, {})
    return canonical.get(model, model)


class _TPMTracker:
    def __init__(self, window: int = 60, limit: int = 600_000):
        self._lock = threading.Lock()
        self._tokens: list[tuple[float, int]] = []
        self._window = window
        self._limit = limit

    def track(self, estimated_tokens: int):
        with self._lock:
            now = time.time()
            self._tokens = [(t, c) for t, c in self._tokens if now - t < self._window]
            window_tokens = sum(c for _, c in self._tokens)
            if window_tokens + estimated_tokens > self._limit:
                sleep_time = self._window - (now - self._tokens[0][0]) if self._tokens else 1
                logger.warning(
                    "TPM limit approaching (%d/%d), sleeping %.1fs",
                    window_tokens, self._limit, sleep_time,
                )
                time.sleep(min(sleep_time, 5))
            self._tokens.append((time.time(), estimated_tokens))


class ModelClient(ABC):
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._provider = detect_provider(api_key)
        self._tpm = _TPMTracker()

    @property
    def provider(self) -> ProviderType:
        return self._provider

    def track_tpm(self, estimated_tokens: int):
        self._tpm.track(estimated_tokens)

    @abstractmethod
    def generate(
        self,
        contents: str,
        system_prompt: str | None = None,
        schema: dict | None = None,
        model: str = "fast",
        config: dict | None = None,
    ) -> str:
        ...


class GeminiClient(ModelClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        from google import genai
        self._client = genai.Client(api_key=api_key)

    def generate(
        self,
        contents: str,
        system_prompt: str | None = None,
        schema: dict | None = None,
        model: str = "fast",
        config: dict | None = None,
    ) -> str:
        model_name = resolve_model(model, ProviderType.GEMINI)
        cfg = {"temperature": 0.1, **(config or {})}
        if schema:
            cfg["response_mime_type"] = "application/json"
        if system_prompt:
            cfg["system_instruction"] = system_prompt
        response = self._client.models.generate_content(
            model=model_name,
            contents=contents,
            config=cfg,
        )
        return response.text.strip()


class AnthropicClient(ModelClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        import anthropic
        self._client = anthropic.Anthropic(api_key=api_key)

    def generate(
        self,
        contents: str,
        system_prompt: str | None = None,
        schema: dict | None = None,
        model: str = "fast",
        config: dict | None = None,
    ) -> str:
        model_name = resolve_model(model, ProviderType.ANTHROPIC)
        kwargs: dict[str, Any] = {
            "model": model_name,
            "max_tokens": (config or {}).get("max_output_tokens", 8192),
            "messages": [{"role": "user", "content": contents}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        if schema:
            kwargs["tools"] = [{
                "name": "extract_data",
                "description": "Extract structured data matching the provided schema",
                "input_schema": schema,
            }]
            kwargs["tool_choice"] = {"type": "tool", "name": "extract_data"}
        response = self._client.messages.create(**kwargs)
        if schema and response.stop_reason == "tool_use":
            for block in response.content:
                if hasattr(block, 'type') and block.type == 'tool_use':
                    return json.dumps(block.input)
        return response.content[0].text if response.content else ""


class OpenAIClient(ModelClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        from openai import OpenAI
        self._client = OpenAI(api_key=api_key)

    def generate(
        self,
        contents: str,
        system_prompt: str | None = None,
        schema: dict | None = None,
        model: str = "fast",
        config: dict | None = None,
    ) -> str:
        model_name = resolve_model(model, ProviderType.OPENAI)
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": contents})
        kwargs: dict[str, Any] = {
            "model": model_name,
            "messages": messages,
            "temperature": (config or {}).get("temperature", 0.1),
        }
        if schema:
            kwargs["response_format"] = {"type": "json_object"}
        if config and "max_output_tokens" in config:
            kwargs["max_tokens"] = config["max_output_tokens"]
        response = self._client.chat.completions.create(**kwargs)
        return response.choices[0].message.content.strip()


_client_cache: dict[str, ModelClient] = {}


def get_client(api_key: str) -> ModelClient:
    if api_key not in _client_cache:
        provider = detect_provider(api_key)
        if provider == ProviderType.GEMINI:
            _client_cache[api_key] = GeminiClient(api_key)
        elif provider == ProviderType.ANTHROPIC:
            _client_cache[api_key] = AnthropicClient(api_key)
        elif provider == ProviderType.OPENAI:
            _client_cache[api_key] = OpenAIClient(api_key)
    return _client_cache[api_key]


def resolve_api_key(settings: Any) -> str:
    if getattr(settings, 'llm_api_key', None):
        return settings.llm_api_key
    if getattr(settings, 'google_api_key', None):
        return settings.google_api_key
    if getattr(settings, 'anthropic_api_key', None):
        return settings.anthropic_api_key
    if getattr(settings, 'openai_api_key', None):
        return settings.openai_api_key
    raise ValueError(
        "No LLM API key configured. Set LLM_API_KEY, GOOGLE_API_KEY, "
        "ANTHROPIC_API_KEY, or OPENAI_API_KEY in your .env"
    )
