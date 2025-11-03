from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .schemas.response import ResponseModel

app = FastAPI(
    title="Library Management API",
    description="A Python-based database management setup using SQLAlchemy for ORM, Alembic for migrations, and python-dotenv for environment configuration. This project provides a clean, scalable structure for managing database models, connections, and schema updates — ideal for web applications and backend systems.",
    summary="Scalable Python database setup with SQLAlchemy ORM, Alembic migrations, and dotenv configuration.",
    version="0.1.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ResponseModel(status="error", message=str(exc), data=None).model_dump()
    )