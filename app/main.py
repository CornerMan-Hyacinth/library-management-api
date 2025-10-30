from fastapi import FastAPI

app = FastAPI(
    title="Library Management API",
    description="A Python-based database management setup using SQLAlchemy for ORM, Alembic for migrations, and python-dotenv for environment configuration. This project provides a clean, scalable structure for managing database models, connections, and schema updates — ideal for web applications and backend systems.",
    summary="Scalable Python database setup with SQLAlchemy ORM, Alembic migrations, and dotenv configuration.",
    version="0.1.0"
)

