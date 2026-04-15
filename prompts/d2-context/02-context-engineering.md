Read gen/init.sql and give Claude the schema as context. Now ask again:
"Gere uma query SQL para faturamento total por estado."

Use this system prompt approach:
- Include the table schemas (customers, products, orders)
- Add an example: "Pedidos por pix?" -> SELECT COUNT(*) FROM orders WHERE payment='pix'
- Add constraints: "Use only these tables. Never invent data."

Claude generates correct SQL now — but still can't EXECUTE it.
That's the limit of Context Engineering without tool access.
