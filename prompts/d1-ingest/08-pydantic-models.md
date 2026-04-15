Read gen/init.sql and gen/shadowtraffic.json. Create Pydantic BaseModel classes
for all 4 ShopAgent entities in src/day1/models.py:

- Customer (customer_id, name, email, city, state, segment)
- Product (product_id, name, category, price, brand)
- Order (order_id, customer_id, product_id, qty, total, status, payment, created_at)
- Review (review_id, order_id, rating, comment, sentiment)

Use Field validators matching the DB constraints: qty 1-10, total >= 0,
rating 1-5. Use Literal types for status, payment, segment, and sentiment
matching exactly the CHECK constraints in init.sql.
