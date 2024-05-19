import uuid
import pytest
from starlette import status
from auth.models import User
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    user_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com",
        "password": "password",
    }
    response = await client.post("/user", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "user_id" in data
    assert data["name"] == user_data["name"]
    assert data["surname"] == user_data["surname"]
    assert data["email"] == user_data["email"]
    assert data["is_active"] == True


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient,
                        db_fixture: AsyncSession):
    test_user_id = uuid.uuid4()
    new_user = User(
        user_id=test_user_id,
        name="Test",
        surname="User",
        email="test.user@example.com",
        is_active=True
    )
    db_fixture.add(new_user)
    await db_fixture.commit()
    response = await client.get(f"/user/{test_user_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["user_id"] == str(test_user_id)
    assert data["name"] == "Test"
    assert data["surname"] == "User"
    assert data["email"] == "test.user@example.com"
    assert data["is_active"] is True
