from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.reader import Reader
from ..schemas import Reader as ReadSchema, ReaderCreate, ReaderUpdate
from typing import List, Optional

async def create_reader(db: AsyncSession, reader: ReaderCreate) -> ReadSchema:
    new_reader = Reader(**reader.model_dump())
    db.add(new_reader)
    await db.commit()
    await db.refresh(new_reader)
    return ReadSchema.model_validate(new_reader)

async def get_readers(db: AsyncSession) -> List[ReadSchema]:
    result = await db.execute(select(Reader))
    db_readers = result.scalars().all()
    return [ReadSchema.model_validate(reader) for reader in db_readers]

async def get_reader_by_id(db: AsyncSession, id: str) -> Optional[ReadSchema]:
    result = await db.execute(select(Reader).where(Reader.id == id))
    return ReadSchema.model_validate(result.scalars().first())

async def get_reader_by_email(db: AsyncSession, email: str) -> Optional[ReadSchema]:
    result = await db.execute(select(Reader).where(Reader.email == email))
    return ReadSchema.model_validate(result.scalars().first())

async def update_reader(
    db: AsyncSession, id: str, data: ReaderUpdate
) -> Optional[ReadSchema]:
    result = await db.execute(select(Reader).where(Reader.id == id))
    reader = result.scalars().first()
    if not reader:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(reader, key, value)

    await db.commit()
    await db.refresh(reader)
    return ReadSchema.model_validate(reader)

async def delete_reader(db: AsyncSession, id: str) -> bool:
    result = await db.execute(select(Reader).where(Reader.id == id))
    reader = result.scalars().first()
    if not reader:
        return False

    await db.delete(reader)
    await db.commit()
    return True
