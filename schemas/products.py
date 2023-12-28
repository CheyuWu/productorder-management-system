from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: int
    stock: int


class Product(ProductCreate):
    product_id: int
    created_by: int

    class Config:
        orm_mode = True
