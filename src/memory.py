from typing import List, Dict


class MemoryManager:
    """
    Memory management layer.

    This class provides an abstraction layer
    for future memory systems such as Mem0.
    """

    def __init__(self):
        self.memories = []


    def add_memory(self, content: str):
        """
        Store a new memory.

        Future implementation:
        Send memory to Mem0.
        """

        memory = {
            "content": content
        }

        self.memories.append(memory)


    def search_memory(self, query: str) -> List[Dict]:
        """
        Retrieve relevant memories.

        Future implementation:
        Query Mem0 vector database.
        """

        results = []

        for memory in self.memories:
            if query.lower() in memory["content"].lower():
                results.append(memory)

        return results


    def get_all_memories(self):
        """
        Return all stored memories.
        """

        return self.memories


memory_manager = MemoryManager()