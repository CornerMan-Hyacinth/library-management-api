from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CategoryBase(BaseModel):
    name: str
    
class Category(CategoryBase):
    id: UUID
    class Config:
        from_attributes = True
        
class CategoryCreate(CategoryBase):
    pass
    
class CategoryUpdate(BaseModel):
    name: Optional[str] = None