from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any
from ..schemas import ResponseModel

def success_response(message: str, data: Any = None, status_code: int = 200):
    # Convert Pydantic models to dicts
    if data is not None:
        if isinstance(data, list):
            data = [item.model_dump() if isinstance(item, BaseModel) else item for item in data]
        elif isinstance(data, BaseModel):
            data = data.model_dump()
    
    return JSONResponse(
        status_code=status_code,
        content=ResponseModel(status="success", message=message, data=data).model_dump()
    )
    
def error_response(message: str, data: Any = None, status_code: int = 500):
    # Convert Pydantic models to dicts
    if data is not None:
        if isinstance(data, list):
            data = [item.model_dump() if isinstance(item, BaseModel) else item for item in data]
        elif isinstance(data, BaseModel):
            data = data.model_dump()
    
    return JSONResponse(
        status_code=status_code,
        content=ResponseModel(status="error", message=message, data=data).model_dump()
    )