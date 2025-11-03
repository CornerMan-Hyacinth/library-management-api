from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from .database import Base, engine
from .schemas.response import ResponseModel
from .routers import book, borrow, category, reader

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield # Application starts here
    
    # Shutdown: Clean up (if needed)
    await engine.dispose()

app = FastAPI(
    title="Library Management API",
    description="A Python-based database management setup using SQLAlchemy for ORM, Alembic for migrations, and python-dotenv for environment configuration. This project provides a clean, scalable structure for managing database models, connections, and schema updates — ideal for web applications and backend systems.",
    summary="Scalable Python database setup with SQLAlchemy ORM, Alembic migrations, and dotenv configuration.",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(book.router)
app.include_router(borrow.router)
app.include_router(category.router)
app.include_router(reader.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ResponseModel(status="error", message=str(exc), data=None).model_dump()
    )
    
