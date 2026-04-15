"""ShopAgent Day 2 — The Ledger: Postgres business queries."""

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def get_connection():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=int(os.environ.get("POSTGRES_PORT", 5432)),
        dbname=os.environ.get("POSTGRES_DB", "shopagent"),
        user=os.environ.get("POSTGRES_USER", "shopagent"),
        password=os.environ.get("POSTGRES_PASSWORD", "shopagent"),
    )


QUERIES = {
    "revenue_by_state": """
        SELECT c.state, COUNT(o.order_id) AS pedidos, SUM(o.total) AS faturamento
        FROM orders o JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.state ORDER BY faturamento DESC
    """,
    "orders_by_status": """
        SELECT status, COUNT(*) AS total, SUM(total) AS faturamento,
               ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pct
        FROM orders GROUP BY status ORDER BY total DESC
    """,
    "top_products": """
        SELECT p.name, p.category, p.brand,
               COUNT(o.order_id) AS pedidos, SUM(o.total) AS faturamento
        FROM orders o JOIN products p ON o.product_id = p.product_id
        GROUP BY p.product_id, p.name, p.category, p.brand
        ORDER BY faturamento DESC LIMIT 10
    """,
    "payment_distribution": """
        SELECT payment, COUNT(*) AS total,
               ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pct
        FROM orders GROUP BY payment ORDER BY total DESC
    """,
    "segment_analysis": """
        SELECT c.segment, COUNT(DISTINCT c.customer_id) AS clientes,
               COUNT(o.order_id) AS pedidos, ROUND(AVG(o.total), 2) AS ticket_medio
        FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.segment ORDER BY ticket_medio DESC
    """,
}


def run_query(name: str) -> list[tuple]:
    sql = QUERIES[name]
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return columns, rows
    finally:
        conn.close()


if __name__ == "__main__":
    for name in QUERIES:
        print(f"\n{'='*60}")
        print(f"  {name.upper().replace('_', ' ')}")
        print(f"{'='*60}")
        columns, rows = run_query(name)
        header = " | ".join(f"{c:>15}" for c in columns)
        print(header)
        print("-" * len(header))
        for row in rows[:10]:
            print(" | ".join(f"{str(v):>15}" for v in row))
