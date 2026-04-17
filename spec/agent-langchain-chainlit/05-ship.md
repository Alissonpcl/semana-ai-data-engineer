# Phase 5: /ship — ShopAgent

## Prompt

```
/ship SHOPAGENT — verify end-to-end functionality, document the architecture,
archive learnings to knowledge base, prepare handoff to Day 4 multi-agent.
```

## Expected Output

### Deployment Verification

```
$ docker compose ps (gen/)
  ✓ postgres:16      healthy    0.0.0.0:5432
  ✓ qdrant:v1.13.2   healthy    0.0.0.0:6333

$ python3 src/day3/tools.py
  ✓ SQL tool connected → 500 customers, 200 products, 5000 orders
  ✓ Qdrant tool connected → 406 vectors in shopagent_reviews

$ python3 src/day3/agent.py
  ✓ 3/3 routing scenarios passed

$ chainlit run src/day3/chainlit_app.py --port 8000
  ✓ Chat interface live at http://localhost:8000
  ✓ Streaming + tool steps verified
```

### Architecture Documented

```
The Ledger (Postgres)          The Memory (Qdrant)
  500 customers                  406 review vectors
  200 products                   BAAI/bge-base-en-v1.5
  5,000 orders                   similarity_top_k=5
       ↑                              ↑
       |                              |
  supabase_execute_sql    qdrant_semantic_search
       |                              |
       └──────── ReAct Agent ─────────┘
                     |
              Chainlit (port 8000)
                     |
                  User Chat
```

### Learnings Archived

1. **Tool docstrings are the routing table** — the agent reads them to decide
2. **astream_events v2** is required for LangGraph streaming in Chainlit
3. **cl.Step context manager** provides tool visualization without extra config
4. **Keyword-based SQL matching** works for demo; Day 4 upgrades to dynamic SQL
5. **Qdrant fallback pattern** (try import → inline) keeps Day 3 independent

### Handoff to Day 4

| Day 3 (Single Agent) | Day 4 (Multi-Agent) |
|----------------------|---------------------|
| 1 ReAct agent | 3 specialized agents (CrewAI) |
| Agent decides tools | Each agent owns one store |
| Sequential tool calls | Parallel execution |
| Chainlit basic | Chainlit + avatars + panels |
| Local only | Cloud migration (Supabase + Qdrant Cloud) |

## Quality Gate

End-to-end verified → Architecture documented → Learnings archived → Day 4 ready
