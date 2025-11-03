from ..enums import Gender
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
    
class ReaderBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    gender: Gender
    
class Reader(ReaderBase):
    id: UUID
    class Config:
        from_attributes = True
        
class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[Gender] = None