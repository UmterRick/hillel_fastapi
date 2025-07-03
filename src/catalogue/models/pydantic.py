from typing import Optional

from pydantic import (
    BaseModel,
    constr,
)

class ProductElasticResponse(BaseModel):
    product_id: int
    title: str
    score: float


class ProductModel(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    short_description: Optional[constr(max_length=20)]
    is_active: bool

    class Config:
        from_attributes = True
