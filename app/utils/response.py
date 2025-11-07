from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any
from ..schemas import ResponseModel
from ..enums import ResponseStatus

def _serialize(data: Any) -> Any:
    """Convert data into dict"""
    
    if data is None:
        return None
    if isinstance(data, list):
        return [
            item.model_dump() if isinstance(item, BaseModel) else item for item in data
        ]
    if isinstance(data, BaseModel):
        return data.model_dump()
    return data

def success_response(message: str, data: Any = None, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content=ResponseModel(
            status=ResponseStatus.SUCCESS, message=message, data=_serialize(data)
        ).model_dump()
    )
    
def error_response(message: str, data: Any = None, status_code: int = 500):
    return JSONResponse(
        status_code=status_code,
        content=ResponseModel(
            status=ResponseStatus.ERROR, message=message, data=_serialize(data)
        ).model_dump()
    )