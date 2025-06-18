# engine.py
from intent_handler import IntentDetector, ConversationalResponseGenerator
from fallback import GeminiFallback
from client_memory import ClientMemoryManager
from context import ConversationState

class ConversationalSupportEngine:
    def __init__(
        self,
        intent_detector=None,
        response_generator=None,
        fallback=None,
        memory_manager=None
    ):
        self.intent_detector = intent_detector or IntentDetector()
        self.response_generator = response_generator or ConversationalResponseGenerator()
        self.fallback = fallback or GeminiFallback()
        self.memory = memory_manager or ClientMemoryManager()

    def process_message(self, client_id: str, user_message: str) -> str:
       
        context = self.memory.get_context(client_id)
        
        # 🎯 Detect intent
        result = self.intent_detector.detect_intent(user_message, context)
        intent = result["intent"]
        confidence = result["confidence"]
        matched = result["matched_patterns"]

        context.add_intent(intent, confidence, matched)

        # 🧠 If unsure, use Gemini fallback
        if intent == "unknown" or confidence < 0.4 or not matched:
            reply = self.fallback.respond(user_message, context.conversation_history)
            context.set_state(ConversationState.INITIAL, "general_chat")
            context.add_message(user_message, reply, "general_chat", confidence)
            return reply

        # 💡 Generate a proper flow response
        response, new_state = self.response_generator.generate_response(intent, context, result)
        context.set_state(new_state, intent)
        context.attempts += 1
        context.add_message(user_message, response, intent, confidence)
        return response
