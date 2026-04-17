# Phase 3: /design — ShopAgent

## Prompt

```
/design SHOPAGENT — generate file manifest with artifact list, assign
specialist agents to each file, define the pipeline architecture, and
produce a DESIGN document for review.
```

## Expected Output

### File Manifest

| File | Purpose | Agent |
|------|---------|-------|
| `src/day3/tools.py` | LangChain @tool definitions for Ledger + Memory | python-developer |
| `src/day3/agent.py` | ReAct agent with create_react_agent | genai-architect |
| `src/day3/chainlit_app.py` | Chainlit streaming chat with tool steps | python-developer |
| `src/day3/__init__.py` | Package init | python-developer |
| `src/day3/requirements.txt` | Day 3 dependencies | python-developer |

### Pipeline Architecture

```
User Question
    ↓
Chainlit (@cl.on_message)
    ↓
agent.astream_events(v2)
    ↓
ReAct Loop (create_react_agent)
    ├── Thought: "This is a revenue question → SQL"
    ├── Action: supabase_execute_sql("faturamento por estado")
    ├── Observation: [table with 8 states, revenue data]
    ├── Thought: "I have the data, can answer now"
    └── Final Answer: formatted markdown response
    ↓
Chainlit streams tokens + shows tool steps
```

### Delegation Map

| Agent | Responsibility |
|-------|---------------|
| python-developer | tools.py, chainlit_app.py, __init__.py |
| genai-architect | agent.py (ReAct pattern + system prompt) |
| code-reviewer | Post-build quality review |

### Key Design Decisions
- Tool docstrings are the routing mechanism (not keyword matching)
- `astream_events(v2)` for real-time token streaming
- `cl.Step` context manager for tool visualization
- Fallback in qdrant tool: try day2.query_reviews, else inline LlamaIndex

## Quality Gate

Design doc reviewed → file manifest complete → agent assignments clear → APPROVED for /build
