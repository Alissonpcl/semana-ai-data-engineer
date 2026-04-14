# E-Commerce Postgres

> **Purpose**: Complete ShopAgent e-commerce data generation — customers+products+orders→Postgres, reviews→JSONL via schedule.stages
> **MCP Validated**: 2026-04-14

## When to Use

- ShopAgent Day 1 data pipeline setup
- Generating relational e-commerce data with foreign key dependencies
- Producing both structured (SQL-queryable) and unstructured (text for RAG) data
- Workshop environment with clean-reset capability

## Implementation

```json
{
  "generators": [
    {
      "name": "customers",
      "connection": "pg",
      "table": "customers",
      "row": {
        "customer_id": { "_gen": "uuid" },
        "name": { "_gen": "string", "expr": "#{Name.fullName}" },
        "email": { "_gen": "string", "expr": "#{Internet.emailAddress}" },
        "city": { "_gen": "string", "expr": "#{Address.city}" },
        "state": {
          "_gen": "oneOf",
          "choices": ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "PE"]
        },
        "segment": {
          "_gen": "oneOf",
          "choices": ["premium", "standard", "basic"]
        }
      },
      "localConfigs": { "maxEvents": 500, "throttle": {"ms": 0} }
    },
    {
      "name": "products",
      "connection": "pg",
      "table": "products",
      "row": {
        "product_id": { "_gen": "uuid" },
        "name": { "_gen": "string", "expr": "#{Commerce.productName}" },
        "category": { "_gen": "string", "expr": "#{Commerce.department}" },
        "price": {
          "_gen": "uniformDistribution",
          "bounds": [19.90, 999.90],
          "decimals": 2
        },
        "brand": { "_gen": "string", "expr": "#{Company.name}" }
      },
      "localConfigs": { "maxEvents": 200, "throttle": {"ms": 0} }
    },
    {
      "name": "orders",
      "connection": "pg",
      "table": "orders",
      "row": {
        "order_id": { "_gen": "uuid" },
        "customer_id": {
          "_gen": "lookup",
          "table": "customers",
          "path": ["row", "customer_id"]
        },
        "product_id": {
          "_gen": "lookup",
          "table": "products",
          "path": ["row", "product_id"]
        },
        "qty": {
          "_gen": "uniformDistribution",
          "bounds": [1, 10],
          "decimals": 0
        },
        "total": {
          "_gen": "uniformDistribution",
          "bounds": [29.90, 999.90],
          "decimals": 2
        },
        "status": {
          "_gen": "weightedOneOf",
          "choices": [
            {"weight": 0.50, "value": "delivered"},
            {"weight": 0.20, "value": "shipped"},
            {"weight": 0.20, "value": "processing"},
            {"weight": 0.10, "value": "cancelled"}
          ]
        },
        "payment": {
          "_gen": "weightedOneOf",
          "choices": [
            {"weight": 0.45, "value": "pix"},
            {"weight": 0.40, "value": "credit_card"},
            {"weight": 0.15, "value": "boleto"}
          ]
        },
        "created_at": { "_gen": "now" }
      },
      "localConfigs": { "maxEvents": 5000, "throttle": {"ms": 100} }
    },
    {
      "name": "reviews",
      "connection": "fs",
      "directory": "/data/reviews",
      "data": {
        "review_id": { "_gen": "uuid" },
        "order_id": {
          "_gen": "lookup",
          "connection": "pg",
          "table": "orders",
          "path": ["row", "order_id"]
        },
        "rating": {
          "_gen": "weightedOneOf",
          "choices": [
            {"weight": 0.05, "value": 1},
            {"weight": 0.10, "value": 2},
            {"weight": 0.20, "value": 3},
            {"weight": 0.30, "value": 4},
            {"weight": 0.35, "value": 5}
          ]
        },
        "comment": {
          "_gen": "oneOf",
          "choices": [
            "Produto chegou antes do prazo, estou muito satisfeito com a compra.",
            "Entrega atrasou mais de 10 dias, nao recebi nenhuma notificacao.",
            "O produto e exatamente como descrito na foto, otima qualidade.",
            "Frete absurdamente caro, quase o dobro do valor do produto.",
            "Ate hoje nao recebi meu pedido, faz 20 dias que comprei.",
            "Superou todas as minhas expectativas, recomendo muito.",
            "Produto chegou danificado, a embalagem estava completamente amassada.",
            "Atendimento ao cliente pessimo, ninguem resolve o problema.",
            "Entrega rapida e produto de otima qualidade, voltarei a comprar.",
            "O produto veio diferente da foto, cor totalmente errada.",
            "Demorou 15 dias para chegar, mas o produto e bom.",
            "Excelente custo-beneficio, produto de qualidade por um preco justo.",
            "Nao recebi o produto e o suporte nao responde meus chamados.",
            "Produto danificado na entrega, pedi reembolso mas nao obtive resposta.",
            "Chegou no prazo, embalagem bem protegida, produto perfeito.",
            "O frete demorou mais do que o esperado, porem o produto e bom.",
            "Comprei ha 3 semanas e ainda esta como pedido em processamento.",
            "Qualidade excelente, bem melhor do que esperava pelo preco.",
            "Produto veio com defeito de fabricacao, muito decepcionante.",
            "Entrega super rapida, recebi em 2 dias uteis. Recomendo o vendedor.",
            "O material e fraco, nao vale o preco que foi cobrado.",
            "Otimo produto, ja e minha segunda compra e continua me surpreendendo.",
            "A entrega estava prevista para sexta e chegou apenas na quarta da semana seguinte.",
            "Produto identico ao anunciado, funcionando perfeitamente.",
            "Tive que abrir disputa pois o produto nunca chegou no endereco.",
            "Muito bom, superou as expectativas em termos de qualidade e acabamento.",
            "Embalagem chegou aberta e produto com sinais de uso, inaceitavel.",
            "Rapido, seguro e produto de alta qualidade. Nota maxima.",
            "O vendedor nao fornece rastreamento atualizado, ficou dias sem movimentacao.",
            "Produto fantastico, vale cada centavo investido na compra."
          ]
        },
        "sentiment": {
          "_gen": "weightedOneOf",
          "choices": [
            {"weight": 0.35, "value": "positive"},
            {"weight": 0.30, "value": "neutral"},
            {"weight": 0.35, "value": "negative"}
          ]
        }
      },
      "localConfigs": { "maxEvents": 500, "throttle": {"ms": 500} },
      "fileConfigs": { "filePrefix": "reviews-", "format": "jsonl" }
    }
  ],
  "connections": {
    "pg": {
      "kind": "postgres",
      "connectionConfigs": {
        "host": "postgres",
        "port": 5432,
        "db": "shopagent",
        "username": "shopagent",
        "password": "shopagent"
      },
      "tablePolicy": "dropAndCreate"
    },
    "fs": {
      "kind": "fileSystem"
    }
  },
  "schedule": {
    "stages": [
      {
        "generators": ["customers", "products"],
        "comment": "Stage 0: Seed parent tables first (500 customers + 200 products)"
      },
      {
        "generators": ["orders", "reviews"],
        "comment": "Stage 1: Stream orders with FK lookups + reviews to JSONL"
      }
    ]
  }
}
```

## Configuration

| Entity | maxEvents | Throttle | Destination | Notes |
|--------|-----------|----------|-------------|-------|
| customers | 500 | `{"ms": 0}` | Postgres | Seeded in stage 0 |
| products | 200 | `{"ms": 0}` | Postgres | Seeded in stage 0 |
| orders | 5000 | `{"ms": 100}` | Postgres | Finite seeding in stage 1 with lookup FKs |
| reviews | 500 | `{"ms": 500}` | JSONL file | Finite; cross-connection lookup (fs→pg); ingested by LlamaIndex on Day 2 |

## Key Design Decisions

- **`name` + `connection` required**: both connections (`pg`, `fs`) are defined, so every generator must declare which connection it uses and a name for stage references.
- **Curated comments over Faker**: `#{Lorem.paragraph}` produces generic Latin text. The `oneOf` list uses realistic Portuguese e-commerce complaints and compliments — better signal for RAG/sentiment analysis on Day 2.
- **Finite `maxEvents` for both streaming stages**: reproducible dataset size for workshop; avoids unbounded growth in local Docker.
- **Cross-connection lookup in reviews**: reviews generator uses `fs` connection but looks up `order_id` from a `pg` generator — requires explicit `"connection": "pg"` in the lookup.

## Example Usage

```bash
# Dev mode — dry run to stdout
docker run --env-file .env \
  -v $(pwd)/shadowtraffic.json:/home/config.json \
  shadowtraffic/shadowtraffic:latest \
  --config /home/config.json --sample 10 --stdout

# Production — stream to Postgres + filesystem
docker compose up
```

## See Also

- [Staged Seeding](../patterns/staged-seeding.md)
- [Connections](../concepts/connections.md)
- [Functions](../concepts/functions.md)
- [Faker Expressions](../concepts/faker-expressions.md)
