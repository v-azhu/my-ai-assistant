from typing import Dict, List

from config import config
from memory import memory_manager
from providers import get_llm_provider

SYSTEM_PROMPT = (
    "You are a helpful personal AI assistant with long-term memory. "
    "Use the user's stored memories (if any are provided below) to "
    "personalize your answers, but don't force them into the "
    "conversation if they aren't relevant. Be direct and honest "
    "rather than simply agreeable."
)


class ChatManager:
    """
    Conversation management layer.

    Responsible for connecting: User -> Memory -> LLM -> Memory.
    Talks to the LLM only through the LLMProvider interface, so it
    doesn't know or care whether OpenAI, Anthropic, or something
    else is answering (see config.LLM_PROVIDER / providers/).
    """

    def __init__(self):
        self.history: List[Dict[str, str]] = []

    def send_message(self, user_message: str) -> str:
        """
        Process one conversation turn and return the assistant's reply.

        Raises:
            LLMError: if the active provider fails in a handled way
                (rate limit, connection issue, API error).
        """
        user_message = user_message.strip()

        # 1. Retrieve relevant memories. Memory retrieval failing
        #    should degrade the conversation, not break it.
        try:
            memories = memory_manager.search_memory(user_message)
        except Exception:
            memories = []

        # 2. Build the full message list: system + memory context
        #    + recent history + the new user message.
        messages = [{"role": "system", "content": self._build_system_prompt(memories)}]

        recent_history = self.history[-config.MAX_HISTORY_TURNS:]
        for turn in recent_history:
            messages.append({"role": "user", "content": turn["user"]})
            messages.append({"role": "assistant", "content": turn["assistant"]})

        messages.append({"role": "user", "content": user_message})

        # 3. Call whichever LLM provider is currently configured.
        response = get_llm_provider().chat(messages)

        # 4. Store the turn in short-term history.
        self.history.append({"user": user_message, "assistant": response})

        # 5. Hand the turn to Mem0 — it decides what's worth
        #    remembering, so we no longer need a keyword heuristic here.
        memory_manager.add_memory(user_message, response)

        return response

    @staticmethod
    def _build_system_prompt(memories: List[Dict]) -> str:
        if not memories:
            return SYSTEM_PROMPT

        memory_lines = "\n".join(f"- {m['content']}" for m in memories)
        return f"{SYSTEM_PROMPT}\n\nRelevant memories about the user:\n{memory_lines}"


chat_manager = ChatManager()
