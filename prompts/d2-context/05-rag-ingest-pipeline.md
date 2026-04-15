Create the RAG ingest pipeline in src/day2/ingest_reviews.py:

1. Use LlamaIndex JSONReader to load gen/data/reviews/reviews.jsonl
2. Use FastEmbedEmbedding (BAAI/bge-base-en-v1.5) — local, no API key needed
3. Connect to Qdrant at localhost:6333, collection "shopagent_reviews"
4. Build VectorStoreIndex from the documents with StorageContext
5. Show progress during indexing

This creates The Memory — reviews as vectors ready for semantic search.
Run it and confirm the collection exists in Qdrant.
