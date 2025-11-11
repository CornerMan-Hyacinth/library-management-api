from pydantic import BaseModel, EmailStr
from typing import Optional

class BorrowBase(BaseModel):
    user_email: EmailStr
    book_id: str
    
class Borrow(BorrowBase):
    id: str
    model_config = {"from_attributes": True}
    
class BorrowCreate(BorrowBase):
    pass
    
class BorrowUpdate(BaseModel):
    user_email: Optional[EmailStr] = None
    book_id: Optional[str] = None