from openai import OpenAI

from config import config


class LLMClient:
    """
    Wrapper class for Large Language Model providers.
    """

    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is missing. "
                "Please set it in your .env file."
            )

        self.client = OpenAI(
            api_key=config.OPENAI_API_KEY
        )

        self.model = config.OPENAI_MODEL


    def chat(self, message: str) -> str:
        """
        Send a message to the LLM and return response.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.choices[0].message.content


llm_client = LLMClient()