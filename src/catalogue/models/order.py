
from sqlalchemy import Column, Integer, ForeignKey, String, Enum, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.catalogue.models.base import Base
import enum

class OrderStatus(enum.Enum):
    open = "Open"
    paid = "Paid"
    sent = "Sent"
    received = "Received"
    cancelled = "Cancelled"
    returned = "Returned"

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    number = Column(Integer, default=10000)
    basket_id = Column(Integer, ForeignKey("basket.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    address_id = Column(Integer, ForeignKey("address.id"))
    total_price = Column(Numeric(10, 2))
    shipping_price = Column(Numeric(10, 2))
    shipping_method = Column(String, nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.open)
    additional_info = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    basket = relationship("Basket", back_populates="orders")
    user = relationship("User")
    address = relationship("Address")
    lines = relationship("OrderLine", back_populates="order")