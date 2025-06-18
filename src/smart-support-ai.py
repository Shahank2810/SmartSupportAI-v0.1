from intent_detector import IntentDetector
from knowledge_base import KnowledgeBase
from responder import Responder

class SmartSupportAI:
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.knowledge_base = KnowledgeBase()
        self.responder = Responder()

    def handle_message(self, client_id: str, message: str) -> str:
        intent = self.intent_detector.detect_intent(message)
        # (Optional) knowledge usage could go here based on intent
        return self.responder.generate_response(intent, message)
