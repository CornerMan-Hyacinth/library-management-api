from app.enums import Gender
from pydantic import BaseModel
from typing import Optional
    
class ProfileBase(BaseModel):
    email: str
    username: str
    gender: Gender
    phone_number: Optional[str] = None
    address: Optional[str] = None
    
class Profile(ProfileBase):
    id: str
    
    model_config = {"from_attributes": True}
        
class ProfileCreate(ProfileBase):
    user_id: str

class ProfileUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    gender: Optional[Gender] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
