import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from app.core.db import async_session_maker

from app.auth.crud import crud_create_user
from app.auth.models import User
from app.auth.schemas import UserCreate
from app.core.db import recreate_tables
from app.main import app


@pytest.fixture()
async def db_fixture() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
async def run_around_tests():
    await recreate_tables()


@pytest.fixture()
async def regular_user(db_fixture: AsyncSession) -> User:
    user = UserCreate(
        name="user",
        surname="user",
        email="user@user.com",
        password="user"
    )
    return await crud_create_user(db_fixture, user)


@pytest.fixture()
async def regular_user2(db_fixture: AsyncSession) -> User:
    user = UserCreate(
        name="user2",
        surname="user2",
        email="user2@user.com",
        password="user2"
    )
    return await crud_create_user(db_fixture, user)
