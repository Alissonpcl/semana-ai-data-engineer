# Generators

> **Purpose**: Define what data ShadowTraffic produces and where it goes
> **Confidence**: 0.95
> **MCP Validated**: 2026-04-14

## Overview

A generator is the fundamental unit of ShadowTraffic. It declares the shape of data — fields with `_gen` functions — and which connection receives the output. The field names vary by connection type: `table`/`row` for Postgres, `topic`/`value` for Kafka, `directory`/`data` for filesystem.

## The Pattern

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
        "segment": { "_gen": "oneOf", "choices": ["premium", "standard", "basic"] }
      },
      "localConfigs": {
        "throttle": {"ms": 100},
        "maxEvents": 500
      }
    },
    {
      "name": "reviews",
      "connection": "fs",
      "directory": "/data/reviews",
      "data": {
        "review_id": { "_gen": "uuid" },
        "comment": { "_gen": "string", "expr": "#{Lorem.paragraph}" }
      },
      "localConfigs": {
        "throttle": {"ms": 500}
      },
      "fileConfigs": {
        "filePrefix": "reviews-",
        "format": "jsonl"
      }
    }
  ]
}
```

## Quick Reference

| Field | Connection | Description |
|-------|-----------|-------------|
| `name` | All | Generator identifier — required by `schedule.stages` and cross-generator lookups when multiple connections exist |
| `connection` | All | Key of the connection to use (e.g., `"pg"`, `"fs"`) — required when multiple connections are defined |
| `table` | Postgres | Target table name |
| `row` | Postgres | Object with field generators |
| `topic` | Kafka | Target topic name |
| `value` | Kafka | Message payload with field generators |
| `directory` | Filesystem | Output directory path |
| `data` | Filesystem | Record object with field generators |
| `localConfigs.throttle` | All | Object `{"ms": N}` — delay between events (0ms = no delay) |
| `localConfigs.maxEvents` | All | Stop after N events (omit for continuous) |
| `fileConfigs.filePrefix` | Filesystem | Output filename prefix (e.g., `"reviews-"`) |
| `fileConfigs.format` | Filesystem | Output format: `"json"`, `"jsonl"`, `"parquet"`, `"log"` |

## Common Mistakes

### Wrong — missing `name` and `connection` with multiple connections

```json
{
  "table": "customers",
  "row": { "name": { "_gen": "string", "expr": "#{Name.fullName}" } },
  "localConfigs": { "throttle": 0 }
}
```

When multiple connections exist, each generator must declare `name` and `connection`. Without `name`, `schedule.stages` cannot reference it. Without `connection`, routing is ambiguous.

### Correct

```json
{
  "name": "customers",
  "connection": "pg",
  "table": "customers",
  "row": { "name": { "_gen": "string", "expr": "#{Name.fullName}" } },
  "localConfigs": { "throttle": {"ms": 0} }
}
```

### Wrong — throttle as plain integer

```json
"localConfigs": { "throttle": 100 }
```

### Correct — throttle as object

```json
"localConfigs": { "throttle": {"ms": 100} }
```

### Wrong — fileConfigs with fileName

```json
"fileConfigs": { "fileName": "reviews.jsonl" }
```

### Correct — fileConfigs with filePrefix + format

```json
"fileConfigs": { "filePrefix": "reviews-", "format": "jsonl" }
```

## Related

- [Connections](../concepts/connections.md)
- [Functions](../concepts/functions.md)
- [E-Commerce Postgres Pattern](../patterns/ecommerce-postgres.md)
