from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship
from backend.db.session import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), nullable=False, default='vendor')
    created_at = Column(DateTime, server_default=func.now())

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    category = Column(String(100))
    price = Column(DECIMAL(10,2), nullable=False)
    cost_price = Column(DECIMAL(10,2), nullable=True, default=0)
    stock_quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())

class Bill(Base):
    __tablename__ = 'bills'
    bill_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    total_amount = Column(DECIMAL(12,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship('User')

class BillItem(Base):
    __tablename__ = 'bill_items'
    bill_item_id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey('bills.bill_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(DECIMAL(10,2), nullable=False)
    subtotal = Column(DECIMAL(12,2), nullable=False)
