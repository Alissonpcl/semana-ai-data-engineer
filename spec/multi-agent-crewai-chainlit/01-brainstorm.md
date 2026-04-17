# Phase 1: /brainstorm — Multi-Agent ShopAgent with CrewAI

## Prompt

```
/brainstorm Multi-Agent ShopAgent: a CrewAI-powered multi-agent system
with 3 specialized agents (AnalystAgent for SQL on Supabase/Postgres,
ResearchAgent for semantic search on Qdrant, ReporterAgent for executive
synthesis). Uses CrewAI Sequential Process with YAML configuration.
Chainlit as conversational frontend with streaming. DeepEval for LLM
evaluation and testing. LangFuse for observability and tracing.
Cloud-ready: same architecture, swap localhost for cloud endpoints via
environment variables.
```

## Expected Output

AgentSpec explores:

1. **Discovery Questions**
   - Should the crew use Sequential or Hierarchical process?
   - How should context flow between agents (task context chaining)?
   - Should each agent have its own LLM or share one?
   - What structured output format: Pydantic models or free text?
   - How should Chainlit stream CrewAI execution (step callbacks)?
   - What DeepEval metrics: faithfulness, relevance, hallucination?
   - How should LangFuse trace each agent's reasoning separately?
   - Should the crew support follow-up questions (memory across runs)?

2. **Approaches Proposed**
   - **A.** CrewAI Sequential + YAML config + Chainlit streaming (confidence: 0.95)
   - **B.** CrewAI Hierarchical with manager agent (confidence: 0.82)
   - **C.** CrewAI Flows for production orchestration (confidence: 0.88)

3. **Recommendation**
   - Approach A for Day 4 live demo (simplest, most visual)
   - Approach C noted as production evolution path
   - DeepEval runs post-execution for quality scoring
   - LangFuse wraps each crew.kickoff() for full trace capture

4. **Artifact: BRAINSTORM.md**
   - Decision log with rationale for each choice
   - Risk assessment: token costs, latency, error handling
   - Stack confirmation: CrewAI + Chainlit + DeepEval + LangFuse
