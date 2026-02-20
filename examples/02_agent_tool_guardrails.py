```python
"""
Example 2: Agent + Tool Calling Guardrails

User -> Agent(LLM decides tool) -> Guardrails -> Tool execution
"""

import json
from dotenv import load_dotenv
from openai import OpenAI
from config.tools import OPENAI_TOOLS, TOOL_REGISTRY
from config.policy import input_policy, tool_policy

load_dotenv()
client = OpenAI()

SYSTEM = """You are an enterprise assistant.
Use tools when appropriate.
"""

def main():
    print("Example 2 — Agent Tool Calling + Guardrails (type 'exit' to quit)\n")
    messages = [{"role": "system", "content": SYSTEM}]
    user_role = "user"

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
            tools=OPENAI_TOOLS,
            tool_choice="auto",
        )

        msg = resp.choices[0].message

        if msg.tool_calls:
            for tc in msg.tool_calls:
                tool_name = tc.function.name
                args = json.loads(tc.function.arguments or "{}")

                ok, why = tool_policy(tool_name, args, role=user_role)
                if not ok:
                    print(f"Guardrails BLOCKED tool '{tool_name}': {why}\n")
                    continue

                result = TOOL_REGISTRY[tool_name](**args)
                print(f"Tool executed ({tool_name}): {result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tool_name,
                    "content": result,
                })

            # ask model to summarize after tool
            follow = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            text = follow.choices[0].message.content or ""
            print(f"Bot: {text}\n")
            messages.append({"role": "assistant", "content": text})
        else:
            text = msg.content or ""
            print(f"Bot: {text}\n")
            messages.append({"role": "assistant", "content": text})

if __name__ == "__main__":
    main()

```