Today you built ONE agent that decides between two tools.
But what if there were THREE specialized agents instead?

Think about:
1. AnalystAgent -- only does SQL, expert in revenue/orders/metrics
2. ResearchAgent -- only does semantic search, expert in reviews/sentiment
3. ReporterAgent -- combines both results into an executive report

What changes?
- Each agent is simpler and more focused
- They can work in parallel
- The ReporterAgent synthesizes without querying anything
- You need an orchestrator to coordinate them

Tomorrow: CrewAI builds this multi-agent team. Same data, 3x smarter.
