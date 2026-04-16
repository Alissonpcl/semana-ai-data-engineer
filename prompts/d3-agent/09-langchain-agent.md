Create src/day3/agent.py with a LangChain ReAct agent that uses both tools:

1. Use ChatAnthropic with claude-sonnet-4-20250514 as the LLM
2. Import the tools from tools.py
3. Create the agent with create_react_agent and a prompt that explains the
   two stores: The Ledger (SQL/exact) and The Memory (semantic/meaning)
4. Test with these 3 questions and watch the agent decide:
   - "Qual o faturamento total por estado?" (should pick SQL)
   - "Quais clientes reclamam de entrega atrasada?" (should pick Qdrant)
   - "Top 3 estados com mais reclamacoes e seu faturamento" (should pick BOTH)

Print the agent's reasoning (Thought/Action/Observation) for each question.
