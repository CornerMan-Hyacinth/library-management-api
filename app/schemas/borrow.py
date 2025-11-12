from pydantic import BaseModel
from typing import Optional

class BorrowBase(BaseModel):
    user_email: str
    book_id: str
    
class Borrow(BorrowBase):
    id: str
    model_config = {"from_attributes": True}
    
class BorrowCreate(BorrowBase):
    pass
    
class BorrowUpdate(BaseModel):
    user_email: Optional[str] = None
    book_id: Optional[str] = None