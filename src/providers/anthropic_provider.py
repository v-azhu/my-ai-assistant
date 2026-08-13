from typing import Dict, List

import anthropic

from config import config
from providers.base import LLMError, LLMProvider


class AnthropicProvider(LLMProvider):
    """
    LLMProvider backed by the Anthropic Messages API (Claude).

    Anthropic's API takes the system prompt as a separate top-level
    argument rather than as a message with role "system", so this
    class splits the incoming OpenAI-style messages list accordingly.
    """

    def __init__(self):
        if not config.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY is missing. "
                "Please set it in your .env file, or switch "
                "LLM_PROVIDER to 'openai' in .env."
            )

        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = config.ANTHROPIC_MODEL
        self.temperature = config.OPENAI_TEMPERATURE
        self.max_tokens = config.OPENAI_MAX_TOKENS

    def chat(self, messages: List[Dict[str, str]]) -> str:
        system_prompt, conversation = self._split_system_message(messages)

        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=conversation,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        except anthropic.RateLimitError as e:
            raise LLMError(
                "Anthropic rate limit or quota reached. "
                "Check your usage at console.anthropic.com, "
                "or switch LLM_PROVIDER to 'openai' in .env."
            ) from e
        except anthropic.APIConnectionError as e:
            raise LLMError(
                "Could not connect to the Anthropic API. "
                "Check your network connection."
            ) from e
        except anthropic.APIError as e:
            raise LLMError(f"Anthropic API error: {e}") from e

        if not response.content:
            raise LLMError("The model returned an empty response.")

        # response.content is a list of content blocks; concatenate
        # any text blocks to build the final reply.
        text_parts = [
            block.text for block in response.content
            if getattr(block, "type", None) == "text"
        ]
        return "".join(text_parts)

    @staticmethod
    def _split_system_message(messages: List[Dict[str, str]]):
        """
        Anthropic wants system instructions separately from the
        user/assistant turns. Pull out any role="system" messages
        (there should only be one, from chat.py) and pass the rest
        through unchanged.
        """
        system_parts = [m["content"] for m in messages if m["role"] == "system"]
        conversation = [m for m in messages if m["role"] != "system"]
        system_prompt = "\n\n".join(system_parts) if system_parts else None
        return system_prompt, conversation
