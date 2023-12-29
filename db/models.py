import enum
from datetime import datetime
from typing import List
from sqlmodel import SQLModel, Field, Relationship, func
from passlib.hash import bcrypt


class UserRole(enum.Enum):
    MANAGER = "Manager"
    CUSTOMER = "Customer"


class User(SQLModel, table=True):
    user_id: int = Field(primary_key=True, index=True)
    username: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    role: UserRole = Field(nullable=False)

    def __init__(self, username: str, password: str, role: UserRole):
        self.username = username
        self.password = bcrypt.hash(password)
        self.role = role

    created_products: List["Product"] = Relationship(
        back_populates="creator", sa_relationship_kwargs={"lazy": "selectin"}
    )
    orders: List["Order"] = Relationship(
        back_populates="customer", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Product(SQLModel, table=True):
    product_id: int = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
    price: float = Field(nullable=False)
    stock: int = Field(nullable=False)
    created_by: int = Field(foreign_key="user.user_id", nullable=False)

    creator: User = Relationship(
        back_populates="created_products", sa_relationship_kwargs={"lazy": "selectin"}
    )
    ordered_in: List["OrderProduct"] = Relationship(
        back_populates="product", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Order(SQLModel, table=True):
    order_id: int = Field(primary_key=True, index=True)
    customer_id: int = Field(foreign_key="user.user_id", nullable=False)
    order_date: datetime = Field(default=func.now)
    total_price: float = Field(nullable=False)

    customer: User = Relationship(
        back_populates="orders", sa_relationship_kwargs={"lazy": "selectin"}
    )
    order_products: List["OrderProduct"] = Relationship(
        back_populates="order", sa_relationship_kwargs={"lazy": "selectin"}
    )


class OrderProduct(SQLModel, table=True):
    order_id: int = Field(foreign_key="order.order_id", primary_key=True)
    product_id: int = Field(foreign_key="product.product_id", primary_key=True)
    quantity: int = Field(nullable=False)

    order: Order = Relationship(
        back_populates="order_products", sa_relationship_kwargs={"lazy": "selectin"}
    )
    product: Product = Relationship(
        back_populates="orders", sa_relationship_kwargs={"lazy": "selectin"}
    )
