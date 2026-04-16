Use AgentSpec to define structured requirements for ShopAgent:

/agentspec:define SHOPAGENT

Review the captured requirements:
1. Are all functional requirements there? (SQL queries, semantic search, hybrid)
2. Does the clarity score look good? (aim for 12+ out of 15)
3. Are the tools correctly identified? (supabase_execute_sql, qdrant_semantic_search)
4. Is the tech stack right? (LangChain, Claude, Chainlit, Postgres, Qdrant)

Only approve if the quality gate passes. Fix any gaps before moving to /design.
