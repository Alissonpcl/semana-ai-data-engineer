# Phase 3: /design — Multi-Agent ShopAgent Architecture

## Prompt

```
/design Based on the DEFINE document, architect the Multi-Agent
ShopAgent system. CrewAI Sequential Process with 3 agents, YAML
configuration, Chainlit frontend, DeepEval testing, LangFuse
observability. Produce file manifest with agent assignments.
```

## Expected Output

AgentSpec produces the technical architecture:

1. **System Architecture**
   ```
   ┌─────────────────────────────────────────────────┐
   │                 Chainlit Frontend                 │
   │          (chat UI + streaming callbacks)          │
   └──────────────────────┬──────────────────────────┘
                          │ user question
                          ▼
   ┌─────────────────────────────────────────────────┐
   │              CrewAI Sequential Crew               │
   │                                                   │
   │  ┌──────────┐  ┌──────────────┐  ┌───────────┐  │
   │  │ Analyst  │→ │  Research    │→ │  Reporter  │  │
   │  │  Agent   │  │   Agent      │  │   Agent    │  │
   │  └────┬─────┘  └──────┬───────┘  └───────────┘  │
   │       │               │                           │
   │       ▼               ▼                           │
   │  ┌─────────┐   ┌───────────┐                     │
   │  │Supabase │   │  Qdrant   │                     │
   │  │  SQL    │   │ Semantic  │                     │
   │  └─────────┘   └───────────┘                     │
   └──────────────────────┬──────────────────────────┘
                          │ structured output
                          ▼
   ┌──────────────┐  ┌──────────────┐
   │   DeepEval   │  │   LangFuse   │
   │  (testing)   │  │ (observ.)    │
   └──────────────┘  └──────────────┘
   ```

2. **File Manifest**
   ```
   src/day4/
   ├── config/
   │   ├── agents.yaml          # Agent definitions (role, goal, backstory)
   │   └── tasks.yaml           # Task definitions (description, expected_output)
   ├── tools/
   │   ├── __init__.py
   │   ├── supabase_tool.py     # supabase_execute_sql BaseTool
   │   └── qdrant_tool.py       # qdrant_semantic_search BaseTool
   ├── crew.py                  # @CrewBase class with agents + tasks + crew
   ├── models.py                # Pydantic output models (AnalystResult, etc.)
   ├── chainlit_app.py          # Chainlit UI with crew.kickoff() integration
   ├── langfuse_config.py       # LangFuse callback handler setup
   ├── test_crew.py             # DeepEval test suite (5+ test cases)
   └── .env.example             # Environment variables template
   ```

3. **Agent Assignments (who builds what)**
   - `python-developer` → tools/, models.py, crew.py
   - `shopagent-builder` → config/agents.yaml, config/tasks.yaml
   - `chainlit-specialist` → chainlit_app.py (streaming callbacks)
   - `test-generator` → test_crew.py (DeepEval metrics)
   - `ai-data-engineer` → langfuse_config.py (trace setup)

4. **Key Design Decisions**
   - YAML-first config: agents and tasks defined declaratively
   - Sequential process: predictable, debuggable, visual in Chainlit
   - Pydantic output models: structured, validatable at each step
   - LangFuse CallbackHandler wraps each crew.kickoff()
   - DeepEval runs as pytest suite, not inline

5. **Artifact: DESIGN.md**
   - Architecture diagram
   - File manifest with line count estimates
   - Agent assignment matrix
   - Technology decision rationale
