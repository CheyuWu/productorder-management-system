from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from core import get_settings
from exception.db_exception import DatabaseUrlNotFound

DATABASE_URL = get_settings().DATABASE_URL
DEBUG = get_settings().DEBUG

print(DATABASE_URL)

if not DATABASE_URL:
    raise DatabaseUrlNotFound

engine = create_async_engine(DATABASE_URL, echo=DEBUG, future=True)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    # expire_on_commit - don't expire objects after transaction commit
    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session
