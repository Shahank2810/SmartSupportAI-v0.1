import re
from nltk.stem import WordNetLemmatizer
from context import ConversationContext, ConversationState

lemmatizer = WordNetLemmatizer()


class EntityExtractor:
    def extract_entities(self, message: str, intent: str) -> dict:
        entities = {}
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        order_id_pattern = r"\b\d{5,}\b"
        phone_pattern = r"\b\d{10}\b"

        if intent in ["password_reset", "account_update"]:
            email_match = re.search(email_pattern, message)
            if email_match:
                entities["email"] = email_match.group()

        if intent in ["order_tracking", "refund_request"]:
            order_match = re.search(order_id_pattern, message)
            if order_match:
                entities["order_id"] = order_match.group()

        if intent == "account_update":
            phone_match = re.search(phone_pattern, message)
            if phone_match:
                entities["phone_number"] = phone_match.group()

        return entities


class IntentDetector:
    def __init__(self, use_lemmatizer=True):
        self.use_lemmatizer = use_lemmatizer
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

        self.synonym_map = {
            "package": "order",
            "shipment": "order",
            "parcel": "order",
            "shipping": "delivery",
            "crashing": "crash",
            "malfunction": "bug",
            "freeze": "crash",
            "lag": "issue",
            "cancel": "cancel order",
            "return": "refund",
            "email address": "email",
            "specifications": "specs",
            "functions": "features",
            "functionality": "features",
        }

    def _lemmatize(self, text: str) -> str:
        return " ".join(lemmatizer.lemmatize(word) for word in text.split())

    def _expand_synonyms(self, text: str) -> str:
        for word, replacement in self.synonym_map.items():
            text = re.sub(rf'\b{re.escape(word)}\b', replacement, text)
        return text

    def detect_intent(self, message: str, context: ConversationContext) -> dict:
        text = message.lower()
        text = self._expand_synonyms(text)
        if self.use_lemmatizer:
            text = self._lemmatize(text)

        scores = {}
        matched_keywords = {}

        for intent, keywords in self.intent_keywords.items():
            matched = [kw for kw in keywords if re.search(rf"\b{re.escape(kw)}\b", text)]
            score = len(matched)
            if score:
                scores[intent] = score
                matched_keywords[intent] = matched

        if not scores or max(scores.values()) / 6 < 0.3:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "matched_patterns": [],
                "conversation_action": "clarify",
                "entities": {}
            }

        best_intent = max(scores, key=scores.get)
        confidence = min(1.0, scores[best_intent] / len(self.intent_keywords[best_intent]))

        extractor = EntityExtractor()
        entities = extractor.extract_entities(message, best_intent)

        print(f"[DEBUG] Intent: {best_intent}, confidence: {confidence:.2f}, patterns: {matched_keywords[best_intent]}, entities: {entities}")

        return {
            "intent": best_intent,
            "confidence": confidence,
            "matched_patterns": matched_keywords[best_intent],
            "conversation_action": "start_flow",
            "entities": entities
        }


class ConversationalResponseGenerator:
    def __init__(self):
        self.extractor = EntityExtractor()

    def generate_response(self, intent: str, context: ConversationContext, detection_result: dict) -> tuple[str, ConversationState]:
        message = context.latest_message
        entities = detection_result.get("entities") or self.extractor.extract_entities(message, intent)

        if intent == "password_reset":
            if "email" in entities:
                return f"Reset link has been sent to {entities['email']}.", ConversationState.RESOLVED
            return "No problem! Can you please share your email so I can help reset your password?", ConversationState.COLLECTING_INFO

        elif intent == "order_tracking":
            if "order_id" in entities:
                return f"Tracking order {entities['order_id']}... 📦", ConversationState.RESOLVED
            return "Sure! Please provide your order number and I'll check its status right away.", ConversationState.COLLECTING_INFO

        elif intent == "technical_support":
            return "I'm here to help! Can you describe the issue you're facing in more detail?", ConversationState.COLLECTING_INFO

        elif intent == "refund_request":
            if "order_id" in entities:
                return f"Processing refund for order {entities['order_id']}. Please wait...", ConversationState.RESOLVED
            return "I understand. Could you provide your order ID for the refund process?", ConversationState.COLLECTING_INFO

        elif intent == "account_update":
            if "phone_number" in entities:
                return f"Got it. Updating your phone number to {entities['phone_number']}.", ConversationState.RESOLVED
            return "What part of your account would you like to update—email, phone, or address?", ConversationState.COLLECTING_INFO

        elif intent == "product_info":
            return "Happy to help! Which product would you like to know more about?", ConversationState.COLLECTING_INFO

        elif intent == "greeting":
            return "Hey there! 👋 How can I help you today?", ConversationState.INITIAL

        elif intent == "goodbye":
            return "You're most welcome! Have a great day ahead! 😊", ConversationState.RESOLVED

        else:
            return "Hmm... I didn't quite get that. Can you clarify your request?", ConversationState.INITIAL
