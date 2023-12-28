from pydantic import BaseModel

from db.models import UserRole



class UserCreate(BaseModel):
    username: str
    role: UserRole


class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True
