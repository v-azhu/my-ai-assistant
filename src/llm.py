from typing import Dict, List

from openai import OpenAI, APIConnectionError, APIError, RateLimitError

from config import config


class LLMError(Exception):
    """Raised when the LLM provider fails in a way the app can handle."""


class LLMClient:
    """
    Wrapper around an LLM provider (currently OpenAI).

    The rest of the application talks to this class only through
    `chat()`, so swapping providers (e.g. adding Ollama) later only
    requires a new class with the same interface.
    """

    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is missing. "
                "Please set it in your .env file."
            )

        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
        self.temperature = config.OPENAI_TEMPERATURE
        self.max_tokens = config.OPENAI_MAX_TOKENS

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Send a list of chat messages to the LLM and return the reply.

        Args:
            messages: list of {"role": "system"/"user"/"assistant",
                                "content": str}

        Returns:
            The assistant's reply text.

        Raises:
            LLMError: on any recoverable provider-side failure
                (rate limit, connection issue, API error).
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        except RateLimitError as e:
            raise LLMError(
                "Rate limit reached. Please wait a moment and try again."
            ) from e
        except APIConnectionError as e:
            raise LLMError(
                "Could not connect to the OpenAI API. "
                "Check your network connection."
            ) from e
        except APIError as e:
            raise LLMError(f"OpenAI API error: {e}") from e

        choice = response.choices[0]
        content = choice.message.content

        if content is None:
            raise LLMError("The model returned an empty response.")

        return content


# Lazily created so importing this module (e.g. in tests) doesn't
# require a valid API key to already be configured.
_llm_client = None


def get_llm_client() -> LLMClient:
    """Return a process-wide LLMClient instance, creating it on first use."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
