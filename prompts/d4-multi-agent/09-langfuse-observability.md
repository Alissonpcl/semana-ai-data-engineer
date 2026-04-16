Add LangFuse tracing to the crew in src/day4/crew.py:

1. Set LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST in .env
2. Initialize the LangFuse callback handler
3. Pass it to the CrewAI agents as a callback

Run the crew again and open the LangFuse dashboard. You should see:
- Each agent as a separate trace span
- Token usage per agent (analyst uses more on SQL generation)
- Latency breakdown (which agent is the bottleneck?)
- Total cost of the full crew execution

This is LLMOps: you don't guess performance, you measure it.
