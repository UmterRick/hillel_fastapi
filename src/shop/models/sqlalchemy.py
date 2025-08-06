import datetime
import enum
from decimal import Decimal

from sqlalchemy import (Column,
                        Integer, Boolean, Numeric,
                        DateTime,
                        String, Text, Enum,
                        ForeignKey, CheckConstraint,
                        )

from sqlalchemy.orm import relationship

from src.common.databases.postgres import Base


class BasketStatus(enum.Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"

class OrderStatus(enum.Enum):
    OPEN = "Open"
    PAID = "Paid"
    SENT = "Sent"
    RECEIVED = "Received"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"


class BasketLine(Base):

    __tablename__ = "basket_lines"

    product_id = Column(Integer, ForeignKey("products.id"))
    basket_id = Column(Integer, ForeignKey("baskets.id"))
    quantity = Column(Integer)
    price = Column(Decimal)

    basket = relationship("Basket", back_populates="lines")
    product = relationship("Product")


class Basket(Base):

    __tablename__ = "baskets"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    price = Column(Decimal, default=Decimal("0.00"))
    status = Column(Enum(BasketStatus), default=BasketStatus.OPEN)

    user = relationship("User", back_populates="baskets")
    lines = relationship("BasketLine", back_populates="basket")



class OrderLine(Base):
    __tablename__ = "order_lines"

    product_id = Column(Integer, ForeignKey("products.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    quantity = Column(Integer)
    price = Column(Decimal)

    order = relationship("Order", back_populates="lines")
    product = relationship("Product")


class Order(Base):
    __tablename__ = "orders"

    number = Column(Integer, default=10000)
    basket_id = Column(Integer, ForeignKey("baskets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("addresses.id"))

    total_price = Column(Decimal, nullable=False)
    shipping_price = Column(Decimal)
    shipping_method = Column(String, nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.OPEN)
    additional_info = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now(tz=datetime.timezone.utc))

    user = relationship("User", back_populates="orders")
    address = relationship("Address")
    basket = relationship("Basket")
    lines = relationship("OrderLine", back_populates="order")