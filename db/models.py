from typing import List, Optional
from sqlmodel import Field, Relationship
from schemas.order_products import OrderProductBase
from schemas.orders import OrderBase
from schemas.products import ProductBase
from schemas.users import UserBase
from uuid import UUID, uuid4


class User(UserBase, table=True):
    user_id: int = Field(default=None, primary_key=True, index=True)
    password: str
    created_products: Optional[List["Product"]] = Relationship(
        back_populates="creator", sa_relationship_kwargs={"lazy": "selectin"}
    )
    orders_list: Optional[List["Order"]] = Relationship(
        back_populates="customer", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Product(ProductBase, table=True):
    product_id: int = Field(primary_key=True, index=True)
    creator: User = Relationship(
        back_populates="created_products", sa_relationship_kwargs={"lazy": "selectin"}
    )
    order_product_list: Optional[List["OrderProduct"]] = Relationship(
        back_populates="product_list", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Order(OrderBase, table=True):
    order_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    customer: User = Relationship(
        back_populates="orders_list", sa_relationship_kwargs={"lazy": "selectin"}
    )
    order_products: List["OrderProduct"] = Relationship(
        back_populates="order_list", sa_relationship_kwargs={"lazy": "selectin"}
    )


class OrderProduct(OrderProductBase, table=True):
    order_list: Order = Relationship(
        back_populates="order_products", sa_relationship_kwargs={"lazy": "selectin"}
    )
    product_list: Product = Relationship(
        back_populates="order_product_list", sa_relationship_kwargs={"lazy": "selectin"}
    )
