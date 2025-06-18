# client_memory.py
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
        return self.client_contexts[client_id]

    def should_store_message(self, user_message: str) -> bool:
        """Check if message should be stored in memory"""
        exit_commands = ["exit", "quit", "bye", "goodbye"]
        return user_message.lower().strip() not in exit_commands

    def save_memories(self):
        """Save all client contexts to file"""
        try:
            memories_data = {}
            for client_id, context in self.client_contexts.items():
                # Convert conversation history to JSON-serializable format and filter out exit commands
                conversation_history = []
                for msg in context.conversation_history:
                    if isinstance(msg, dict):
                        # Skip exit commands
                        user_msg = msg.get("user", "").lower().strip()
                        if user_msg in ["exit", "quit", "bye", "goodbye"]:
                            continue
                            
                        # Handle any datetime objects in the message
                        cleaned_msg = {}
                        for key, value in msg.items():
                            if isinstance(value, datetime):
                                cleaned_msg[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                            else:
                                cleaned_msg[key] = value
                        conversation_history.append(cleaned_msg)
                    else:
                        # If it's just a string, check if it's an exit command
                        if isinstance(msg, str) and msg.lower().strip() not in ["exit", "quit", "bye", "goodbye"]:
                            conversation_history.append(msg)
                
                memories_data[client_id] = {
                    "conversation_history": conversation_history,
                    "current_state": context.current_state.value if context.current_state else None,
                    "current_intent": context.current_intent,
                    "attempts": context.attempts,
                    "intent_history": context.intent_history,
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            
            with open(self.memory_file, 'w') as f:
                json.dump(memories_data, f, indent=2)
            print(f"💾 Memories saved to {self.memory_file}")
        except Exception as e:
            print(f"❌ Error saving memories: {e}")
            print(f"Debug info: Check if ConversationContext contains datetime objects")

    def load_memories(self):
        """Load client contexts from file"""
        if not os.path.exists(self.memory_file):
            print(f"📁 No existing memory file found. Starting fresh.")
            return

        try:
            with open(self.memory_file, 'r') as f:
                memories_data = json.load(f)
            
            for client_id, data in memories_data.items():
                context = ConversationContext()
                context.conversation_history = data.get("conversation_history", [])
                context.current_intent = data.get("current_intent")
                context.attempts = data.get("attempts", 0)
                context.intent_history = data.get("intent_history", [])
                
                # Restore state if it exists
                if data.get("current_state"):
                    from context import ConversationState
                    try:
                        context.current_state = ConversationState(data["current_state"])
                    except:
                        context.current_state = ConversationState.INITIAL
                
                self.client_contexts[client_id] = context
            
            print(f"🧠 Loaded memories for {len(self.client_contexts)} clients")
            
        except Exception as e:
            print(f"❌ Error loading memories: {e}")

    def get_client_stats(self, client_id: str) -> dict:
        """Get statistics for a specific client"""
        if client_id not in self.client_contexts:
            return {"messages": 0, "intents": 0, "last_seen": "Never"}
        
        context = self.client_contexts[client_id]
        return {
            "messages": len(context.conversation_history),
            "intents": len(context.intent_history),
            "current_intent": context.current_intent,
            "attempts": context.attempts,
            "last_seen": "Current session"  # You can enhance this with timestamps
        }

    def list_all_clients(self) -> list:
        """Get list of all clients with their basic info"""
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
        """Clear memory for a specific client"""
        if client_id in self.client_contexts:
            del self.client_contexts[client_id]
            self.save_memories()
            print(f"🗑️ Cleared memory for client: {client_id}")
            return True
        return False

    def __del__(self):
        """Auto-save when object is destroyed"""
        try:
            self.save_memories()
        except:
            pass
