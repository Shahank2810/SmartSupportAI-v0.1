# intent_handler.py
import re
from context import ConversationContext, ConversationState

class IntentDetector:
    def __init__(self):
        self.intent_keywords = {
            "password_reset": ["password", "forgot", "reset", "login issue"],
            "order_tracking": ["track", "order", "status", "shipping", "delivery", "where is my order"],
            "technical_support": ["error", "crash", "bug", "not working", "issue", "glitch", "problem"],
            "refund_request": ["refund", "money back", "return", "cancel order", "cancellation"],
            "account_update": ["change email", "update profile", "edit account", "new number"],
            "product_info": ["details", "product", "feature", "specs", "information about"],
            "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
            "goodbye": ["bye", "goodbye", "see you", "later", "thanks", "thank you"]
        }

    def detect_intent(self, message: str, context: ConversationContext) -> dict:
        text = message.lower()
        scores = {}
        matched_keywords = {}

        for intent, keywords in self.intent_keywords.items():
            matched = [kw for kw in keywords if re.search(rf"\b{kw}\b", text)]
            score = len(matched)
            if score:
                scores[intent] = score
                matched_keywords[intent] = matched

        if not scores:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "matched_patterns": [],
                "conversation_action": "clarify"
            }

        best_intent = max(scores, key=scores.get)
        return {
            "intent": best_intent,
            "confidence": min(1.0, scores[best_intent] / len(self.intent_keywords[best_intent])),
            "matched_patterns": matched_keywords[best_intent],
            "conversation_action": "start_flow"
        }

class ConversationalResponseGenerator:
    def generate_response(self, intent: str, context: ConversationContext, detection_result: dict) -> tuple[str, ConversationState]:
        if intent == "password_reset":
            return "No problem! Can you please share your email so I can help reset your password?", ConversationState.COLLECTING_INFO
        elif intent == "order_tracking":
            return "Sure! Please provide your order number and I'll check its status right away.", ConversationState.COLLECTING_INFO
        elif intent == "technical_support":
            return "I'm here to help! Can you describe the issue you're facing in more detail?", ConversationState.COLLECTING_INFO
        elif intent == "refund_request":
            return "I understand. Could you provide your order ID for the refund process?", ConversationState.COLLECTING_INFO
        elif intent == "account_update":
            return "What part of your account would you like to update—email, phone, or address?", ConversationState.COLLECTING_INFO
        elif intent == "product_info":
            return "Happy to help! Which product would you like to know more about?", ConversationState.COLLECTING_INFO
        elif intent == "greeting":
            return "Hey there! 👋 How can I help you today?", ConversationState.INITIAL
        elif intent == "goodbye":
            return "You're most welcome! Have a great day ahead! 😊", ConversationState.RESOLVED
        else:
            return "Hmm... I didn't quite get that. Can you clarify your request?", ConversationState.INITIAL
