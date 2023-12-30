from datetime import datetime
from sqlalchemy import func
from sqlmodel import Field, SQLModel

class OrderBase(SQLModel):
    customer_id: int = Field(foreign_key="user.user_id", nullable=False)
    order_date: datetime = Field(default=func.now)
    total_price: float