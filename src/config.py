import os
from dotenv import load_dotenv

load_dotenv()

# Some systems have an HTTP(S)_PROXY set (VPN clients, corporate
# networks, security software) that intercepts even localhost
# traffic, causing local Ollama calls to fail with a 502 from the
# proxy rather than a normal connection error. Ollama's own server
# always runs on localhost, so it's always safe to exclude it from
# proxying. setdefault() won't override anything the user has
# explicitly configured.
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")
os.environ.setdefault("no_proxy", "localhost,127.0.0.1")

# Optional: route outbound calls to cloud providers (OpenAI,
# Anthropic, Groq) through a local proxy — needed on networks where
# those domains aren't directly reachable (e.g. behind a v2ray/Clash
# client). Leave HTTPS_PROXY unset in .env if you don't need this.
# This never affects local Ollama traffic, which is always excluded
# via NO_PROXY above regardless of this setting.
_https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
if _https_proxy:
    os.environ.setdefault("HTTPS_PROXY", _https_proxy)
    os.environ.setdefault("https_proxy", _https_proxy)

_http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
if _http_proxy:
    os.environ.setdefault("HTTP_PROXY", _http_proxy)
    os.environ.setdefault("http_proxy", _http_proxy)

# Mem0 phones home anonymous usage stats via PostHog by default. This
# has nothing to do with your OpenAI/Anthropic/Groq calls, and on a
# network that needs a proxy for outbound traffic (see above), the
# PostHog call can time out and print a noisy — but harmless —
# traceback. Disabling it removes both the noise and the network call.
# Must be set before mem0 is imported, so this needs to stay in
# config.py (imported first by every module that uses Mem0).
os.environ.setdefault("MEM0_TELEMETRY", "False")

SUPPORTED_PROVIDERS = ("openai", "anthropic", "ollama", "groq")


class Config:
    """
    Application configuration.

    All configuration values are loaded from environment
    variables (via a .env file). See .env.example for the
    full list of supported variables.
    """

    # --- Which LLM backend to use ---
    # "openai" or "anthropic". Only the settings for the selected
    # provider need to be filled in.
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

    # --- OpenAI ---
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # --- Anthropic (Claude) ---
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

    # --- Groq (free, no credit card, hosted open-weight models) ---
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    # --- Ollama (local, free, no API key needed) ---
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    # Separate embedding model used by the local Mem0 backend (chat
    # models like llama3.2/gemma don't produce embeddings).
    OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    # Model used internally by Mem0 to decide what's worth
    # remembering from each turn. This runs as an *extra* LLM call on
    # every message, on top of your normal chat reply — defaulting it
    # to a small, fast model keeps that overhead low even if your main
    # chat model (OLLAMA_MODEL) is large and CPU-bound. Falls back to
    # OLLAMA_MODEL if not set.
    OLLAMA_MEMORY_MODEL = os.getenv("OLLAMA_MEMORY_MODEL", "") or OLLAMA_MODEL

    # --- Memory (Mem0) backend ---
    # "local" (self-hosted, free, via Ollama + Chroma) or "cloud"
    # (Mem0 Platform, needs MEM0_API_KEY).
    MEMORY_BACKEND = os.getenv("MEMORY_BACKEND", "local")
    MEM0_API_KEY = os.getenv("MEM0_API_KEY")
    MEM0_USER_ID = os.getenv("MEM0_USER_ID", "default_user")
    MEM0_VECTOR_STORE_PATH = os.getenv("MEM0_VECTOR_STORE_PATH", "./mem0_data")
    MEM0_COLLECTION_NAME = os.getenv("MEM0_COLLECTION_NAME", "my_ai_assistant_memories")

    # --- Shared generation settings ---
    # (Applied to whichever provider is active.)
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))

    # --- Conversation ---
    # How many previous turns (user+assistant pairs) to keep
    # in the prompt sent to the LLM. Keeps token usage bounded.
    MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS", "10"))

    # --- Memory layer ---
    # How many relevant memories to retrieve per turn.
    MEMORY_TOP_K = int(os.getenv("MEMORY_TOP_K", "3"))

    @classmethod
    def validate(cls):
        """
        Validate required configuration at startup.

        Raises:
            ValueError: if a required setting is missing or invalid.
        """
        errors = []

        provider = cls.LLM_PROVIDER.lower()
        if provider not in SUPPORTED_PROVIDERS:
            errors.append(
                f"LLM_PROVIDER '{cls.LLM_PROVIDER}' is not supported. "
                f"Choose one of: {', '.join(SUPPORTED_PROVIDERS)}."
            )
        elif provider == "openai" and not cls.OPENAI_API_KEY:
            errors.append(
                "LLM_PROVIDER is 'openai' but OPENAI_API_KEY is not set."
            )
        elif provider == "anthropic" and not cls.ANTHROPIC_API_KEY:
            errors.append(
                "LLM_PROVIDER is 'anthropic' but ANTHROPIC_API_KEY is not set."
            )
        elif provider == "ollama" and not cls.OLLAMA_MODEL:
            errors.append(
                "LLM_PROVIDER is 'ollama' but OLLAMA_MODEL is not set."
            )
            # Note: we don't check here whether the Ollama server is
            # actually running / reachable — that's a connection
            # issue surfaced clearly by OllamaProvider.chat() instead,
            # since it can change after startup (e.g. service stops).
        elif provider == "groq" and not cls.GROQ_API_KEY:
            errors.append(
                "LLM_PROVIDER is 'groq' but GROQ_API_KEY is not set. "
                "Get a free key at https://console.groq.com/keys."
            )

        if cls.OPENAI_TEMPERATURE < 0 or cls.OPENAI_TEMPERATURE > 2:
            errors.append("OPENAI_TEMPERATURE must be between 0 and 2.")

        if cls.OPENAI_MAX_TOKENS <= 0:
            errors.append("OPENAI_MAX_TOKENS must be a positive integer.")

        memory_backend = cls.MEMORY_BACKEND.lower()
        if memory_backend not in ("local", "cloud"):
            errors.append(
                f"MEMORY_BACKEND '{cls.MEMORY_BACKEND}' is not supported. "
                f"Choose one of: local, cloud."
            )
        elif memory_backend == "cloud" and not cls.MEM0_API_KEY:
            errors.append(
                "MEMORY_BACKEND is 'cloud' but MEM0_API_KEY is not set. "
                "Get one at https://app.mem0.ai."
            )
            # Note: for MEMORY_BACKEND=local, we don't verify here that
            # Ollama is running or that OLLAMA_EMBED_MODEL has been
            # pulled — that's surfaced clearly by LocalMemoryBackend
            # when it actually tries to connect.

        if errors:
            raise ValueError(
                "Invalid configuration:\n- " + "\n- ".join(errors)
            )


config = Config()
