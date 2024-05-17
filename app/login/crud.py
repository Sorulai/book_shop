from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User


async def crud_get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    res = await db.execute(query)
    return res.fetchone()