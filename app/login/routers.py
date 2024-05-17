from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from app.auth.models import User
from .schemas import Token
from app.core.db import get_async_session
from .services import authenticate_user, create_access_token, get_current_user_from_token

router = APIRouter()


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: AsyncSession = Depends(get_async_session)):
    user = await authenticate_user(email=form_data.username,
                                   password=form_data.password,
                                   db=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password'
        )
    access_token_expired = timedelta(minutes=60)
    access_token = create_access_token(
        data={'sub': user.email},
        expires_delta=access_token_expired
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/test')
async def get_norm_user(current_user: User = Depends(get_current_user_from_token)):
    return {'succes':True, 'current_user': current_user}
