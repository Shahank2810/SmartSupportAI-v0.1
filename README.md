
---

# 🧠 SmartSupportAI

A modular, memory-aware AI customer support engine that detects user intent, extracts context, tracks conversation state, and responds smartly — all while leaving room for fallback models and client-specific memory.

## 🚀 What It Does

SmartSupportAI is a rule-based + NLP-powered conversational engine built for:

* Intent detection from user queries (with confidence scoring)
* Entity extraction (emails, order IDs, phone numbers, etc.)
* Memoryful context tracking per client
* State transitions (`INITIAL`, `COLLECTING_INFO`, `RESOLVED`, etc.)
* Modular fallback handling (e.g., Gemini, GPT)
* Client-specific message filtering (e.g., skip "exit" messages)

---

## 🧩 Project Structure (So Far)

```bash
SmartSupportAI/
├── engine.py                      # Main conversational engine
├── context.py                     # Tracks session state, history, entities
├── intent_handler.py              # Intent detection, entity extraction, response generation
├── client_memory.py               # Manages client contexts (per-user memory)
├── fallback.py                    # Handles unknown intents with Gemini or fallback logic
├── test_data/                     # (Optional) Test prompts, examples, transcripts
└── README.md                      # This very document
```

---

## ⚙️ Core Features

| Feature                  | Description                                                         |
| ------------------------ | ------------------------------------------------------------------- |
| 🧠 Intent Detection      | Keyword + synonym matching + optional NLTK lemmatization            |
| 📦 Entity Extraction     | Auto-detect emails, phone numbers, order IDs from user messages     |
| 💬 Conversational Memory | Stores message history per client ID (filters "exit")               |
| 🔁 State Tracking        | Transitions between states like `COLLECTING_INFO`, `RESOLVED`, etc. |
| 🛑 Fallback Support      | Custom fallback handler (`GeminiFallback` for now)                  |
| 🧰 Extensible Design     | Easily swappable modules (intent, memory, fallback, etc.)           |

---

## 📚 How It Works

### 1. `ConversationalSupportEngine` (`engine.py`)

Takes in a user message + client ID, routes through:

```text
IntentDetector → EntityExtractor → ResponseGenerator
                           ↓
              Updates context and memory
```

### 2. `ConversationContext` (`context.py`)

Tracks:

* session\_id
* current\_state + current\_intent
* history of messages & intents
* entities extracted

### 3. `IntentDetector` + `EntityExtractor`

* Expands synonyms
* Lemmatizes input (via `nltk`)
* Matches patterns per intent
* Extracts structured data (email, phone, order)

---

## 🧪 How to Run (Basic)

Make sure you’re using Python **3.11** (🛑 not 3.13 yet!).

```bash
pip install nltk
```

Download required NLTK data (only once):

```python
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
```

Then run your engine in a script like:

```python
from engine import ConversationalSupportEngine

engine = ConversationalSupportEngine()
response = engine.process_message("user123", "I forgot my password. My email is foo@example.com")
print(response)
```

---

## 🛣️ Roadmap (Next Steps)

| Milestone                    | Status          |
| ---------------------------- | --------------- |
| ✅ Basic intent handling      | Done            |
| ✅ Entity extraction          | Done            |
| ✅ Memory manager             | Done            |
| ✅ Fallback support           | Done            |
| 🔲 FastAPI wrapper           | Coming up next! |
| 🔲 Persistent DB for context | Optional        |
| 🔲 RAG/GPT fallback module   | Optional        |
| 🔲 UI demo/chat interface    | Optional        |
| 🔲 Unit tests + validation   | Optional        |
| 🔲 Analytics dashboard       | Optional        |

---

## 🧙‍♂️ Contributions & Philosophy

This is not just a support bot — it’s a structured **thinking agent**.
It believes in:

* Contextual conversations
* Intelligent fallback
* Declarative modularity

And most of all: **clarity through structure**.



---

