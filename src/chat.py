from llm import llm_client
from memory import memory_manager


class ChatManager:
    """
    Conversation management layer.

    Responsible for connecting:
    User -> Memory -> LLM -> Memory
    """

    def __init__(self):
        self.history = []


    def send_message(self, user_message: str) -> str:
        """
        Process one conversation turn.
        """

        # 1. Retrieve relevant memories
        memories = memory_manager.search_memory(
            user_message
        )


        # 2. Build context
        context = ""

        if memories:
            context = (
                "Relevant memories about the user:\n"
            )

            for memory in memories:
                context += (
                    f"- {memory['content']}\n"
                )


        # 3. Construct prompt
        prompt = f"""
{context}

User message:
{user_message}

Please answer the user.
"""


        # 4. Call LLM
        response = llm_client.chat(
            prompt
        )


        # 5. Store conversation
        self.history.append(
            {
                "user": user_message,
                "assistant": response
            }
        )


        # 6. Simple memory example
        # Future:
        # Replace with Mem0 automatic extraction

        if "I prefer" in user_message:
            memory_manager.add_memory(
                user_message
            )


        return response


chat_manager = ChatManager()