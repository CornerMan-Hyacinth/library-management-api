from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.crud import profile as profile_crud
from app.database import get_db
from app.models import User
from app.utils.core.security import hash_password, verify_password
from app.utils.core.auth import create_access_token, get_user_by_username, get_user_by_email, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas import UserCreate, UserLogin, UserOut, Token, ResponseModel, ProfileCreate
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=ResponseModel[UserOut])
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_email = await get_user_by_email(db=db, email=user_data.email)
    if existing_email:
        return error_response(
            status_code=status.HTTP_400_BAD_REQUEST, message="Email already taken"
        )
        
    existing_username = await get_user_by_username(db=db, username=user_data.username)
    if existing_username:
        return error_response(
            status_code=status.HTTP_400_BAD_REQUEST, message="Username already taken"
        )
        
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password),
        is_staff=user_data.is_staff
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    new_profile = ProfileCreate(
        email=user_data.email,
        username=user_data.username,
        gender=user_data.gender,
        phone_number=user_data.phone_number,
        address=user_data.address
    )
    await profile_crud.create_profile(db=db, profile=new_profile)
    
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        data=new_user
    )

@router.post("/login", response_model=Token)
async def login_user(form_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db=db, username=form_data.username)    
    if not user or not verify_password(form_data.password, user.password):
        return error_response(
            status_code=status.HTTP_400_BAD_REQUEST, message="Invalid credentials"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}