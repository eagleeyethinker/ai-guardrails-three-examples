```python
"""
Example 3: Multi-Agent Guardrails

Planner agent -> Guardrails -> Worker agent -> Guardrails -> Tools
"""

import json
from dotenv import load_dotenv
from openai import OpenAI
from config.tools import OPENAI_TOOLS, TOOL_REGISTRY
from config.policy import input_policy, tool_policy

load_dotenv()
client = OpenAI()

PLANNER_SYSTEM = """You are a planner agent.
Decide which worker should handle the task.
Return one word: SUPPORT or DATA.
"""

WORKER_SUPPORT_SYSTEM = "You are a support agent. Use tools if needed."
WORKER_DATA_SYSTEM = "You are a data agent. Use tools if needed."

def call_model(system_prompt, messages, tools=None):
    kwargs = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": system_prompt}] + messages,
    }
    if tools is not None:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    return client.chat.completions.create(**kwargs)

def main():
    print("Example 3 — Multi-Agent Guardrails (type 'exit' to quit)\n")
    user_role = "user"
    history = []

    while True:
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit"}:
            break

        ok, why = input_policy(user)
        if not ok:
            print(f"Guardrails: {why}\n")
            continue

        history.append({"role": "user", "content": user})

        # Planner agent
        planner_resp = call_model(PLANNER_SYSTEM, history)
        route = (planner_resp.choices[0].message.content or "").strip().upper()
        worker_system = WORKER_SUPPORT_SYSTEM if "SUPPORT" in route else WORKER_DATA_SYSTEM

        print(f"[Planner routed to: {route}]")

        worker_resp = call_model(worker_system, history, tools=OPENAI_TOOLS)
        msg = worker_resp.choices[0].message

        if msg.tool_calls:
            for tc in msg.tool_calls:
                tool_name = tc.function.name
                args = json.loads(tc.function.arguments or "{}")

                allowed, reason = tool_policy(tool_name, args, role=user_role)
                if not allowed:
                    print(f"Guardrails BLOCKED tool '{tool_name}': {reason}")
                    continue

                result = TOOL_REGISTRY[tool_name](**args)
                print(f"Tool executed ({tool_name}): {result}")

                history.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tool_name,
                    "content": result,
                })

            final = call_model(worker_system, history)
            text = final.choices[0].message.content or ""
        else:
            text = msg.content or ""

        print(f"Bot: {text}\n")
        history.append({"role": "assistant", "content": text})

if __name__ == "__main__":
    main()

```