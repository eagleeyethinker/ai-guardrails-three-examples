```python
"""
Example 1: LLM Guardrails
User -> Guardrails -> LLM
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from config.policy import input_policy

load_dotenv()
client = OpenAI()

SYSTEM = "You are a professional enterprise assistant. Be concise."

def main():
    print("Example 1 — LLM Guardrails (type 'exit' to quit)\n")
    messages = [{"role": "system", "content": SYSTEM}]
    while True:
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit"}:
            break

        allowed, reason = input_policy(user)
        if not allowed:
            print(f"Guardrails: {reason}\n")
            continue

        messages.append({"role": "user", "content": user})

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        text = resp.choices[0].message.content or ""
        print(f"Bot: {text}\n")
        messages.append({"role": "assistant", "content": text})

if __name__ == "__main__":
    main()

```