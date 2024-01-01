from fastapi import Depends
import pytest
from sqlalchemy import StaticPool
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlmodel import SQLModel
from db.database import get_session
from api import app

from schemas.users import UserRole


BASE_URL = "http://test"


@pytest.fixture(name="session")
@pytest.mark.asyncio
async def session_fixture():
    engine = create_async_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session


@pytest.mark.asyncio
async def test_create_and_delete_user(session: AsyncSession):
    async def get_session_override():
        return session

    app.dependency_overrides[Depends(get_session)] = get_session_override
    # Test case for the create_user_api endpoint
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "role": UserRole.CUSTOMER.value,
    }
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        # Create user
        create_response = await client.post("/user", json=user_data, timeout=5)
        assert create_response.status_code == 201
        created_user = create_response.json()
        assert "user_id" in created_user
        assert created_user["username"] == user_data["username"]

        # Test case for the delete_user_api endpoint
        delete_response = await client.delete(
            f"/user/{created_user['user_id']}", timeout=5
        )
        assert delete_response.status_code == 204
    app.dependency_overrides.clear()
