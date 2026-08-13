from typing import Dict, List

from config import config
from memory_backends.base import MemoryBackend, MemoryBackendError
from memory_backends._utils import normalize_mem0_results


class CloudMemoryBackend(MemoryBackend):
    """
    Mem0 Platform (cloud-hosted). Requires a Mem0 account and API key
    from https://app.mem0.ai — memories are stored on Mem0's servers
    rather than locally.
    """

    def __init__(self):
        from mem0 import MemoryClient  # imported lazily, same reason
                                        # as in local_backend.py

        if not config.MEM0_API_KEY:
            raise ValueError(
                "MEM0_API_KEY is missing. Get one at https://app.mem0.ai "
                "and set it in your .env file, or switch "
                "MEMORY_BACKEND to 'local' in .env."
            )

        self.client = MemoryClient(api_key=config.MEM0_API_KEY)

    def add(self, messages: List[Dict[str, str]], user_id: str) -> None:
        try:
            self.client.add(messages, user_id=user_id)
        except Exception as e:
            raise MemoryBackendError(f"Mem0 cloud add() failed: {e}") from e

    def search(self, query: str, user_id: str, limit: int) -> List[Dict]:
        try:
            try:
                raw = self.client.search(
                    query, filters={"user_id": user_id}, limit=limit
                )
            except TypeError:
                raw = self.client.search(query, user_id=user_id, limit=limit)
        except Exception as e:
            raise MemoryBackendError(f"Mem0 cloud search() failed: {e}") from e

        return normalize_mem0_results(raw)

    def get_all(self, user_id: str) -> List[Dict]:
        try:
            try:
                raw = self.client.get_all(filters={"user_id": user_id})
            except TypeError:
                raw = self.client.get_all(user_id=user_id)
        except Exception as e:
            raise MemoryBackendError(f"Mem0 cloud get_all() failed: {e}") from e

        return normalize_mem0_results(raw)
