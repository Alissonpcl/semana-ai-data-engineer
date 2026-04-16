-- ShopAgent — Postgres schema (customers, products, orders)
-- Semana AI Data Engineer 2026

CREATE TABLE IF NOT EXISTS customers (
    customer_id UUID PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    email       VARCHAR(255) NOT NULL,
    city        VARCHAR(100),
    state       CHAR(2),
    segment     VARCHAR(20) CHECK (segment IN ('premium', 'standard', 'basic'))
);

CREATE TABLE IF NOT EXISTS products (
    product_id UUID PRIMARY KEY,
    name       VARCHAR(255) NOT NULL,
    category   VARCHAR(100) NOT NULL,
    price      DECIMAL(10,2) NOT NULL CHECK (price > 0),
    brand      VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id    UUID PRIMARY KEY,
    customer_id UUID NOT NULL REFERENCES customers(customer_id),
    product_id  UUID NOT NULL REFERENCES products(product_id),
    qty         INTEGER      CHECK (qty BETWEEN 1 AND 10),
    total       DECIMAL(10,2) CHECK (total >= 0),
    status      VARCHAR(20)  CHECK (status IN ('delivered', 'shipped', 'processing', 'cancelled')),
    payment     VARCHAR(20)  CHECK (payment IN ('pix', 'credit_card', 'boleto')),
    created_at  TIMESTAMPTZ  DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id  ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_product_id   ON orders(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_status       ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_payment      ON orders(payment);
CREATE INDEX IF NOT EXISTS idx_customers_state     ON customers(state);
CREATE INDEX IF NOT EXISTS idx_customers_segment   ON customers(segment);
CREATE INDEX IF NOT EXISTS idx_orders_created_at   ON orders(created_at);
