from ..enums import Gender
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
    
class User(BaseModel):
    id: str
    email: EmailStr
    password: str
    username: str
    gender: Gender
    is_staff: bool
    is_staff: bool
    
    model_config = {"from_attributes": True}
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    gender: Gender
    is_staff: Optional[bool] = False
    
    model_config = {"from_attributes": True}
    
class UserLogin(BaseModel):
    username: str
    password: str
    
# Response Model for user info (password hidden)
class UserOut(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    gender: Optional[Gender] = None
    is_staff: Optional[bool] = None
    is_active: Optional[bool] = None
    
    model_config = {"from_attributes": True}
    
# Token response returned on login
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {"from_attributes": True}

# Token payload data structure
class TokenData(BaseModel):
    username: Optional[str] = None