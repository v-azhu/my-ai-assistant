from typing import Dict, List

from config import config
from memory_backends.base import MemoryBackend, MemoryBackendError
from memory_backends._utils import normalize_mem0_results


class LocalMemoryBackend(MemoryBackend):
    """
    Self-hosted Mem0, storing vectors in a local Chroma database and
    using a local Ollama model for both fact extraction and
    embeddings. No API key needed, no data leaves your machine.

    Requirements (see README/.env.example):
      - Ollama running locally
      - The chat model pulled (config.OLLAMA_MODEL)
      - An embedding model pulled, e.g.: ollama pull nomic-embed-text
    """

    def __init__(self):
        from mem0 import Memory  # imported lazily so mem0ai isn't
                                  # required unless this backend is used

        mem0_config = {
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": config.MEM0_COLLECTION_NAME,
                    "path": config.MEM0_VECTOR_STORE_PATH,
                },
            },
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": config.OLLAMA_MODEL,
                    "temperature": 0,
                    "max_tokens": 2000,
                    "ollama_base_url": config.OLLAMA_BASE_URL,
                },
            },
            "embedder": {
                "provider": "ollama",
                "config": {
                    "model": config.OLLAMA_EMBED_MODEL,
                    "ollama_base_url": config.OLLAMA_BASE_URL,
                },
            },
        }

        try:
            self.client = Memory.from_config(mem0_config)
        except Exception as e:
            raise MemoryBackendError(
                "Failed to initialize local Mem0 memory store. "
                "Make sure Ollama is running and both "
                f"'{config.OLLAMA_MODEL}' and '{config.OLLAMA_EMBED_MODEL}' "
                f"have been pulled (ollama pull {config.OLLAMA_EMBED_MODEL}). "
                f"Original error: {e}"
            ) from e

    def add(self, messages: List[Dict[str, str]], user_id: str) -> None:
        try:
            self.client.add(messages, user_id=user_id)
        except Exception as e:
            raise MemoryBackendError(f"Local Mem0 add() failed: {e}") from e

    def search(self, query: str, user_id: str, limit: int) -> List[Dict]:
        try:
            try:
                raw = self.client.search(
                    query, filters={"user_id": user_id}, limit=limit
                )
            except TypeError:
                # Older mem0 versions take user_id directly instead of
                # a filters dict.
                raw = self.client.search(query, user_id=user_id, limit=limit)
        except Exception as e:
            raise MemoryBackendError(f"Local Mem0 search() failed: {e}") from e

        return normalize_mem0_results(raw)

    def get_all(self, user_id: str) -> List[Dict]:
        try:
            try:
                raw = self.client.get_all(filters={"user_id": user_id})
            except TypeError:
                raw = self.client.get_all(user_id=user_id)
        except Exception as e:
            raise MemoryBackendError(f"Local Mem0 get_all() failed: {e}") from e

        return normalize_mem0_results(raw)
