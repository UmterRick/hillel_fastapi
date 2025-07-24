from sqlalchemy import Column, Integer, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from src.catalogue.models.base import Base
import enum

class BasketStatus(enum.Enum):
    open = "Open"
    closed = "Closed"
    cancelled = "Cancelled"

class Basket(Base):
    __tablename__ = "basket"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    price = Column(Numeric(10, 2))
    status = Column(Enum(BasketStatus), default=BasketStatus.open)

    user = relationship("User")
    lines = relationship("BasketLine", back_populates="basket")
    orders = relationship("Order", back_populates="basket")

class BasketLine(Base):
    __tablename__ = "basket_line"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    basket_id = Column(Integer, ForeignKey("basket.id"))
    quantity = Column(Integer)
    price = Column(Numeric(10, 2))

    product = relationship("Product")
    basket = relationship("Basket", back_populates="lines")

class OrderLine(Base):
    __tablename__ = "order_line"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    order_id = Column(Integer, ForeignKey("order.id"))
    quantity = Column(Integer)
    price = Column(Numeric(10, 2))

    product = relationship("Product")
    order = relationship("Order", back_populates="lines")