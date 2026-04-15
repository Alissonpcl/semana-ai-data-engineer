"""ShopAgent — Pydantic models for the 4 core entities."""

from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class Customer(BaseModel):
    customer_id: UUID
    name: str
    email: str
    city: str | None = None
    state: Literal["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "PE"] | None = None
    segment: Literal["premium", "standard", "basic"]


class Product(BaseModel):
    product_id: UUID
    name: str
    category: str | None = None
    price: Decimal | None = None
    brand: str | None = None


class Order(BaseModel):
    order_id: UUID
    customer_id: UUID
    product_id: UUID
    qty: int = Field(ge=1, le=10)
    total: Decimal = Field(ge=0)
    status: Literal["delivered", "shipped", "processing", "cancelled"]
    payment: Literal["pix", "credit_card", "boleto"]
    created_at: datetime | None = None


class Review(BaseModel):
    review_id: UUID
    order_id: UUID
    rating: int = Field(ge=1, le=5)
    comment: str
    sentiment: Literal["positive", "neutral", "negative"]
