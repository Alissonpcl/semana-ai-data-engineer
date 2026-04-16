"""ShopAgent Day 3 — Chainlit app with full-trace LangGraph streaming."""

import chainlit as cl

from src.day3.agent import create_agent

WELCOME_MESSAGE = """**ShopAgent conectado!** Eu tenho acesso a dois stores de dados:

**The Ledger (Postgres)** — Dados exatos: faturamento, pedidos, clientes, produtos
**The Memory (Qdrant)** — Significado: reviews, reclamacoes, sentimentos

Pergunte qualquer coisa sobre o e-commerce e eu decido automaticamente qual store consultar.

Exemplos:
- "Qual o faturamento total por estado?"
- "Quais clientes reclamam de entrega atrasada?"
- "Top 3 estados com mais reclamacoes e seu faturamento"
"""

TOOL_DISPLAY_NAMES = {
    "execute_sql": "The Ledger (SQL)",
    "semantic_search": "The Memory (Qdrant)",
}


@cl.on_chat_start
async def start():
    agent = create_agent(streaming=True)
    cl.user_session.set("agent", agent)
    await cl.Message(content=WELCOME_MESSAGE).send()


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    msg = cl.Message(content="")
    tool_steps: dict[str, cl.Step] = {}

    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": message.content}]},
        version="v2",
    ):
        kind = event["event"]

        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if hasattr(chunk, "content") and isinstance(chunk.content, str) and chunk.content:
                await msg.stream_token(chunk.content)

        elif kind == "on_tool_start":
            tool_name = event["name"]
            display_name = TOOL_DISPLAY_NAMES.get(tool_name, tool_name)
            step = cl.Step(name=display_name, type="tool")
            await step.__aenter__()
            step.input = str(event["data"].get("input", ""))
            tool_steps[event["run_id"]] = step

        elif kind == "on_tool_end":
            step = tool_steps.pop(event["run_id"], None)
            if step:
                output = str(event["data"].get("output", ""))
                step.output = output[:1000]
                await step.__aexit__(None, None, None)

    await msg.send()
