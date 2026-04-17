# Phase 2: /define — ShopAgent

## Prompt

```
/define SHOPAGENT — extract structured requirements from the brainstorm,
identify users, set goals with MoSCoW priorities, write acceptance tests,
and produce a clarity score >= 12/15.
```

## Expected Output

### Functional Requirements (MUST)
- FR-01: Query Postgres for exact metrics (revenue, counts, averages)
- FR-02: Search Qdrant for semantic review analysis (complaints, sentiment)
- FR-03: Autonomous tool routing — agent decides which store to query
- FR-04: Hybrid queries — use both stores when question requires it
- FR-05: Chainlit chat interface with streaming responses
- FR-06: Tool-use steps visible as collapsible panels in chat

### Functional Requirements (SHOULD)
- FR-07: Thinking visualization (ReAct Thought/Action/Observation)
- FR-08: Markdown rendering for tables, bold, bullet points
- FR-09: Portuguese language support for all responses

### Constraints
- Python 3.11+ with type hints
- Docker-first (100% local, ports 5432/6333)
- Claude Sonnet as LLM base
- LangChain + LangGraph for agent framework
- Chainlit >= 2.0 for chat interface

### Acceptance Tests
- AT-01: "Faturamento por estado?" → agent picks SQL, returns table
- AT-02: "Reclamacoes de entrega?" → agent picks Qdrant, cites reviews
- AT-03: "Premium no Sudeste que reclamam: ticket medio?" → uses BOTH tools
- AT-04: Chainlit shows tool steps as collapsible sections

### Clarity Score

| Dimension | Score |
|-----------|-------|
| Problem   | 3/3   |
| Users     | 3/3   |
| Goals     | 3/3   |
| Success   | 2/3   |
| Scope     | 3/3   |
| **Total** | **14/15** |

## Quality Gate

Clarity score >= 12/15 → APPROVED for /design
