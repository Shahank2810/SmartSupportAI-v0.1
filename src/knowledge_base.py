from typing import Dict

class KnowledgeBase:
    def __init__(self):
        self.client_memory: Dict[str, Dict] = {}

    def store_fact(self, client_id: str, key: str, value: str):
        if client_id not in self.client_memory:
            self.client_memory[client_id] = {}
        self.client_memory[client_id][key] = value

    def retrieve_fact(self, client_id: str, key: str) -> str:
        return self.client_memory.get(client_id, {}).get(key, "I don't know that yet.")

    def forget_fact(self, client_id: str, key: str):
        if client_id in self.client_memory and key in self.client_memory[client_id]:
            del self.client_memory[client_id][key]
