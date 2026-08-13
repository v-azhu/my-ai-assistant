from providers.base import LLMError, LLMProvider

__all__ = ["LLMError", "LLMProvider", "get_llm_provider"]

_provider_instance = None


def get_llm_provider() -> LLMProvider:
    """
    Return a process-wide LLM provider instance, chosen by
    config.LLM_PROVIDER, creating it lazily on first use.

    This is the single place that knows which concrete provider
    classes exist. To add a new provider (e.g. Ollama), register it
    in _PROVIDER_REGISTRY below and implement a class with the same
    chat(messages) -> str interface as LLMProvider.
    """
    global _provider_instance
    if _provider_instance is None:
        _provider_instance = _create_provider()
    return _provider_instance


def _create_provider() -> LLMProvider:
    from config import config

    name = config.LLM_PROVIDER.lower()

    if name == "openai":
        from providers.openai_provider import OpenAIProvider
        return OpenAIProvider()

    if name == "anthropic":
        from providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider()

    if name == "ollama":
        from providers.ollama_provider import OllamaProvider
        return OllamaProvider()

    raise ValueError(
        f"Unknown LLM_PROVIDER '{config.LLM_PROVIDER}'. "
        f"Supported values: 'openai', 'anthropic', 'ollama'."
    )
