class Responder:
    def generate_response(self, intent: str, message: str) -> str:
        responses = {
            "greeting": "Hello! How can I help you today?",
            "issue_reporting": "I'm sorry to hear that. Can you describe the issue in more detail?",
            "feature_request": "Thanks for the suggestion! I’ve noted it down.",
            "goodbye": "Take care! Let me know if you need anything else.",
            "unknown": "Hmm... I’m not sure I understood that. Could you rephrase?"
        }
        return responses.get(intent, "Let me look into that for you.")
