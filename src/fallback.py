# fallback.py
import google.generativeai as genai

genai.configure(api_key="API key")

class GeminiFallback:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def respond(self, user_message: str, history: list[dict]) -> str:
        prompt = "You are SmartSupportAI, a helpful, friendly assistant for customer queries.\n"
        for turn in history[-3:]:
            prompt += f"User: {turn['user_message']}\nBot: {turn['ai_response']}\n"
        prompt += f"User: {user_message}\nBot:"
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Sorry, I'm having a bit of trouble thinking right now. (Error: {e})"
