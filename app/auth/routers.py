import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.crud import crud_delete_user, crud_create_user, crud_get_user, crud_update_user
from app.auth.schemas import ShowUser, UserCreate, DeleteUserResponse, UpdateUserResponse, UpdateUserRequest
from app.core.db import get_async_session

router = APIRouter()


@router.post('/', response_model=ShowUser)
async def create_user(user: UserCreate,
                      session: AsyncSession = Depends(get_async_session)):
    new_user = await crud_create_user(db=session, user=user)
    return ShowUser(
        user_id=new_user.user_id,
        name=new_user.name,
        surname=new_user.surname,
        email=new_user.email,
        is_active=new_user.is_active
    )


@router.delete('/{user_id}', response_model=DeleteUserResponse)
async def delete_user(user_id: uuid.UUID,
                      session: AsyncSession = Depends(get_async_session)):
    user_row = await crud_delete_user(db=session, user_id=user_id)
    if user_row is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} not found')
    return DeleteUserResponse(user_id=user_row[0])


@router.get('/{user_id}', response_model=ShowUser)
async def get_user(user_id: uuid.UUID,
                   session: AsyncSession = Depends(get_async_session)):
    user_row = await crud_get_user(db=session, user_id=user_id)
    if user_row is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} not found')
    return ShowUser(
        user_id=user_row[0].user_id,
        name=user_row[0].name,
        surname=user_row[0].surname,
        email=user_row[0].email,
        is_active=user_row[0].is_active
    )


@router.patch('/{user_id}', response_model=UpdateUserResponse)
async def update_user(user_id: uuid.UUID,
                      body: UpdateUserRequest,
                      session: AsyncSession = Depends(get_async_session)):
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail=f'At least one param should be provided')
    user = await crud_update_user(db=session, user_id=user_id, **body.dict(exclude_none=True))
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} not found')
    return DeleteUserResponse(user_id=user[0])
