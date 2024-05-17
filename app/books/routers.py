from fastapi import Depends, APIRouter, HTTPException, Response
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.books.schemas import BookCreate, BookUpdate
from app.books.crud import create_book, get_all_books, get_book_by_id, update_book, delete_book
from app.auth.models import User
from app.books.schemas import BookResponse
from app.login.services import get_current_user_from_token

router = APIRouter()


@router.post("/add", response_model=BookResponse)
async def create_book_endpoint(book: BookCreate,
                               db: AsyncSession = Depends(get_async_session),
                               current_user: User = Depends(get_current_user_from_token)):
    return await create_book(db, book)


@router.get("/all", response_model=List[BookResponse])
async def get_all_books_endpoint(db: AsyncSession = Depends(get_async_session),
                                 current_user: User = Depends(get_current_user_from_token)):
    return await get_all_books(db)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book_by_id_endpoint(book_id: int,
                                  db: AsyncSession = Depends(get_async_session),
                                  current_user: User = Depends(get_current_user_from_token)):
    return await get_book_by_id(book_id, db)


@router.put("/{book_id}", response_model=BookResponse)
async def update_book_endpoint(book_id: int,
                               book_update: BookUpdate,
                               db: AsyncSession = Depends(get_async_session),
                               current_user: User = Depends(get_current_user_from_token)):
    return await update_book(book_id, book_update, db)


@router.delete("/{book_id}")
async def delete_book_endpoint(book_id: int,
                               db: AsyncSession = Depends(get_async_session),
                               current_user: User = Depends(get_current_user_from_token)):
    book_row = await delete_book(book_id, db)
    if book_row is None:
        raise HTTPException(status_code=404, detail=f'Book with id {book_id} not found')
    return Response(status_code=204)
