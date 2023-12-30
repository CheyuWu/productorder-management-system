import enum
from sqlmodel import Field, SQLModel


class UserRole(enum.Enum):
    MANAGER = "Manager"
    CUSTOMER = "Customer"

class UserBase(SQLModel):
    username: str = Field(unique=True, nullable=False)
    role: UserRole

class UserCreate(UserBase):
    password: str

