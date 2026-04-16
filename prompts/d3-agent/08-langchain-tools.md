Create src/day3/tools.py with two LangChain tools for the ShopAgent:

1. supabase_execute_sql -- connects to Postgres (localhost:5432, shopagent/shopagent),
   receives a SQL query string, executes it, returns results. Description must tell
   the agent: "Use for exact data: revenue, counts, averages, orders, products, customers."

2. qdrant_semantic_search -- connects to Qdrant (localhost:6333), searches the
   "shopagent_reviews" collection using LlamaIndex query engine. Description must tell
   the agent: "Use for meaning: complaints, sentiment, review themes, customer opinions."

Use @tool decorator from langchain_core.tools. The descriptions are critical --
they're how the agent decides which tool to use.
