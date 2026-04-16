"""ShopAgent — Pydantic validation tests for Day 1 models."""

from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from models import Customer, Order, Product, Review


def test_valid_order():
    order = Order(
        order_id=uuid4(),
        customer_id=uuid4(),
        product_id=uuid4(),
        qty=3,
        total=Decimal("149.90"),
        status="delivered",
        payment="pix",
    )
    assert order.qty == 3
    assert order.status == "delivered"


def test_qty_zero_rejected():
    with pytest.raises(ValidationError):
        Order(
            order_id=uuid4(),
            customer_id=uuid4(),
            product_id=uuid4(),
            qty=0,
            total=Decimal("50.00"),
            status="shipped",
            payment="credit_card",
        )


def test_invalid_payment_rejected():
    with pytest.raises(ValidationError):
        Order(
            order_id=uuid4(),
            customer_id=uuid4(),
            product_id=uuid4(),
            qty=2,
            total=Decimal("99.90"),
            status="processing",
            payment="dinheiro",
        )


def test_valid_review():
    review = Review(
        review_id=uuid4(),
        order_id=uuid4(),
        rating=5,
        comment="Produto excelente, recomendo!",
        sentiment="positive",
    )
    assert review.rating == 5
    assert review.sentiment == "positive"


def test_rating_above_max_rejected():
    with pytest.raises(ValidationError):
        Review(
            review_id=uuid4(),
            order_id=uuid4(),
            rating=6,
            comment="Teste",
            sentiment="positive",
        )


def test_rating_below_min_rejected():
    with pytest.raises(ValidationError):
        Review(
            review_id=uuid4(),
            order_id=uuid4(),
            rating=0,
            comment="Teste",
            sentiment="negative",
        )


def test_valid_customer():
    customer = Customer(
        customer_id=uuid4(),
        name="Maria Silva",
        email="maria@example.com",
        city="São Paulo",
        state="SP",
        segment="premium",
    )
    assert customer.segment == "premium"


def test_invalid_segment_rejected():
    with pytest.raises(ValidationError):
        Customer(
            customer_id=uuid4(),
            name="João",
            email="joao@example.com",
            city="Rio",
            state="RJ",
            segment="vip",
        )


def test_valid_product():
    product = Product(
        product_id=uuid4(),
        name="Smartphone XYZ",
        category="electronics",
        price=Decimal("1299.90"),
        brand="TechBrand",
    )
    assert product.price == Decimal("1299.90")


def test_product_zero_price_rejected():
    with pytest.raises(ValidationError):
        Product(
            product_id=uuid4(),
            name="Free Item",
            category="electronics",
            price=Decimal("0.00"),
        )


def test_product_missing_category_rejected():
    with pytest.raises(ValidationError):
        Product(
            product_id=uuid4(),
            name="No Category",
            price=Decimal("99.90"),
        )
