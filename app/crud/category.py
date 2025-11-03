from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.category import Category
from ..schemas.category import Category as CatSchema, CategoryCreate, CategoryUpdate
from typing import List, Optional

async def create_category(db: AsyncSession, category: CategoryCreate) -> CatSchema:
    new_category = Category(**category.model_dump())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return CatSchema.model_validate(new_category)

async def get_categories(db: AsyncSession) -> List[CatSchema]:
    result = await db.execute(select(Category))
    db_categories = result.scalars().all()
    return [CatSchema.model_validate(cat) for cat in db_categories]

async def get_category_by_id(db: AsyncSession, category_id: str) -> Optional[CatSchema]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        return None
    
    return CatSchema.model_validate(category)

async def get_category_by_name(db: AsyncSession, category: str) -> Optional[CatSchema]:
    result = await db.execute(select(Category).where(func.lower(Category.name) == category.lower()))
    category = result.scalars().first()
    if not category:
        return None
    
    return CatSchema.model_validate(category)

async def update_category(
    db: AsyncSession, category_id: str, data: CategoryUpdate
) -> Optional[CatSchema]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)
    return CatSchema.model_validate(category)

async def delete_category(db: AsyncSession, category_id: str) -> bool:
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        return False

    await db.delete(category)
    await db.commit()
    return True
