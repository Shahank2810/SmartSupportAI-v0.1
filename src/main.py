# main.py
import signal
import sys
from context import ConversationContext, ConversationState
from intent_handler import IntentDetector, ConversationalResponseGenerator
from fallback import GeminiFallback
from engine import ConversationalSupportEngine  # Import the correct class

# Remove the duplicate class definition - use the one from engine.py

def save_and_exit(engine):
    """Save memories and exit gracefully"""
    print("\nBot: Saving your memories... 💾")
    engine.memory.save_memories()
    print("Bot: Peace out! 👋")
    sys.exit(0)

def signal_handler(sig, frame, engine):
    """Handle Ctrl+C gracefully"""
    save_and_exit(engine)

if __name__ == "__main__":
    print("🤖 Chatbot is alive! Type 'exit' to leave.\n")
    
    # Get username/client_id from user
    client_id = input("Enter your username/client ID: ").strip()
    if not client_id:
        client_id = "anonymous_user"
        print(f"Using default client ID: {client_id}")
    else:
        print(f"Welcome, {client_id}!")
    
    print("\nYou can start chatting now. Type 'exit' to leave.\n")
    
    engine = ConversationalSupportEngine()
    
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, engine))
    
    try:
        while True:
            user_input = input(f"{client_id}: ")
            if user_input.lower() in ("exit", "quit"):
                save_and_exit(engine)
            # Only process non-exit commands through the engine
            reply = engine.process_message(client_id, user_input)
            print("Bot:", reply)
    except KeyboardInterrupt:
        save_and_exit(engine)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        save_and_exit(engine)
