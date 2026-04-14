# Functions

> **Purpose**: Built-in _gen functions that produce realistic synthetic values
> **Confidence**: 0.95
> **MCP Validated**: 2026-04-14

## Overview

Every field in a ShadowTraffic generator uses `{"_gen": "functionName", ...params}` to produce data. Functions range from simple scalars (uuid, boolean) to relational references (lookup) and text generation (string with Faker expressions). Function modifiers like `decimals` and `cast` control output formatting.

## The Pattern

```json
{
  "name": "orders",
  "connection": "pg",
  "table": "orders",
  "row": {
    "order_id": { "_gen": "uuid" },
    "customer_id": { "_gen": "lookup", "table": "customers", "path": ["row", "customer_id"] },
    "total": { "_gen": "uniformDistribution", "bounds": [29.90, 999.90], "decimals": 2 },
    "qty": { "_gen": "uniformDistribution", "bounds": [1, 10], "decimals": 0 },
    "status": {
      "_gen": "weightedOneOf",
      "choices": [
        {"weight": 0.50, "value": "delivered"},
        {"weight": 0.20, "value": "shipped"},
        {"weight": 0.20, "value": "processing"},
        {"weight": 0.10, "value": "cancelled"}
      ]
    },
    "payment": { "_gen": "oneOf", "choices": ["pix", "credit_card", "boleto"] },
    "note": { "_gen": "string", "expr": "Order for #{Name.firstName}" },
    "created_at": { "_gen": "now" }
  }
}
```

## Quick Reference

| Function | Required Params | Output | Notes |
|----------|----------------|--------|-------|
| `uuid` | — | UUID string | `"a1b2c3d4-..."` |
| `oneOf` | `choices[]` | Random element | Uniform distribution; choices can be raw primitives |
| `weightedOneOf` | `choices[]` | Weighted pick | Each choice is `{"weight": N, "value": V}` — no separate weights array |
| `uniformDistribution` | `bounds:[min,max]` | Random float | Use `decimals` to control precision |
| `normalDistribution` | `mean`, `sd` | Gaussian float | Bell curve around mean |
| `lookup` | `table`/`topic`, `path[]` | Value from another generator | Postgres: `table`; Kafka: `topic`; cross-connection: add `connection` key |
| `string` | `expr` | Faker-templated text | Uses `#{Namespace.method}` syntax |
| `var` | `var` | Named variable value | Reference `vars` block in same generator |
| `now` | `offset` (optional) | ISO timestamp | Offset in ms (e.g., -86400000 = yesterday) |
| `boolean` | — | true/false | Random boolean |
| `sequentialInteger` | `start` (optional) | Auto-increment int | Starts at 0 by default |

## Lookup Reference by Connection Type

| Referenced Generator | Lookup Key | Example |
|----------------------|------------|---------|
| Postgres (`table`) | `"table": "customers"` | `{ "_gen": "lookup", "table": "customers", "path": ["row", "customer_id"] }` |
| Kafka (`topic`) | `"topic": "events"` | `{ "_gen": "lookup", "topic": "events", "path": ["value", "user_id"] }` |
| Cross-connection | `"connection"` + `"table"` | `{ "_gen": "lookup", "connection": "pg", "table": "orders", "path": ["row", "order_id"] }` |

**Rule 1**: use `table` (not `topic`) when the referenced generator writes to Postgres.
**Rule 2**: add `"connection": "<name>"` when the lookup crosses connection types (e.g., a filesystem generator referencing a Postgres generator).
**Rule 3**: `path` must be an array starting with the shape key of the referenced generator (`"row"` for Postgres, `"value"` for Kafka, `"data"` for filesystem).

## Common Mistakes

### Wrong — `topic` used for Postgres lookup

```json
{ "_gen": "lookup", "topic": "customers", "path": ["row", "customer_id"] }
```

`topic` is for Kafka generators. For Postgres use `table`.

### Correct — same-connection Postgres lookup

```json
{ "_gen": "lookup", "table": "customers", "path": ["row", "customer_id"] }
```

### Wrong — `weightedOneOf` with parallel arrays

```json
{
  "_gen": "weightedOneOf",
  "choices": ["delivered", "shipped"],
  "weights": [0.80, 0.20]
}
```

### Correct — `weightedOneOf` with object choices

```json
{
  "_gen": "weightedOneOf",
  "choices": [
    {"weight": 0.80, "value": "delivered"},
    {"weight": 0.20, "value": "shipped"}
  ]
}
```

## Related

- [Faker Expressions](../concepts/faker-expressions.md)
- [Generators](../concepts/generators.md)
- [Staged Seeding](../patterns/staged-seeding.md)
