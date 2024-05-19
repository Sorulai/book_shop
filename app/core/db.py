from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.ddl import CreateTable

from .config import settings

db_url = f'postgresql+asyncpg://{settings.db.POSTGRES_USER}:{settings.db.POSTGRES_PASSWORD}@{settings.db.POSTGRES_HOSTNAME}:{settings.db.POSTGRES_PORT}/{settings.db.POSTGRES_DB}'
engine = create_async_engine(db_url, future=True, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def recreate_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)