Run the crew with a complex question that needs ALL 3 agents:

"Faca uma analise completa de satisfacao dos clientes por regiao, incluindo faturamento,
principais reclamacoes e um plano de acao para melhorar a experiencia."

Watch the sequential flow:
1. AnalystAgent writes SQL -> revenue by state, order counts, avg ticket
2. ResearchAgent searches vectors -> complaint themes by region
3. ReporterAgent synthesizes -> executive report with data + insights + actions

This is the power: one question, three specialists, one coherent report.
Try another: "Quais produtos tem mais reclamacao e qual o impacto no faturamento?"
