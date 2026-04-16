Design the 3-agent crew on paper before writing code:

1. **AnalystAgent** — SQL data analyst. Tool: supabase_execute_sql. Queries The Ledger.
   "Faturamento por estado" -> writes SQL -> returns numbers.

2. **ResearchAgent** — Customer experience researcher. Tool: qdrant_semantic_search. Queries The Memory.
   "Reclamacoes de entrega" -> semantic search -> returns review themes.

3. **ReporterAgent** — Executive report writer. No tools. Receives context from both agents.
   Synthesizes a professional report with data + insights + recommendations.

The pattern is Sequential: Analyst -> Researcher -> Reporter. Each builds on the previous.
