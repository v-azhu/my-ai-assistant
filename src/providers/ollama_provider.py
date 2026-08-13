from typing import Dict, List

import requests

from config import config
from providers.base import LLMError, LLMProvider


class OllamaProvider(LLMProvider):
    """
    LLMProvider backed by a locally running Ollama server.

    No API key required — Ollama runs entirely on your own machine.
    Requires the Ollama app/service to be installed and running
    (https://ollama.com), and the chosen model to be pulled first,
    e.g.:  ollama pull llama3.2
    """

    def __init__(self):
        self.base_url = config.OLLAMA_BASE_URL.rstrip("/")
        self.model = config.OLLAMA_MODEL
        self.temperature = config.OPENAI_TEMPERATURE

    def chat(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": self.temperature},
                },
                timeout=120,
            )
        except requests.exceptions.ConnectionError as e:
            raise LLMError(
                f"Could not connect to Ollama at {self.base_url}. "
                "Is the Ollama app/service running? "
                "Install it from https://ollama.com if you haven't."
            ) from e
        except requests.exceptions.Timeout as e:
            raise LLMError(
                "Ollama took too long to respond. The model may still "
                "be loading — try again in a moment."
            ) from e

        if response.status_code == 404:
            raise LLMError(
                f"Model '{self.model}' was not found locally. "
                f"Pull it first with: ollama pull {self.model}"
            )

        if response.status_code != 200:
            raise LLMError(
                f"Ollama returned an error (status {response.status_code}): "
                f"{response.text}"
            )

        data = response.json()
        content = data.get("message", {}).get("content")

        if not content:
            raise LLMError("Ollama returned an empty response.")

        return content
