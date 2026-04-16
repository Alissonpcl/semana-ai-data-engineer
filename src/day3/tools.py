"""ShopAgent Day 3 — LangChain tools for The Ledger (SQL) and The Memory (semantic)."""

import os
from pathlib import Path

import psycopg2
import qdrant_client
from dotenv import load_dotenv
from langchain_core.tools import tool
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.anthropic import Anthropic
from llama_index.vector_stores.qdrant import QdrantVectorStore

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

_llama_settings_initialized = False


def _configure_llama_settings() -> None:
    global _llama_settings_initialized
    if _llama_settings_initialized:
        return
    Settings.llm = Anthropic(model="claude-sonnet-4-20250514")
    Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")
    _llama_settings_initialized = True


def _get_postgres_connection():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=int(os.environ.get("POSTGRES_PORT", 5432)),
        dbname=os.environ.get("POSTGRES_DB", "shopagent"),
        user=os.environ.get("POSTGRES_USER", "shopagent"),
        password=os.environ.get("POSTGRES_PASSWORD", "shopagent"),
    )


@tool
def execute_sql(query: str) -> str:
    """Execute SQL query against Postgres (The Ledger) for EXACT data.

    Use when the question asks for specific numbers, totals, or structured data:
    - Faturamento (revenue) by state, category, or period
    - Total de pedidos (order counts), ticket medio (average order value)
    - Payment method distribution, customer segment analysis
    - Any question requiring aggregation, GROUP BY, or JOINs

    Args:
        query: Valid SELECT SQL query for the shopagent database.
    """
    conn = _get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
        result_lines = [" | ".join(columns)]
        for row in rows:
            result_lines.append(" | ".join(str(v) for v in row))
        return "\n".join(result_lines)
    except Exception as e:
        return f"SQL Error: {e}"
    finally:
        conn.close()


@tool
def semantic_search(question: str) -> str:
    """Search customer reviews by MEANING using Qdrant vector database (The Memory).

    Use when the question asks about opinions, complaints, or text patterns:
    - Reclamacoes (complaints) about delivery, quality, price
    - Customer sentiment analysis (positive, negative, neutral)
    - Product feedback themes and review patterns
    - Any question about what customers SAY, THINK, or FEEL

    Args:
        question: Natural language question for semantic similarity search.
    """
    _configure_llama_settings()
    qdrant_url = os.environ.get("QDRANT_URL", "http://localhost:6333")
    collection_name = os.environ.get("QDRANT_COLLECTION", "shopagent_reviews")

    try:
        client = qdrant_client.QdrantClient(url=qdrant_url)
        vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
        index = VectorStoreIndex.from_vector_store(vector_store)
        engine = index.as_query_engine(similarity_top_k=5)
        response = engine.query(question)

        result_parts = [f"Resposta: {response.response}"]
        if response.source_nodes:
            result_parts.append(f"\nFontes ({len(response.source_nodes)} reviews):")
            for node in response.source_nodes:
                score = f"[{node.score:.3f}]" if node.score else ""
                result_parts.append(f"  {score} {node.text[:200]}")
        return "\n".join(result_parts)
    except Exception as e:
        return f"Semantic Search Error: {e}"
