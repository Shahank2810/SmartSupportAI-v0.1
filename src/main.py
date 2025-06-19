import signal
import sys
from engine import ConversationalSupportEngine

def signal_handler(sig, frame):
    print("\n\n👋 Goodbye! Thanks for chatting!")
    sys.exit(0)

if __name__ == "__main__":
    print("🤖 Chatbot is alive! Type 'exit' to leave.\n")

    signal.signal(signal.SIGINT, signal_handler)

    client_id = input("Enter your username/client ID: ").strip()
    if not client_id:
        client_id = "guest_user"
        print(f"Using default client ID: {client_id}")
    else:
        print(f"Welcome, {client_id}!")

    print("\nYou can start chatting now. Type 'exit' to leave.\n")

    engine = ConversationalSupportEngine()

    while True:
        try:
            user_input = input(f"{client_id}: ").strip()

            # Exit filter BEFORE anything else
            if engine.memory.is_exit_command(user_input):
                print("👋 Thanks for chatting! Goodbye!")
                break

            if not user_input:
                continue

            response = engine.process_message(client_id, user_input)
            print(f"🤖 Bot: {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for chatting!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔄 Let's try again...\n")

    try:
        engine.memory.save_memories()
        print("💾 Memories saved successfully!")
    except Exception as e:
        print(f"⚠️ Warning: Could not save memories: {e}")

    print("Session ended. 🎯")
