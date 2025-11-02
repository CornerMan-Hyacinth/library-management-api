from __future__ import annotations
from uuid import uuid4
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
## from sqlalchemy.dialects.postgresql import UUID ## for production postgresql
from ..database import Base

class Book(Base):
    __tablename__ = "books"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    category_id: Mapped[str] = mapped_column(String, ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="books") # type: ignore
    borrows: Mapped[List["Borrow"]] = relationship("Borrow", back_populates="book") # type: ignore