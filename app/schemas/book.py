from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    quantity: int
    category_id: str
    
class Book(BookBase):
    id: UUID
    class Config:
        from_attributes = True
    
class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    category_id: Optional[str] = None
    