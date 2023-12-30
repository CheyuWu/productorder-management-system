

from uuid import UUID
from sqlmodel import Field, SQLModel


class OrderProductBase(SQLModel):
    order_id: UUID = Field(foreign_key="order.order_id", primary_key=True)
    product_id: int = Field(foreign_key="product.product_id", primary_key=True)
    quantity: int
