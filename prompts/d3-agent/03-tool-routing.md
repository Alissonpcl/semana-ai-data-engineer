How does an agent decide "this is SQL" vs "this is semantic search"?
Analyze these 6 questions and classify each as Ledger (SQL), Memory (Qdrant),
or Both:

1. "Qual o faturamento total por estado?"
2. "Quais clientes reclamam de entrega atrasada?"
3. "Top 5 produtos por receita"
4. "Resumo das reclamacoes sobre qualidade"
5. "Clientes do Sudeste com reviews negativos: ticket medio?"
6. "Sentimento geral dos clientes de SP"

What keywords/patterns would tell the agent which tool to pick?
This is the routing logic we'll encode in the tool descriptions.
