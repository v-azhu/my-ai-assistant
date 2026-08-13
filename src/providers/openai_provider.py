from typing import Dict, List

from openai import OpenAI, APIConnectionError, APIError, RateLimitError

from config import config
from providers.base import LLMError, LLMProvider


class OpenAIProvider(LLMProvider):
    """LLMProvider backed by the OpenAI Chat Completions API."""

    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is missing. "
                "Please set it in your .env file, or switch "
                "LLM_PROVIDER to 'anthropic' in .env."
            )

        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
        self.temperature = config.OPENAI_TEMPERATURE
        self.max_tokens = config.OPENAI_MAX_TOKENS

    def chat(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
        except RateLimitError as e:
            raise LLMError(
                "OpenAI rate limit or quota reached. "
                "Check your usage at platform.openai.com/usage, "
                "or switch LLM_PROVIDER to 'anthropic' in .env."
            ) from e
        except APIConnectionError as e:
            raise LLMError(
                "Could not connect to the OpenAI API. "
                "Check your network connection."
            ) from e
        except APIError as e:
            raise LLMError(f"OpenAI API error: {e}") from e

        content = response.choices[0].message.content
        if content is None:
            raise LLMError("The model returned an empty response.")

        return content
