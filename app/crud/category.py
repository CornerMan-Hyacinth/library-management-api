from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.category import Category
from ..schemas.category import CategoryCreate, CategoryUpdate
from typing import List, Optional

async def create_category(db: AsyncSession, category: CategoryCreate) -> Category:
    new_category = Category(**category.model_dump())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

async def get_categories(db: AsyncSession) -> List[Category]:
    result = await db.execute(select(Category))
    return result.scalars().all()

async def get_category_by_id(db: AsyncSession, category_id: str) -> Optional[Category]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalars().first()

async def update_category(db: AsyncSession, category_id: str, data: CategoryUpdate) -> Optional[Category]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)
    return category

async def delete_category(db: AsyncSession, category_id: str) -> bool:
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        return False

    await db.delete(category)
    await db.commit()
    return True
