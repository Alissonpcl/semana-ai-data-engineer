# Phase 4: /build — ShopAgent

## Prompt

```
/build SHOPAGENT — execute the DESIGN manifest, delegate each file to its
specialist agent, write production code with type hints, run tests
iteratively until all pass, produce a BUILD report.
```

## Expected Output

### Build Execution

```
★ Executing DESIGN manifest...

[python-developer] → src/day3/tools.py
  ✓ supabase_execute_sql with 7 pre-built queries
  ✓ qdrant_semantic_search with LlamaIndex fallback
  ✓ _match_query keyword routing
  ✓ _format_results table formatter

[genai-architect] → src/day3/agent.py
  ✓ create_react_agent with Claude Sonnet
  ✓ System prompt: dual-store routing in Portuguese
  ✓ run_agent() for CLI testing
  ✓ Streaming enabled (temperature=0)

[python-developer] → src/day3/chainlit_app.py
  ✓ @cl.on_chat_start welcome message
  ✓ @cl.on_message with astream_events(v2)
  ✓ Token streaming (text blocks + string chunks)
  ✓ cl.Step for tool visualization
  ✓ Output truncation (2000 chars max)

[code-reviewer] → Post-build review
  ✓ No security issues
  ✓ Type hints present
  ✓ Error handling for DB connections
  ✓ Graceful fallback in Qdrant tool
```

### Build Report

| Metric | Value |
|--------|-------|
| Files generated | 5 |
| Agents delegated | 3 |
| Lines of code | ~200 |
| SQL queries | 7 |
| Tool definitions | 2 |
| Errors | 0 |

### Test Results

```
$ python3 src/day3/tools.py
  ✓ supabase_execute_sql: "Faturamento por estado" → 8 rows
  ✓ qdrant_semantic_search: "Entrega atrasada" → 5 chunks

$ python3 src/day3/agent.py
  ✓ SQL routing: "Faturamento por estado?" → supabase_execute_sql
  ✓ Semantic routing: "Reviews positivos?" → qdrant_semantic_search
  ✓ Hybrid routing: "Premium + reclamacoes?" → BOTH tools

$ chainlit run src/day3/chainlit_app.py --port 8000
  ✓ Welcome message rendered
  ✓ Streaming response working
  ✓ Tool steps visible in chat
```

## Quality Gate

All tests pass → 3 routing scenarios verified → Chainlit UI functional → APPROVED for /ship
