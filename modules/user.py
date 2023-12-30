from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from schemas.users import UserCreate
from passlib.hash import bcrypt

async def create_user(user: UserCreate, db: AsyncSession):
    user.password = bcrypt.hash(user.password)
    user_to_db = User.model_validate(user)
    db.add(user_to_db)
    await db.commit()
    await db.refresh(user_to_db)
    await db.close()
    return user_to_db

