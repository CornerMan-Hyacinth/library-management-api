from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Borrow
from app.schemas import Borrow as BorSchema, BorrowCreate, BorrowUpdate
from typing import List, Optional

async def create_borrow(db: AsyncSession, borrow: BorrowCreate) -> BorSchema:
    new_borrow = Borrow(**borrow.model_dump())
    db.add(new_borrow)
    await db.commit()
    await db.refresh(new_borrow)
    return BorSchema.model_validate(new_borrow)

async def get_borrows(db: AsyncSession) -> List[Borrow]:
    result = await db.execute(select(Borrow))
    db_borrows = result.scalars().all()
    return [BorSchema.model_validate(borrow) for borrow in db_borrows]

async def get_borrow_by_id(db: AsyncSession, borrow_id: str) -> Optional[BorSchema]:
    result = await db.execute(select(Borrow).where(Borrow.id == borrow_id))
    borrow = result.scalars().first()
    if not borrow:
        return None
    return BorSchema.model_validate(borrow)

async def get_borrows_by_user(db: AsyncSession, user_email: str) -> List[BorSchema]:
    result = await db.execute(select(Borrow).where(Borrow.user_email == user_email))
    db_borrows = result.scalars().all()
    return [BorSchema.model_validate(borrow) for borrow in db_borrows]

async def get_borrows_by_book(db: AsyncSession, book_id: str) -> List[BorSchema]:
    result = await db.execute(select(Borrow).where(Borrow.book_id == book_id))
    db_borrows = result.scalars().all()
    return [BorSchema.model_validate(borrow) for borrow in db_borrows]

async def update_borrow(
    db: AsyncSession, borrow_id: str, data: BorrowUpdate
) -> Optional[BorSchema]:
    result = await db.execute(select(Borrow).where(Borrow.id == borrow_id))
    borrow = result.scalars().first()
    if not borrow:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(borrow, key, value)

    await db.commit()
    await db.refresh(borrow)
    return BorSchema.model_validate(borrow)

async def delete_borrow(db: AsyncSession, borrow_id: str) -> bool:
    result = await db.execute(select(Borrow).where(Borrow.id == borrow_id))
    borrow = result.scalars().first()
    if not borrow:
        return False

    await db.delete(borrow)
    await db.commit()
    return True
