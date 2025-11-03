from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..enums import BookAvailable
from ..models import Book
from ..schemas import BookCreate, BookUpdate
from typing import List, Optional

async def create_book(db: AsyncSession, book: BookCreate):
    new_book = Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

async def get_books(db: AsyncSession, available: BookAvailable) -> List[Book]:
    query = select(Book)
    
    if available == BookAvailable.available:
        query = query.where(Book.available == True)
    elif available == BookAvailable.borrowed:
        query == query.where(Book.available == False)
        
    results = await db.execute(query)      
    return results.scalars().all()

async def get_book_by_id(db: AsyncSession, id: str) -> Optional[Book]:
    result = await db.execute(select(Book).where(Book.id == id))
    return result.scalars().first()

async def get_book_by_title(db: AsyncSession, title: str) -> Optional[Book]:
    result = await db.execute(select(Book).where(Book.title == title))
    return result.scalars().first()

async def get_book_by_category(db: AsyncSession, cat_id: str) -> List[Book]:
    results = await db.execute(select(Book).where(Book.category_id == cat_id))
    return results.scalars().all()

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