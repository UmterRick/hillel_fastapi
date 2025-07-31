from src.common.databases.postgres import Base
from src.orders.models.sqlalchemy import Order, OrderLine, Basket, BasketLine
from src.users.models.sqlalchemy import User, UserAddress
from src.catalogue.models.sqlalchemy import (
    Product,
    Category,
    ProductCategory,
    ProductImage,
    StockRecord,
    ProductDiscount,
)