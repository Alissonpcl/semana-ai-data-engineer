Create the CrewAI crew in src/day4/crew.py:

1. Use the @CrewBase decorator with inline agent/task definitions (no YAML files needed)
2. Create 3 agents: analyst (with sql tool), researcher (with qdrant tool), reporter (no tools)
3. Create 3 tasks linked to their agents, sequential order
4. The report_task should use context=[analysis_task, research_task] to get both results
5. Build the Crew with process=Process.sequential and Claude as LLM
6. Add a run_crew() function that takes a question and calls crew.kickoff()

Use anthropic/claude-sonnet-4-20250514 as the LLM model string.
The crew should accept dynamic input via {question} placeholder in task descriptions.
Run it with: python src/day4/crew.py
