from pydantic import BaseModel
from typing import TypeVar, Generic, Optional
from ..enums import ResponseStatus

T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    status: ResponseStatus
    message: str
    data: Optional[T] = None