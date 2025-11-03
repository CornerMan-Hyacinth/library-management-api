from __future__ import annotations
from ..database import Base
from uuid import uuid4
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    books: Mapped[List["Book"]] = relationship("Book", back_populates="category") # type: ignore
    