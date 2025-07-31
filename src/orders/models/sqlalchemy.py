from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Sequence,
    Enum as SQLEnum,
    Numeric,
)

from enum import Enum
from sqlalchemy.orm import relationship
from src.common.databases.postgres import Base
from datetime import datetime



class OrderStatusEnum(str, Enum):
    Open = "Open"
    Paid = "Paid"
    Sent = "Sent"
    Received = "Received"
    Cancelled = "Cancelled"
    Returned = "Returned"



class BasketStatusEnum(str, Enum):
    Open = "Open"
    Closed = "Closed"
    Cancelled = "Cancelled"



class BasketLine(Base):
    __tablename__ = "basket_lines"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    basket_id = Column(Integer, ForeignKey('baskets.id', ondelete="CASCADE"))
    quantity = Column(Integer, CheckConstraint('quantity >= 0'))
    price = Column(Numeric(10, 2), CheckConstraint('price >= 0'))


    product = relationship('Product', back_populates='basket_lines')
    basket = relationship('Basket', back_populates='basket_lines')



class Basket(Base):
    __tablename__ = "baskets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    price = Column(Numeric(10, 2), CheckConstraint('price >= 0'))
    status = Column(SQLEnum(BasketStatusEnum, name="basket_status"), nullable=False)


    user = relationship('User', back_populates='basket')
    basket_lines = relationship(
        'BasketLine',
        back_populates='basket',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    orders = relationship('Order', back_populates='basket')



class OrderLine(Base):
    __tablename__ = "order_lines"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
    quantity = Column(Integer, CheckConstraint('quantity >= 0'))
    price = Column(Numeric(10, 2), CheckConstraint('price >= 0'))


    product = relationship('Product', back_populates='order_lines')
    order = relationship('Order', back_populates='order_lines')



class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, Sequence("order_number_seq", start=10000), unique=True, nullable=False)
    basket_id = Column(Integer, ForeignKey('baskets.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    address_id = Column(Integer, ForeignKey('user_addresses.id'))
    total_price = Column(Numeric(10, 2), CheckConstraint('total_price >= 0'))
    shipping_price = Column(Numeric(10, 2), CheckConstraint('shipping_price >= 0'))
    shipping_method = Column(String, nullable=True)
    status = Column(SQLEnum(OrderStatusEnum, name="order_status"), nullable=False)
    additional_info = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


    order_lines = relationship('OrderLine', back_populates='order', cascade='all, delete-orphan')
    basket = relationship('Basket', back_populates='orders')
    user = relationship('User', back_populates='orders')
    address = relationship('UserAddress', back_populates='orders')
