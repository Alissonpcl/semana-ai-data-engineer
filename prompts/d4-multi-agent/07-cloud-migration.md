Migrate from Docker to cloud — same code, different URLs.

1. In .env, change SUPABASE_DB_URL from localhost to your Supabase Cloud connection string
2. In .env, change QDRANT_URL from localhost:6333 to your Qdrant Cloud URL
3. Add QDRANT_API_KEY for cloud authentication

That's it. No code changes. The tools read from env vars, so the agents work
the same way — but now against cloud infrastructure.

Run the same complex question from prompt 06 and confirm identical behavior.
This is why environment-based config matters: local dev, cloud prod, zero code changes.
