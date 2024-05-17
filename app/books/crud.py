from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.books.schemas import BookCreate, BookUpdate
from app.books.models import Book


async def create_book(db: AsyncSession, book: BookCreate):
    new_book = Book(title=book.title, author=book.author,
                    year=book.year, genre=book.genre,
                    user_id=book.user_id)

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


async def get_all_books(db: AsyncSession):
    stmt = select(Book)
    res = await db.execute(stmt)
    return res.scalars().all()


async def get_book_by_id(book_id: int, db: AsyncSession):
    stmt = select(Book).where(Book.id == book_id)
    result = await db.execute(stmt)
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


async def update_book(book_id: int, book_update: BookUpdate, db: AsyncSession):
    stmt = select(Book).where(Book.id == book_id)
    result = await db.execute(stmt)
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(book, key, value)

    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(book_id: int, db: AsyncSession):
    stmt = select(Book).where(Book.id == book_id)
    result = await db.execute(stmt)
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(book)
    await db.commit()
    return True
