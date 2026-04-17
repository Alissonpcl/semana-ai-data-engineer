# Phase 5: /ship — Multi-Agent ShopAgent Deployment

## Prompt

```
/ship The Multi-Agent ShopAgent is built and tested. Ship it:
verify all tests pass, document the architecture, capture lessons
learned, update the Knowledge Base with new patterns discovered
during the build. Archive the feature as complete.
```

## Expected Output

AgentSpec produces the shipping artifacts:

1. **Pre-Ship Checklist**
   - [ ] All DeepEval tests passing (≥ 0.7 on all metrics)
   - [ ] Chainlit UI tested with 5+ query types
   - [ ] LangFuse traces visible in dashboard
   - [ ] Docker Compose runs full stack locally
   - [ ] Environment variables documented in .env.example
   - [ ] No hardcoded API keys in source
   - [ ] README.md with setup instructions

2. **Architecture Documentation**
   ```
   ## Multi-Agent ShopAgent — Day 4

   Stack: CrewAI + Chainlit + DeepEval + LangFuse
   Process: Sequential (Analyst → Research → Reporter)

   ### Quick Start
   cp .env.example .env
   # Set ANTHROPIC_API_KEY, SUPABASE_URL, QDRANT_URL
   docker compose up
   chainlit run chainlit_app.py

   ### Testing
   pytest test_crew.py -v

   ### Observability
   # LangFuse: http://localhost:3000
   # Every crew.kickoff() creates a trace with 3 agent spans
   ```

3. **Lessons Learned**
   - CrewAI YAML config is the fastest path to multi-agent prototype
   - Sequential process is best for demos (visual, predictable)
   - Pydantic output models prevent downstream parsing errors
   - LangFuse CallbackHandler needs to wrap the entire kickoff()
   - DeepEval faithfulness metric catches hallucination reliably
   - Chainlit Step UI is ideal for showing agent-by-agent progress
   - Token cost: ~$0.15-0.25 per crew run with Claude Sonnet

4. **KB Updates**
   - New pattern: `patterns/crewai-chainlit-streaming.md`
   - New pattern: `patterns/deepeval-crew-testing.md`
   - Updated: `patterns/shopagent-crew.md` with Day 4 learnings
   - Updated: `concepts/tools.md` with Supabase + Qdrant BaseTool

5. **Cloud Migration Notes**
   - Swap SUPABASE_URL from localhost to cloud project URL
   - Swap QDRANT_URL from localhost to Qdrant Cloud endpoint
   - Add LANGFUSE_HOST for cloud LangFuse instance
   - Same code, zero changes — environment-driven

6. **Artifact: SHIP.md**
   - Feature archive with all decisions documented
   - Performance metrics (latency, token cost, eval scores)
   - Next steps: Hierarchical process, more agents, Flows
