from typing import List
from pydantic import BaseModel

class OrderProductCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_id: int
    total_price: int
    order_products: List[OrderProductCreate]


class Order(OrderCreate):
    order_id: int
    order_date: str

    class Config:
        orm_mode = True
