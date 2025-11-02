from fastapi.responses import JSONResponse
from typing import Any
from ..schemas import ResponseModel

def success_response(message: str, data: Any = None, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content=ResponseModel(status="success", message=message, data=data).model_dump()
    )
    
def error_response(message: str, data: Any = None, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content=ResponseModel(status="error", message=message, data=data).model_dump()
    )