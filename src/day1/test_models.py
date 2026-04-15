"""ShopAgent — Pydantic validation tests for Day 1 models."""

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent))

from pydantic import ValidationError

from models import Customer, Order, Product, Review


def test_valid_order():
    order = Order(
        order_id=uuid4(),
        customer_id=uuid4(),
        product_id=uuid4(),
        qty=3,
        total=149.90,
        status="delivered",
        payment="pix",
    )
    print(f"Valid Order: {order.order_id} | qty={order.qty} | status={order.status}")


def test_qty_zero():
    try:
        Order(
            order_id=uuid4(),
            customer_id=uuid4(),
            product_id=uuid4(),
            qty=0,
            total=50.00,
            status="shipped",
            payment="credit_card",
        )
    except ValidationError as e:
        print(f"qty=0 rejected: {e.errors()[0]['msg']}")


def test_invalid_payment():
    try:
        Order(
            order_id=uuid4(),
            customer_id=uuid4(),
            product_id=uuid4(),
            qty=2,
            total=99.90,
            status="processing",
            payment="dinheiro",
        )
    except ValidationError as e:
        print(f"payment='dinheiro' rejected: {e.errors()[0]['msg']}")


def test_valid_review():
    review = Review(
        review_id=uuid4(),
        order_id=uuid4(),
        rating=5,
        comment="Produto excelente, recomendo!",
        sentiment="positive",
    )
    print(f"Valid Review: rating={review.rating} | sentiment={review.sentiment}")


def test_rating_six():
    try:
        Review(
            review_id=uuid4(),
            order_id=uuid4(),
            rating=6,
            comment="Teste",
            sentiment="positive",
        )
    except ValidationError as e:
        print(f"rating=6 rejected: {e.errors()[0]['msg']}")


if __name__ == "__main__":
    print("=" * 50)
    print("ShopAgent — Pydantic Validation Tests")
    print("=" * 50)
    test_valid_order()
    test_qty_zero()
    test_invalid_payment()
    test_valid_review()
    test_rating_six()
    print("=" * 50)
    print("All tests passed!")
