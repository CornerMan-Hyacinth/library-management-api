from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CategoryBase(BaseModel):
    name: str
    
class Category(CategoryBase):
    id: UUID
    class Config:
        orm_mode = True
    
class CategoryUpdateRequest(BaseModel):
    name: Optional[str] = None