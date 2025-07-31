from typing import Optional
from decimal import Decimal

from pydantic import (
    BaseModel,
    constr,
)


class ProductModel(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    short_description: Optional[constr(max_length=20)]
    is_active: bool

    class Config:
        from_attributes = True


class StockRecordModel(BaseModel):
    id: Optional[int]
    product_id: int
    price: Decimal
    quantity: int

    class Config:
        from_attributes = True