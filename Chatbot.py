import os
import json
from .env import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=api_key)

HISTORY_FILE = "chat_history.json"

# Load history if exists
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        try:
            messages = json.load(f)
        except json.JSONDecodeError:
            messages = []
else:
    messages = []

# If no history, start fresh
if not messages:
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

print("Chatbot: Hello! Type 'exit' to end the conversation.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4o"
        messages=messages
    )

    bot_reply = response.choices[0].message.content
    print(f"Chatbot: {bot_reply}")

    messages.append({"role": "assistant", "content": bot_reply})

    # Save history
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)
