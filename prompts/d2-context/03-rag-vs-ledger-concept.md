Explain the two types of data in ShopAgent:

1. **The Ledger (Postgres):** Exact data — revenue, counts, averages
   Question: "Faturamento de SP?" -> SELECT SUM(total) -> R$ 127.430
   
2. **The Memory (Qdrant):** Meaning — complaints, sentiment, themes  
   Question: "Quem reclama de entrega?" -> semantic search -> reviews

Why two stores? Because "demorou 15 dias" = "nao recebi" = "entrega atrasada" — 
SQL can't find this, but vector similarity can.

Give 3 example questions for each store and 2 that need BOTH.
