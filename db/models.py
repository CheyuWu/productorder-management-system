from enum import Enum
from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from passlib.hash import bcrypt
from .database import Base


class UserRole(Enum):
    MANAGER = "Manager"
    CUSTOMER = "Customer"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    def __init__(self, username: str, password: str, role: UserRole):
        self.username = username
        self.password = bcrypt.hash(password)
        self.role = role

    created_products = relationship("Product", back_populates="creator", lazy="dynamic")
    orders = relationship("Order", back_populates="customer", lazy="dynamic")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id"))

    creator = relationship("User", back_populates="created_products")
    ordered_in = relationship("OrderProduct", back_populates="product", lazy="dynamic")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    order_date = Column(TIMESTAMP, default=func.now)
    total_price = Column(Integer, nullable=False)

    customer = relationship("User", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order")


class OrderProduct(Base):
    __tablename__ = "order_products"
    order_id = Column(Integer, ForeignKey("orders.order_id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="ordered_in")
