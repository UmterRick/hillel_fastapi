from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from src.common.databases.postgres import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    short_description = Column(String(20), nullable=True)
    is_active = Column(Boolean)

    categories = relationship('ProductCategory', back_populates='product')
    images = relationship('ProductImage', back_populates='product')
    stock_records = relationship('StockRecord', back_populates='product')
    discounts = relationship('ProductDiscount', back_populates='product')


class ProductCategory(Base):
    __tablename__ = 'product_categories'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    product = relationship('Product', back_populates='categories')
    category = relationship('Category', back_populates='products')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    is_active = Column(Boolean)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    products = relationship('ProductCategory', back_populates='category')
    parent = relationship('Category', back_populates='subcategories', remote_side='categories.c.id')
    subcategories = relationship('Category', back_populates='parent')


class ProductImage(Base):
    __tablename__ = 'product_images'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    original = Column(String, nullable=False)
    thumbnail = Column(String, nullable=True)
    caption = Column(String(50), nullable=True)

    product = relationship('Product', back_populates='images')


class StockRecord(Base):
    __tablename__ = 'stock_records'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(Numeric, CheckConstraint('price >= 0'))
    quantity = Column(Integer, CheckConstraint('quantity >= 0'))
    date_created = Column(DateTime)
    additional_info = Column(String, nullable=True)

    product = relationship('Product', back_populates='stock_records')


class ProductDiscount(Base):
    __tablename__ = 'product_discounts'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    discount_percent = Column(Integer, CheckConstraint('0 <= discount_percent <= 100'), nullable=True)
    discount_amount = Column(Numeric, CheckConstraint('discount_amount >= 0'), nullable=True)
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)

    product = relationship('Product', back_populates='discounts')

