from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlmodel import SQLModel, Session
from db.database import get_session
from api import app

from schemas.users import UserRole


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_and_delete_user(client: TestClient):
    # Test case for the create_user_api endpoint
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "role": UserRole.CUSTOMER.value,
    }
    # Create user
    create_response = client.post("/user", json=user_data)
    assert create_response.status_code == 201
    created_user = create_response.json()
    assert "user_id" in created_user
    assert created_user["username"] == user_data["username"]

    # Test case for the delete_user_api endpoint
    # delete_response = client.delete(f"/user/1")
    # assert delete_response.status_code == 204
