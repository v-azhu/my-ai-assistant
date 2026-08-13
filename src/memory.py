from typing import Dict, List, Optional

from config import config
from memory_backends import MemoryBackendError, get_memory_backend


class MemoryManager:
    """
    Thin wrapper around whichever memory backend is configured
    (local self-hosted Mem0, or Mem0 cloud — see memory_backends/).

    This is the only class the rest of the app (chat.py) talks to,
    so swapping MEMORY_BACKEND in .env never requires touching
    chat.py.

    Note: this app is currently single-user, so every call uses the
    same fixed user_id from config. If multi-user support is added
    later, thread a real per-session user_id through these methods
    instead.
    """

    def __init__(self):
        self.user_id = config.MEM0_USER_ID

    def add_memory(self, user_message: str, assistant_response: Optional[str] = None):
        """
        Hand a conversation turn to Mem0 and let it decide what (if
        anything) is worth remembering — this replaces the old
        keyword-based heuristic with Mem0's own LLM-based extraction.
        """
        messages = [{"role": "user", "content": user_message}]
        if assistant_response:
            messages.append({"role": "assistant", "content": assistant_response})

        try:
            get_memory_backend().add(messages, user_id=self.user_id)
        except MemoryBackendError as e:
            # Memory storage failing shouldn't break the conversation —
            # the user still gets a reply, they just won't be
            # remembered this turn.
            print(f"\n[Memory not saved: {e}]")

    def search_memory(self, query: str, top_k: int = None) -> List[Dict]:
        """Retrieve memories relevant to the query."""
        if top_k is None:
            top_k = config.MEMORY_TOP_K

        try:
            return get_memory_backend().search(query, user_id=self.user_id, limit=top_k)
        except MemoryBackendError:
            return []

    def get_all_memories(self) -> List[Dict]:
        """Return all stored memories for the current user."""
        try:
            return get_memory_backend().get_all(user_id=self.user_id)
        except MemoryBackendError:
            return []


memory_manager = MemoryManager()
