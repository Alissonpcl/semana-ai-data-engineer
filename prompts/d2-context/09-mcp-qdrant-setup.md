Configure MCP Qdrant to connect Claude Code to The Memory:

Add to your Claude Code MCP settings:
```json
{
  "mcpServers": {
    "qdrant": {
      "command": "uvx",
      "args": ["mcp-server-qdrant"],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "COLLECTION_NAME": "shopagent_reviews"
      }
    }
  }
}
```

Then ask Claude Code: "Quais clientes reclamam de entrega atrasada?"
Claude should search Qdrant semantically and return real review matches.
