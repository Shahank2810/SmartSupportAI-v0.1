from typing import Optional

class IntentDetector:
    def __init__(self):
        self.intents = {
            "greeting": ["hello", "hi", "hey"],
            "issue_reporting": ["problem", "not working", "issue"],
            "feature_request": ["can you add", "I want a feature", "please add"],
            "goodbye": ["bye", "see you", "later"]
        }

    def detect_intent(self, message: str) -> Optional[str]:
        message = message.lower()
        for intent, patterns in self.intents.items():
            if any(p in message for p in patterns):
                return intent
        return "unknown"
