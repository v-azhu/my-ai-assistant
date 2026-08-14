from typing import Dict, List

from openai import OpenAI, APIConnectionError, APIError, RateLimitError

from config import config
from providers.base import LLMError, LLMProvider

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


class GroqProvider(LLMProvider):
    """
    LLMProvider backed by Groq's hosted open-weight models
    (Llama, GPT-OSS, Qwen, etc.) running on their LPU hardware.

    Groq's API is OpenAI-compatible, so this reuses the official
    OpenAI SDK and just points it at Groq's base URL instead of
    writing a separate HTTP client from scratch.

    Free tier: no credit card required, rate-limited (not a
    one-time token grant) — see https://console.groq.com.
    """

    def __init__(self):
        if not config.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is missing. Get a free key (no credit "
                "card needed) at https://console.groq.com/keys and "
                "set it in your .env file, or switch LLM_PROVIDER "
                "to something else."
            )

        self.client = OpenAI(api_key=config.GROQ_API_KEY, base_url=GROQ_BASE_URL)
        self.model = config.GROQ_MODEL
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
                "Groq rate limit reached (free tier: 30 requests/min, "
                "14,400/day). Wait a bit and try again, or switch to "
                "another LLM_PROVIDER in .env."
            ) from e
        except APIConnectionError as e:
            raise LLMError(
                "Could not connect to Groq's API. "
                "Check your network connection."
            ) from e
        except APIError as e:
            raise LLMError(f"Groq API error: {e}") from e

        content = response.choices[0].message.content
        if content is None:
            raise LLMError("The model returned an empty response.")

        return content
