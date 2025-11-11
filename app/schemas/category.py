from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    
class Category(CategoryBase):
    id: str
    model_config = {"from_attributes": True}
        
class CategoryCreate(CategoryBase):
    pass
    
class CategoryUpdate(BaseModel):
    name: Optional[str] = None