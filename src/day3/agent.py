"""ShopAgent Day 3 — LangChain ReAct agent with autonomous dual-store routing."""

import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from day3.tools import qdrant_semantic_search, supabase_execute_sql

SYSTEM_PROMPT = """Voce e o ShopAgent, um analista de dados de e-commerce autonomo e inteligente.

Voce tem acesso a duas fontes de dados:

1. **The Ledger (Postgres)** — Dados exatos: faturamento, contagens, medias, totais.
   Use a ferramenta `supabase_execute_sql` para perguntas sobre numeros, metricas e agregacoes.

2. **The Memory (Qdrant)** — Significado: opinoes, reclamacoes, sentimentos dos clientes.
   Use a ferramenta `qdrant_semantic_search` para perguntas sobre o que os clientes dizem ou sentem.

Regras:
- Decida autonomamente qual ferramenta usar com base na pergunta.
- Se a pergunta exigir dados de ambas as fontes, use as duas ferramentas em sequencia.
- Responda sempre em portugues brasileiro.
- Apresente os dados de forma clara e organizada.
- Quando usar dados numericos, inclua os valores exatos retornados.
- Quando usar reviews, cite trechos relevantes como evidencia.
"""


def create_shopagent() -> object:
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0,
        streaming=True,
    )
    agent = create_react_agent(
        model=llm,
        tools=[supabase_execute_sql, qdrant_semantic_search],
        prompt=SYSTEM_PROMPT,
    )
    return agent


def run_agent(question: str) -> str:
    agent = create_shopagent()
    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    return result["messages"][-1].content


if __name__ == "__main__":
    demo_questions = [
        "Qual o faturamento total por estado?",
        "Clientes reclamando de entrega atrasada",
        "Clientes premium do Sudeste que reclamam: qual o ticket medio?",
    ]

    for question in demo_questions:
        print(f"\n{'='*60}")
        print(f"  Q: {question}")
        print(f"{'='*60}")
        answer = run_agent(question)
        print(f"\n  A: {answer}")
