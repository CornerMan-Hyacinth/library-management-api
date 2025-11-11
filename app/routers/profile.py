from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas import Profile, ProfileCreate, ProfileUpdate, ResponseModel
from app.crud import profile as profile_crud
from app.database import get_db
from app.utils.response import success_response, error_response
from app.utils.core.auth import get_current_staff, get_current_user

router = APIRouter(prefix="/profiles", tags=["Profiles"])

# @router.post("/", dependencies=[Depends(get_current_staff)], response_model=ResponseModel[Profile])
# async def create_profile(profile: ProfileCreate, db: AsyncSession = Depends(get_db)):
#     existing = await profile_crud.get_profile_by_email(db=db, email=profile.email)
#     if existing:
#         return error_response(
#             message="Profile already exists", status_code=status.HTTP_409_CONFLICT
#         )
        
#     new_profile = await profile_crud.create_profile(db=db, profile=profile)
#     return success_response(
#         "Profile created successfully",
#         data=new_profile,
#         status_code=status.HTTP_201_CREATED
#     )

@router.get("/", dependencies=[Depends(get_current_staff)], response_model=ResponseModel[List[Profile]])
async def get_profiles(db: AsyncSession = Depends(get_db)):
    profiles = await profile_crud.get_profiles(db=db)
    return success_response(message="Retrieved profiles successfully", data=profiles)

@router.get("/{profile_id}", dependencies=[Depends(get_current_user)], response_model=ResponseModel[Profile])
async def get_profile(profile_id: str, db: AsyncSession = Depends(get_db)):
    profile = await profile_crud.get_profile_by_id(db=db, id=profile_id)
    if not profile:
        return error_response(
            message="Profile not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(data=profile, message="Retrieved profile successfully")

@router.put("/{profile_id}", dependencies=[Depends(get_current_user)], response_model=ResponseModel[Profile])
async def update_profile(
    profile_id: str, profile: ProfileUpdate, db: AsyncSession = Depends(get_db)
):
    updated_profile = await profile_crud.update_profile(db=db, id=profile_id, data=profile)
    if not updated_profile:
        return error_response(
            message="Profile not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Updated profile successfully", data=updated_profile)

@router.delete("/{profile_id}", dependencies=[Depends(get_current_staff)], response_model=ResponseModel[None])
async def delete_profile(profile_id: str, db: AsyncSession = Depends(get_db)):
    is_deleted = await profile_crud.delete_profile(db=db, id=profile_id)
    if not is_deleted:
        return error_response(
            message="Profile not found", status_code=status.HTTP_404_NOT_FOUND
        )
        
    return success_response(message="Deleted profile successfully")