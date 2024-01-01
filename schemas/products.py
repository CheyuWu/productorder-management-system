from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: str = Field(nullable=False, unique=True)
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass
    
class ProductToDb(ProductBase):
    creator_id: int
    
class ProductCreateResponse(ProductBase):
    product_id: int
    creator_id: int
    
class ProductList(ProductBase):
    product_id: int
    creator_id: int
class ProductUpdate(ProductBase):
    pass