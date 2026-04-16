Create the CrewAI tools in src/day4/tools.py:

1. **supabase_execute_sql** — receives a SQL query string, connects to Postgres via psycopg2,
   executes the query, returns results as formatted text. Use SUPABASE_DB_URL from env.

2. **qdrant_semantic_search** — receives a natural language query, uses FastEmbed
   (BAAI/bge-base-en-v1.5) to encode it, searches Qdrant collection "shopagent_reviews",
   returns top 5 results with score, rating, and comment text.

Use @tool decorator from crewai. Each tool must have a clear docstring —
CrewAI uses the docstring to decide WHEN to call the tool.
