from abc import ABC, abstractmethod
from typing import Dict, List


class LLMError(Exception):
    """Raised when a provider fails in a way the app can handle
    (rate limit, network issue, auth error, etc.)."""


class LLMProvider(ABC):
    """
    Common interface every LLM backend must implement.

    Keeping this interface tiny (one method) makes it cheap to add
    new providers (Ollama, Gemini, ...) without touching chat.py or
    main.py at all.
    """

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Send a conversation to the model and return its reply.

        Args:
            messages: list of {"role": "system"/"user"/"assistant",
                                "content": str}, in OpenAI-style format.
                       Each provider is responsible for translating
                       this into whatever shape its own API expects.

        Returns:
            The assistant's reply text.

        Raises:
            LLMError: on any recoverable provider-side failure.
        """
        raise NotImplementedError
