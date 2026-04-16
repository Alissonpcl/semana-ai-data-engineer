Walk me through the ReAct (Reason + Act) pattern for this question:
"Clientes premium do Sudeste que reclamam de entrega: qual o ticket medio?"

Show the agent's thinking step by step:
1. Thought: what kind of data do I need? (semantic vs structured)
2. Action: which tool? (Qdrant for complaints, Postgres for ticket)
3. Observation: what came back?
4. Thought: do I need another step?
5. Action: second tool call
6. Final Answer: synthesis of both results

This is the pattern our LangChain agent will use later tonight.
