# Phase 4: /build — Multi-Agent ShopAgent Implementation

## Prompt

```
/build Execute the DESIGN document. Build the Multi-Agent ShopAgent
using CrewAI Sequential Process. Follow the file manifest exactly.
Each file must be production-ready with proper imports, error handling,
and type hints. Use the agent assignments from the design phase.
```

## Expected Output

AgentSpec delegates to specialist agents and produces:

1. **config/agents.yaml** (shopagent-builder)
   ```yaml
   analyst_agent:
     role: >
       Senior SQL Data Analyst
     goal: >
       Execute precise SQL queries against the e-commerce database
       to extract exact metrics: revenue, order counts, averages,
       and rankings. Always return numbers, never estimates.
     backstory: >
       You are a data analyst with 10 years of experience querying
       e-commerce databases. You write clean, optimized SQL and
       always verify your results before reporting.
     llm: anthropic/claude-sonnet-4-20250514
     max_iter: 5
     verbose: true

   research_agent:
     role: >
       Customer Experience Researcher
     goal: >
       Search customer reviews semantically to identify themes,
       sentiment patterns, and recurring complaints. Provide
       qualitative insights that numbers alone cannot reveal.
     backstory: >
       You are a UX researcher specializing in voice-of-customer
       analysis. You find patterns in unstructured feedback that
       drive product decisions.
     llm: anthropic/claude-sonnet-4-20250514
     max_iter: 5
     verbose: true

   reporter_agent:
     role: >
       Executive Report Writer
     goal: >
       Combine SQL data and semantic insights into a clear,
       actionable executive summary. Always cite your sources
       and provide specific recommendations.
     backstory: >
       You write board-level reports that combine hard data with
       customer context. Your reports drive decisions because they
       are precise, honest, and actionable.
     llm: anthropic/claude-sonnet-4-20250514
     max_iter: 3
     verbose: true
   ```

2. **config/tasks.yaml** (shopagent-builder)
   ```yaml
   analysis_task:
     description: >
       Analyze the e-commerce database to answer: {question}
       Write and execute SQL queries to get exact numbers.
       Return structured results with the query used.
     expected_output: >
       A structured analysis with SQL query, raw results,
       and a brief interpretation of the numbers.
     agent: analyst_agent

   research_task:
     description: >
       Search customer reviews semantically for: {question}
       Find relevant themes, sentiment, and patterns.
       Return the top findings with supporting quotes.
     expected_output: >
       A research brief with 3-5 key findings, each supported
       by actual customer review excerpts.
     agent: research_agent
     context:
       - analysis_task

   report_task:
     description: >
       Create an executive report combining the SQL analysis
       and review research for: {question}
       Synthesize both data sources into actionable insights.
     expected_output: >
       A concise executive report with: key metrics, customer
       sentiment summary, and 3 specific recommendations.
     agent: reporter_agent
     context:
       - analysis_task
       - research_task
   ```

3. **tools/supabase_tool.py** (python-developer)
   - BaseTool subclass with Pydantic input schema
   - Executes SQL via Supabase client
   - Returns formatted results as string
   - Environment-based URL (SUPABASE_URL, SUPABASE_KEY)

4. **tools/qdrant_tool.py** (python-developer)
   - BaseTool subclass with Pydantic input schema
   - Generates embedding via Claude/OpenAI
   - Queries Qdrant collection with similarity search
   - Returns top-k results with metadata
   - Environment-based URL (QDRANT_URL)

5. **crew.py** (python-developer)
   - @CrewBase decorated class
   - Loads agents.yaml and tasks.yaml
   - Registers tools per agent
   - Process.sequential with memory=True
   - Returns CrewOutput with token_usage

6. **chainlit_app.py** (chainlit-specialist)
   - @cl.on_message handler calls crew.kickoff()
   - Streams agent progress via CrewAI callbacks
   - Shows which agent is active (Step UI)
   - Displays final report as formatted message
   - System prompt with guardrails

7. **langfuse_config.py** (ai-data-engineer)
   - LangFuse CallbackHandler initialization
   - Wraps crew execution with trace context
   - Tags: crew_name, session_id, model
   - Environment-based (LANGFUSE_HOST, keys)

8. **test_crew.py** (test-generator)
   - 5+ DeepEval test cases
   - Metrics: faithfulness, relevance, hallucination, toxicity
   - Assert all scores ≥ 0.7
   - Runs via: `pytest test_crew.py`

9. **Artifact: BUILD.md**
   - File completion checklist
   - Test results summary
   - Token usage report
