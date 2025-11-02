from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import Book
from ..schemas import BookCreate, BookUpdate
from typing import List, Optional

async def create_book(db: AsyncSession, book: BookCreate):
    new_book = Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book.id

async def get_books(db: AsyncSession) -> List[Book]:
    results = await db.execute(select(Book))
    return results.scalars().all()

async def get_borrowed_books(db: AsyncSession) -> List[Book]:
    results = await db.execute(select(Book).where(Book.available == False))
    return results.scalars().all

async def get_book_by_id(db: AsyncSession, id: str) -> Optional[Book]:
    result = await db.execute(select(Book).where(Book.id == id))
    return result.scalars().first()

async def update_book(db: AsyncSession, id: str, data: BookUpdate) -> Optional[Book]:
    result = await db.execute(select(Book).where(Book.id == id))
    book = result.scalars().first()
    if not book:
        return None
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    
    await db.commit()
    await db.refresh(book)
    return book

async def delete_book(db: AsyncSession, id: str) -> bool:
    result = await db.execute(select(Book).where(Book.id == id))
    book = result.scalars().first()
    if not book:
        return False
    
    await db.delete(book)
    await db.commit()
    return True