from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: str = Field(nullable=False, unique=True)
    price: float
    stock: int
    creator_id: int = Field(foreign_key="user.user_id", nullable=False)

class ProductCreate(ProductBase):
    pass
    
class ProductCreateResponse(ProductBase):
    product_id: int
    
class ProductList(ProductBase):
    product_id: int

class ProductUpdate(ProductBase):
    pass