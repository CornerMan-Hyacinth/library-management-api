from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import Book
from ..schemas import Book as BookSchema, BookCreate, BookUpdate
from typing import List, Optional

async def create_book(db: AsyncSession, book: BookCreate) -> BookSchema:
    new_book = Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return BookSchema.model_validate(new_book)

async def get_books(db: AsyncSession) -> List[BookSchema]:
    results = await db.execute(select(Book))      
    db_books = results.scalars().all()
    return [BookSchema.model_validate(b) for b in db_books]

async def get_book_by_id(db: AsyncSession, id: str) -> Optional[BookSchema]:
    result = await db.execute(select(Book).where(Book.id == id))
    return BookSchema.model_validate(result.scalars().first())

async def get_book_by_title(db: AsyncSession, title: str) -> Optional[BookSchema]:
    result = await db.execute(select(Book).where(Book.title == title))
    return BookSchema.model_validate(result.scalars().first())

async def get_books_by_category(db: AsyncSession, cat_id: str) -> List[BookSchema]:
    results = await db.execute(select(Book).where(Book.category_id == cat_id))
    db_books = results.scalars().all()
    return [BookSchema.model_validate(b) for b in db_books]

async def update_book(db: AsyncSession, id: str, data: BookUpdate) -> Optional[BookSchema]:
    result = await db.execute(select(Book).where(Book.id == id))
    book = result.scalars().first()
    if not book:
        return None
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    
    await db.commit()
    await db.refresh(book)
    return BookSchema.model_validate(book)

async def delete_book(db: AsyncSession, id: str) -> bool:
    result = await db.execute(select(Book).where(Book.id == id))
    book = result.scalars().first()
    if not book:
        return False
    
    await db.delete(book)
    await db.commit()
    return True