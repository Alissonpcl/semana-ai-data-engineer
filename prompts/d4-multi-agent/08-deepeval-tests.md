Create src/day4/eval_agent.py to test agent quality with DeepEval:

1. Define test cases with input question + expected tool calls:
   - "Faturamento total" -> should call supabase_execute_sql
   - "Reclamacoes de entrega" -> should call qdrant_semantic_search
   - "Analise completa por regiao" -> should call BOTH tools

2. Use ToolCorrectnessMetric — did the agent pick the RIGHT tool?
3. Use AnswerRelevancyMetric — is the final answer relevant to the question?
4. Run with: deepeval test run src/day4/eval_agent.py

This is how you prove your agent works: not "it looks right" but "it measurably works."
