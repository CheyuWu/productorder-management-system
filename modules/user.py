from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select, delete
from db.models import User
from schemas.users import UserCreate
from passlib.hash import bcrypt


async def create_user(user: UserCreate, db: AsyncSession):
    user.password = bcrypt.hash(user.password)
    user_to_db = User.model_validate(user)
    db.add(user_to_db)
    await db.commit()
    await db.refresh(user_to_db)
    return user_to_db


async def delete_user(user_id: int, db: AsyncSession):
    select_statement = select(User).where(col(User.user_id) == user_id)
    (await db.execute(select_statement)).one()
    delete_statement = delete(User).where(col(User.user_id) == user_id)
    await db.execute(delete_statement)
    await db.commit()
