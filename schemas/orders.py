from datetime import datetime
from uuid import UUID
from sqlalchemy import func
from sqlmodel import Field, SQLModel

class OrderBase(SQLModel):
    customer_id: int = Field(foreign_key="user.user_id", nullable=False)
    order_date: datetime = Field(default=func.now)
    total_price: float

class OrderList(OrderBase):
    order_id: UUID

class OrderCreate(OrderBase):
    pass

class OrderProductBase(SQLModel):
    product_id: int = Field(foreign_key="product.product_id", primary_key=True)
    quantity: int


class OrderProductList(OrderProductBase):
    pass
class OrderProductCreate(OrderProductBase):
    pass