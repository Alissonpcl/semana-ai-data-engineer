Use AgentSpec to design the full architecture:

/agentspec:design SHOPAGENT

Review the generated design:
1. File manifest -- does it include tools.py, agent.py, chainlit_app.py?
2. Pipeline architecture -- is the ReAct loop correct?
3. Delegation map -- which specialist agents will build each component?
4. Does it connect to existing Day 2 infrastructure? (Postgres on 5432, Qdrant on 6333)

This is the blueprint. Tomorrow we'll use AgentSpec to build the multi-agent version.
