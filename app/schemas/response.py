from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None