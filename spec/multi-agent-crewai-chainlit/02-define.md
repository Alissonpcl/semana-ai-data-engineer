# Phase 2: /define — Multi-Agent ShopAgent Requirements

## Prompt

```
/define Based on the brainstorm, define the complete requirements for
the Multi-Agent ShopAgent. The system uses CrewAI with 3 agents
(AnalystAgent, ResearchAgent, ReporterAgent), Chainlit frontend,
DeepEval evaluation, and LangFuse observability. Docker-first local
development, cloud-ready via env vars.
```

## Expected Output

AgentSpec produces a structured PRD with:

1. **Functional Requirements**
   - FR-01: AnalystAgent executes SQL queries via `supabase_execute_sql` tool
   - FR-02: ResearchAgent performs semantic search via `qdrant_semantic_search` tool
   - FR-03: ReporterAgent synthesizes SQL results + semantic insights into executive report
   - FR-04: CrewAI Sequential Process chains agents: Analyst → Research → Reporter
   - FR-05: Chainlit provides chat UI with streaming crew execution updates
   - FR-06: System prompt defines guardrails (no recipes, no off-topic)
   - FR-07: Structured output via Pydantic models for each agent's result
   - FR-08: DeepEval test suite validates faithfulness, relevance, hallucination
   - FR-09: LangFuse traces every crew execution with per-agent spans
   - FR-10: Environment-based URLs (localhost for local, cloud for production)

2. **Non-Functional Requirements**
   - NFR-01: Crew execution completes in < 30 seconds for typical queries
   - NFR-02: Token budget < $0.25 per crew run (3 agents, GPT-4o or Claude)
   - NFR-03: Chainlit streams agent progress in real-time (not batch)
   - NFR-04: Docker Compose runs full stack locally (Postgres + Qdrant + App)
   - NFR-05: DeepEval scores ≥ 0.7 on all metrics before shipping

3. **Acceptance Criteria**
   - AC-01: "Qual o faturamento total?" returns exact SQL number from Postgres
   - AC-02: "O que os clientes reclamam?" returns semantic themes from Qdrant
   - AC-03: Combined queries produce executive report with both data sources
   - AC-04: Chainlit shows which agent is active during execution
   - AC-05: LangFuse dashboard shows full trace with 3 agent spans
   - AC-06: DeepEval test suite passes with ≥ 5 test cases

4. **Artifact: DEFINE.md**
   - Clarity score ≥ 12/15
   - All requirements traceable to user stories
   - Technology constraints documented
