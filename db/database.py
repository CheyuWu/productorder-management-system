import os

from sqlmodel import SQLModel, Session, create_engine
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    # For development
    "postgresql://dev:password@localhost:5432/app"
)

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
