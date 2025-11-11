from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Profile
from app.schemas import Profile as ProfSchema, ProfileCreate, ProfileUpdate
from typing import List, Optional

async def create_profile(db: AsyncSession, profile: ProfileCreate) -> ProfSchema:
    profile = Profile(**profile.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return ProfSchema.model_validate(profile)

async def get_profiles(db: AsyncSession) -> List[ProfSchema]:
    result = await db.execute(select(Profile))
    db_profiles = result.scalars().all()
    return [ProfSchema.model_validate(profile) for profile in db_profiles]

async def get_profile_by_id(db: AsyncSession, id: str) -> Optional[ProfSchema]:
    result = await db.execute(select(Profile).where(Profile.id == id))
    profile = result.scalars().first()
    if not profile:
        return None
    return Profile.model_validate(profile)

async def get_profile_by_email(db: AsyncSession, email: str) -> Optional[ProfSchema]:
    result = await db.execute(select(Profile).where(Profile.email == email))
    profile = result.scalars().first()
    if not profile:
        return None
    return ProfSchema.model_validate(profile)

async def update_profile(
    db: AsyncSession, id: str, data: ProfileUpdate
) -> Optional[ProfSchema]:
    result = await db.execute(select(Profile).where(Profile.id == id))
    profile = result.scalars().first()
    if not profile:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return ProfSchema.model_validate(profile)

async def delete_profile(db: AsyncSession, id: str) -> bool:
    result = await db.execute(select(ProfSchema).where(ProfSchema.id == id))
    profile = result.scalars().first()
    if not profile:
        return False

    await db.delete(profile)
    await db.commit()
    return True
