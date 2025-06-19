import json
import os
from typing import Dict
from datetime import datetime
from context import ConversationContext

class ClientMemoryManager:
    def __init__(self, memory_file: str = "client_memories.json"):
        self.client_contexts: Dict[str, ConversationContext] = {}
        self.memory_file = memory_file
        self.load_memories()

    def get_context(self, client_id: str) -> ConversationContext:
        if client_id not in self.client_contexts:
            self.client_contexts[client_id] = ConversationContext()
            print(f"📝 Created new memory for client: {client_id}")
        else:
            context = self.client_contexts[client_id]
            if context.conversation_history:
                print(f"🧠 Loaded existing context for {client_id} ({len(context.conversation_history)} previous messages)")
        return self.client_contexts[client_id]

    def is_exit_command(self, message: str) -> bool:
        return message.lower().strip() in {"exit", "quit", "bye", "goodbye"}

    def save_memories(self):
        try:
            exit_commands = {"exit", "quit", "bye", "goodbye"}
            memories_data = {}

            for client_id, context in self.client_contexts.items():
                conversation_history = []
                for msg in context.conversation_history:
                    if isinstance(msg, dict):
                        if msg.get("user_message", "").lower().strip() in exit_commands:
                            print(f"[SKIP] Skipping exit message: {msg.get('user_message')}")
                            continue
                        cleaned_msg = {}
                        for key, value in msg.items():
                            if isinstance(value, datetime):
                                cleaned_msg[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                            else:
                                cleaned_msg[key] = value
                        conversation_history.append(cleaned_msg)
                    elif isinstance(msg, str):
                        if msg.lower().strip() in exit_commands:
                            continue
                        conversation_history.append(msg)

                # 🧼 Clean datetime inside intent history
                intent_history = []
                for intent_entry in context.intent_history:
                    cleaned_intent = {}
                    for key, value in intent_entry.items():
                        if isinstance(value, datetime):
                            cleaned_intent[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            cleaned_intent[key] = value
                    intent_history.append(cleaned_intent)

                memories_data[client_id] = {
                    "conversation_history": conversation_history,
                    "current_intent": context.current_intent,
                    "attempts": context.attempts,
                    "intent_history": intent_history,
                    "current_state": context.current_state.value if hasattr(context.current_state, 'value') else str(context.current_state)
                }

                print(f"[SAVE] Saving {len(conversation_history)} messages for {client_id}")

            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(memories_data, f, indent=4)

            print(f"💾 Saved memories for {len(memories_data)} clients")

        except Exception as e:
            print(f"❌ Failed to save memories: {e}")

    def load_memories(self):
        if not os.path.exists(self.memory_file):
            print(f"📁 No existing memory file found. Starting fresh.")
            return

        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                memories_data = json.load(f)

            for client_id, data in memories_data.items():
                context = ConversationContext()

                if isinstance(data, list):
                    context.conversation_history = data
                elif isinstance(data, dict):
                    context.conversation_history = data.get("conversation_history", [])
                    context.current_intent = data.get("current_intent")
                    context.attempts = data.get("attempts", 0)
                    context.intent_history = data.get("intent_history", [])

                    if data.get("current_state"):
                        from context import ConversationState
                        try:
                            if hasattr(ConversationState, data["current_state"]):
                                context.current_state = getattr(ConversationState, data["current_state"])
                            else:
                                context.current_state = ConversationState(data["current_state"])
                        except:
                            context.current_state = ConversationState.INITIAL

                self.client_contexts[client_id] = context

            print(f"🧠 Loaded memories for {len(self.client_contexts)} clients")
            for client_id, context in self.client_contexts.items():
                print(f"   └─ {client_id}: {len(context.conversation_history)} messages, intent: {context.current_intent}")

        except Exception as e:
            print(f"❌ Error loading memories: {e}")
            import traceback
            traceback.print_exc()

    def get_client_stats(self, client_id: str) -> dict:
        if client_id not in self.client_contexts:
            return {"messages": 0, "intents": 0, "last_seen": "Never"}

        context = self.client_contexts[client_id]
        return {
            "messages": len(context.conversation_history),
            "intents": len(context.intent_history),
            "current_intent": context.current_intent,
            "attempts": context.attempts,
            "last_seen": "Current session"
        }

    def list_all_clients(self) -> list:
        clients = []
        for client_id, context in self.client_contexts.items():
            clients.append({
                "client_id": client_id,
                "message_count": len(context.conversation_history),
                "intent_count": len(context.intent_history),
                "current_intent": context.current_intent
            })
        return clients

    def clear_client_memory(self, client_id: str) -> bool:
        if client_id in self.client_contexts:
            del self.client_contexts[client_id]
            self.save_memories()
            print(f"🗑️ Cleared memory for client: {client_id}")
            return True
        return False

    def __del__(self):
        try:
            self.save_memories()
        except:
            pass
