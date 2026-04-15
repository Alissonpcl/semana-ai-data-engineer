"""ShopAgent Day 2 — Ingest reviews JSONL into Qdrant (The Memory)."""

import os
from pathlib import Path

import qdrant_client
from dotenv import load_dotenv
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.anthropic import Anthropic
from llama_index.readers.json import JSONReader
from llama_index.vector_stores.qdrant import QdrantVectorStore

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

Settings.llm = Anthropic(model="claude-sonnet-4-20250514")


def ingest_reviews(
    jsonl_path: str | None = None,
    qdrant_url: str | None = None,
    collection_name: str | None = None,
) -> VectorStoreIndex:
    jsonl_path = jsonl_path or str(PROJECT_ROOT / "gen" / "data" / "reviews" / "reviews.jsonl")
    qdrant_url = qdrant_url or os.environ.get("QDRANT_URL", "http://localhost:6333")
    collection_name = collection_name or os.environ.get("QDRANT_COLLECTION", "shopagent_reviews")

    Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")

    reader = JSONReader(is_jsonl=True, clean_json=True)
    documents = reader.load_data(input_file=jsonl_path)
    print(f"Loaded {len(documents)} reviews from {Path(jsonl_path).name}")

    client = qdrant_client.QdrantClient(url=qdrant_url)
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, show_progress=True,
    )
    print(f"Indexed {len(documents)} reviews into Qdrant '{collection_name}'")

    return index


if __name__ == "__main__":
    index = ingest_reviews()

    engine = index.as_query_engine(similarity_top_k=5)
    response = engine.query("Clientes reclamando de entrega")
    print(f"\nTest query: 'Clientes reclamando de entrega'")
    print(f"Answer: {response.response}")
    print(f"\nSources ({len(response.source_nodes)} chunks):")
    for node in response.source_nodes:
        print(f"  [{node.score:.3f}] {node.text[:100]}...")
