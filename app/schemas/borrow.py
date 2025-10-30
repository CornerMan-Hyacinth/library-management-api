from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BorrowBase(BaseModel):
    reader_id: str
    book_id: str
    
class Borrow(BorrowBase):
    id: str
    
class BorrowUpdateRequest(BaseModel):
    reader_id: Optional[str] = None
    book_id: Optional[str] = None