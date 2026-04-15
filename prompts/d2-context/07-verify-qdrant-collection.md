Verify the Qdrant collection was created correctly:

1. Call GET http://localhost:6333/collections/shopagent_reviews
2. Check: vector size (should be 768 for bge-base-en-v1.5), point count, distance metric
3. Search for a sample point and inspect its payload
4. Compare: how many reviews in JSONL vs how many points in Qdrant?
