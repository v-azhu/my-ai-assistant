from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class MemoryBackendError(Exception):
    """Raised when a memory backend fails in a way the app can handle."""


class MemoryBackend(ABC):
    """
    Common interface every memory storage backend must implement.

    Mirrors the LLMProvider pattern in providers/base.py: keeping this
    interface tiny makes it cheap to move between a local, self-hosted
    Mem0 instance and Mem0's cloud platform (or any future backend)
    without touching chat.py or memory.py's public API.
    """

    @abstractmethod
    def add(self, messages: List[Dict[str, str]], user_id: str) -> None:
        """Store a conversation turn. The backend decides what, if
        anything, is worth remembering from it."""
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str, user_id: str, limit: int) -> List[Dict]:
        """Return up to `limit` memories relevant to `query`, each as
        a dict with at least a 'content' key."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self, user_id: str) -> List[Dict]:
        """Return every stored memory for this user."""
        raise NotImplementedError
