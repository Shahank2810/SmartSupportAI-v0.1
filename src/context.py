import uuid
from datetime import datetime
from typing import Dict, List
from enum import Enum
from dataclasses import dataclass, field

class ConversationState(Enum):
    INITIAL = "initial"
    COLLECTING_INFO = "collecting_info"
    CONFIRMING = "confirming"
    PROCESSING = "processing"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

@dataclass
class ConversationContext:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    current_intent: str = None
    current_state: ConversationState = ConversationState.INITIAL
    confidence_score: float = 0.0
    collected_data: Dict = field(default_factory=dict)
    conversation_history: List[Dict] = field(default_factory=list)
    intent_history: List[Dict] = field(default_factory=list)
    required_fields: List[str] = field(default_factory=list)
    attempts: int = 0

    def add_message(self, user_msg: str, ai_response: str, detected_intent: str, confidence: float):
        from client_memory import ClientMemoryManager
        if ClientMemoryManager().is_exit_command(user_msg):
            print(f"[DEBUG] Skipped storing exit message: {user_msg}")
            return
        print(f"[DEBUG] Storing message: {user_msg}")
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user_message': user_msg,
            'ai_response': ai_response,
            'detected_intent': detected_intent,
            'confidence': confidence,
            'state': self.current_state.value
        })

    def add_intent(self, intent: str, confidence: float, patterns: List[str]):
        self.intent_history.append({
            'timestamp': datetime.now(),
            'intent': intent,
            'confidence': confidence,
            'matched_patterns': patterns
        })

    def set_state(self, new_state: ConversationState, intent: str = None):
        self.current_state = new_state
        if intent:
            self.current_intent = intent
