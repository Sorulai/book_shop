from uuid import UUID
from sqlalchemy import update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from .schemas import UserCreate
from .services import Hasher


async def crud_create_user(db: AsyncSession, user: UserCreate):
    hash_psw = Hasher.get_password_hash(user.password)
    new_user = User(name=user.name, surname=user.surname, email=user.email, hashed_password=hash_psw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def crud_delete_user(db: AsyncSession, user_id: UUID):
    query = update(User).where(
        and_(User.user_id == user_id, User.is_active == True)).values(
        is_active=False).returning(User.user_id)
    res = await db.execute(query)
    await db.commit()
    return res.fetchone()


async def crud_get_user(db: AsyncSession, user_id: UUID):
    query = select(User).where(User.user_id == user_id)
    res = await db.execute(query)
    return res.fetchone()


async def crud_update_user(db: AsyncSession, user_id: UUID, **kwargs):
    query = update(User).where(
        and_(User.user_id == user_id, User.is_active == True)).values(
        kwargs).returning(User.user_id)

    res = await db.execute(query)
    await db.commit()
    return res.fetchone()
