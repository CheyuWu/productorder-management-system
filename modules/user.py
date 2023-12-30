from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy import delete
from db.models import User
from schemas.users import UserCreate, UserDelete
from passlib.hash import bcrypt


async def create_user(user: UserCreate, db: AsyncSession):
    user.password = bcrypt.hash(user.password)
    user_to_db = User.model_validate(user)
    db.add(user_to_db)
    await db.commit()
    await db.refresh(user_to_db)
    return user_to_db


async def delete_user(username: str, db: AsyncSession):
    select_statement = select(User).where(username == User.username)
    (await db.execute(select_statement)).one()
    delete_statement = delete(User).where(username == User.username)  # type: ignore (false positive)
    await db.execute(delete_statement)
    await db.commit()
    