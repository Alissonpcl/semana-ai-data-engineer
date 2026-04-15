Create src/day2/query_reviews.py that queries The Memory (Qdrant) using
LlamaIndex without re-indexing:

1. Connect to existing Qdrant collection "shopagent_reviews"
2. Build a query engine with similarity_top_k=5
3. Run these semantic searches:
   - "Clientes reclamando de entrega atrasada"
   - "Reviews positivos sobre qualidade do produto"
   - "Problemas com pagamento ou frete"
4. For each result, print the answer and the source chunks with scores

Notice how "demorou 15 dias" and "nao recebi" are found by the same query —
this is what SQL cannot do.
