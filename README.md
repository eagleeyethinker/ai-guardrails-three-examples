````markdown
# AI Guardrails — 3 Enterprise Examples

This repo contains **three progressively advanced examples** to accompany the newsletter:

1. **LLM Guardrails** — policy layer around a single LLM
2. **Agent + Tool Calling Guardrails** — LLM proposes tool calls, guardrails authorize execution
3. **Multi-Agent Guardrails** — planner + worker agents with centralized governance

## Quick start

```bash
python -m venv venv
# Windows
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# add OPENAI_API_KEY
```

Run examples:

```bash
python examples/01_llm_guardrails.py
python examples/02_agent_tool_guardrails.py
python examples/03_multi_agent_guardrails.py
```

## Architecture (high-level)

```
LLM Example:
User -> Guardrails -> LLM

Agent Example:
User -> Agent(LLM) -> Guardrails -> Tool

Multi-agent Example:
User -> Planner Agent -> Guardrails -> Worker Agent -> Guardrails -> Tools
```

## Notes

- This is intentionally small and readable.
- Replace in-memory policies with enterprise policy services in production.

````
