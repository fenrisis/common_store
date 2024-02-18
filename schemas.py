from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    shop_id: int
    category_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None


class OrderCreate(BaseModel):
    customer_id: int
    total_amount: Decimal


class OrderStatusUpdate(BaseModel):
    status: str


class CartItemCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None


class CartItem(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    added_at: datetime

    class Config:
        from_attributes = True
