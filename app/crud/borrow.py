from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import Borrow
from ..schemas import BorrowCreate, BorrowUpdate
from typing import List, Optional

async def create_borrow(db: AsyncSession, borrow: BorrowCreate) -> Borrow:
    new_borrow = Borrow(**borrow.model_dump())
    db.add(new_borrow)
    await db.commit()
    await db.refresh(new_borrow)
    return new_borrow

async def get_borrows(db: AsyncSession) -> List[Borrow]:
    result = await db.execute(select(Borrow))
    return result.scalars().all()

async def get_borrow_by_id(db: AsyncSession, borrow_id: str) -> Optional[Borrow]:
    result = await db.execute(select(Borrow).where(Borrow.id == borrow_id))
    return result.scalars().first()

async def get_borrow_by_reader(db: AsyncSession, reader_id: str) -> Optional[Borrow]:
    result = await db.execute(select(Borrow).where(Borrow.reader_id == reader_id))
    return result.scalars().first()

async def get_borrow_by_book(db: AsyncSession, book_id: str) -> Optional[Borrow]:
    result = await db.execute(select(Borrow).where(Borrow.book_id == book_id))
    return result.scalars().first()

async def update_borrow(db: AsyncSession, borrow_id: str, data: BorrowUpdate) -> Optional[Borrow]:
    result = await db.execute(select(Borrow).where(Borrow.id == borrow_id))
    borrow = result.scalars().first()
    if not borrow:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(borrow, key, value)

    await db.commit()
    await db.refresh(borrow)
    return borrow

async def delete_borrow(db: AsyncSession, borrow_id: str) -> bool:
    result = await db.execute(select(Borrow).where(Borrow.id == borrow_id))
    borrow = result.scalars().first()
    if not borrow:
        return False

    await db.delete(borrow)
    await db.commit()
    return True
