from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    category_id: str
    
class Book(BookBase):
    id: UUID
    class Config:
        orm_mode = True
    
class BookCreateRequest(BookBase):
    pass

class BookUpdateRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None