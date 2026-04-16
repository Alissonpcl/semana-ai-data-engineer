# Phase 1: /brainstorm — ShopAgent

## Prompt

```
/brainstorm ShopAgent: autonomous e-commerce agent that queries
Postgres (The Ledger) for exact data like revenue and orders, and Qdrant
(The Memory) for semantic search on customer reviews. Uses LangChain ReAct
pattern with Claude as LLM. Needs a Chainlit chat interface with streaming,
thinking visualization, and tool-use steps visible in the UI.
```

## Expected Output

AgentSpec explores:

1. **Discovery Questions**
   - Should the agent support hybrid queries (SQL + semantic in one turn)?
   - What output format: plain text, markdown tables, or structured JSON?
   - Should routing be explicit (keyword) or NL-classification based?
   - How many pre-built SQL queries vs dynamic SQL generation?
   - Should Chainlit show intermediate thinking (ReAct steps)?
   - What error recovery: retry, fallback, or explain failure?

2. **Approaches Proposed**
   - **A.** LangChain ReAct Agent + `create_react_agent` (confidence: 0.92)
   - **B.** LangGraph StateGraph with conditional routing (confidence: 0.85)
   - **C.** CrewAI single-agent with tools (confidence: 0.78)

3. **Recommendation**
   - Approach A: ReAct is simplest for dual-store routing, maps directly to
     Day 4 multi-agent upgrade, and Chainlit has native LangChain streaming.

## Quality Gate

Can describe the full agent loop: User → Chainlit → ReAct → Tool Selection → Observation → Response
