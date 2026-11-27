"""Fábrica de provedores de LLM."""

from app.core.config import settings
from .base import LLMProvider
from .mock import MockLLMProvider


def get_llm_provider() -> LLMProvider:
    """
    Retorna a implementação do provedor de LLM configurada.

    Atualmente só o mock está implementado.
    Futuramente suportará OpenAI, Anthropic, Ollama, etc.
    """
    provider_name = settings.llm_provider.lower()

    if provider_name == "mock":
        return MockLLMProvider()

    # Placeholder para futuros provedores
    # if provider_name == "openai":
    #     return OpenAIProvider(...)
    # if provider_name == "ollama":
    #     return OllamaProvider(...)

    # Fallback seguro
    return MockLLMProvider()
