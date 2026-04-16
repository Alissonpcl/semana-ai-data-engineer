Use the AgentSpec pattern to generate the full CrewAI project structure:

Create the following files in src/day4/:
1. agents.yaml — defines the 3 agents (analyst, researcher, reporter) with role, goal, backstory
2. tasks.yaml — defines 3 tasks: data_analysis, experience_research, executive_report
3. crew.py — orchestrates agents + tasks in sequential process
4. tools.py — supabase_execute_sql and qdrant_semantic_search tools

Each agent.yaml entry should have: role, goal, backstory (in Portuguese, professional tone).
Each task should reference which agent executes it and what output is expected.
