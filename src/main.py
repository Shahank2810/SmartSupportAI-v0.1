# main.py
from context import ConversationContext, ConversationState
from intent_handler import IntentDetector, ConversationalResponseGenerator
from fallback import GeminiFallback

class ConversationalSupportEngine:
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.response_generator = ConversationalResponseGenerator()
        self.fallback_gemini = GeminiFallback()
        self.context = ConversationContext()

    def process_message(self, user_message: str) -> str:
        result = self.intent_detector.detect_intent(user_message, self.context)
        intent = result["intent"]
        confidence = result["confidence"]
        matched = result["matched_patterns"]

        self.context.add_intent(intent, confidence, matched)

        if intent == "unknown" or confidence < 0.4 or not matched:
            reply = self.fallback_gemini.respond(user_message, self.context.conversation_history)
            self.context.set_state(ConversationState.INITIAL, "general_chat")
            self.context.add_message(user_message, reply, "general_chat", confidence)
            return reply

        response, new_state = self.response_generator.generate_response(intent, self.context, result)
        self.context.set_state(new_state, intent)
        self.context.attempts += 1
        self.context.add_message(user_message, response, intent, confidence)
        return response

if __name__ == "__main__":
    print("🤖 Chatbot is ready! Type 'exit' to leave.\n")
    engine = ConversationalSupportEngine()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Bot: Farewell, human!")
            break
        reply = engine.process_message(user_input)
        print("Bot:", reply)
