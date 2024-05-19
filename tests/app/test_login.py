import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_for_access_token(client: AsyncClient):
    test_email = "user@user.com"
    test_password = "user"
    form_data = {
        "username": test_email,
        "password": test_password
    }
    response = await client.post("/login/token", data=form_data)
    assert response.status_code == status.HTTP_200_OK
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_for_access_token_invalid_credentials(client: AsyncClient):
    form_data = {
        "username": "wrong.user@example.com",
        "password": "wrongpassword"
    }
    response = await client.post("/login/token", data=form_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}
