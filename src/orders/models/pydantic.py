from typing import Optional
from decimal import Decimal
from pydantic import (
    BaseModel,
    ConfigDict,
)

from datetime import datetime
from src.users.models.pydantic import UserAddressModel
from src.orders.models.sqlalchemy import OrderStatusEnum


class BasketLineModel(BaseModel):
    id: Optional[int] = None
    product_id: int
    basket_id: int
    quantity: int
    price: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)


class BasketModel(BaseModel):
    id: Optional[int] = None
    user_id: int
    price: Optional[Decimal] = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class OrderLineModel(BaseModel):
    id: Optional[int] = None
    product_id: int
    order_id: int
    quantity: int
    price: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)


class OrderCreateFromBasket(BaseModel):
    user_id: int
    basket_id: int
    address_id: int
    additional_info: Optional[str] = None
    status: Optional[OrderStatusEnum] = OrderStatusEnum.Open

    model_config = ConfigDict(from_attributes=True)


class OrderModel(BaseModel):
    id: Optional[int] = None
    number: Optional[int] = None
    basket_id: int
    user_id: int
    address_id: int
    total_price: Optional[Decimal] = None
    shipping_price: Optional[Decimal] = None
    shipping_method: Optional[str] = None
    status: str
    additional_info: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    additional_info: Optional[str] = None
    address_id: Optional[int] = None