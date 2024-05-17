import datetime
from datetime import timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.core.config import settings
from app.auth.services import Hasher
from .crud import crud_get_user_by_email


async def authenticate_user(email: str, password: str, db: AsyncSession):
    user = await crud_get_user_by_email(email=email, db=db)
    if user is None:
        return False
    if not Hasher.verify_password(password, user[0].hashed_password):
        return False
    return user[0]


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now() + expires_delta
    else:
        expire = datetime.datetime.now() + timedelta(minutes=60)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, settings.db.SECRET_KEY, algorithm='HS256')
    return encode_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/token')


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not valid token'
    )
    try:
        payload = jwt.decode(
            token, settings.db.SECRET_KEY, algorithms=['HS256']
        )
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await crud_get_user_by_email(email=username, db=db)
    if user is None:
        raise credentials_exception
    return user[0]
