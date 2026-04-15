Configure MCP Postgres to connect Claude Code to The Ledger:

Add to your Claude Code MCP settings:
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://shopagent:shopagent@localhost:5432/shopagent"
      ]
    }
  }
}
```

Then ask Claude Code: "Qual o faturamento total por estado?"
Claude should execute SQL via MCP and return real results — not hallucinated ones.

Note: On Day 4 we migrate to Supabase Cloud, which has its own MCP server.
