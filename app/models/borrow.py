from ..database import Base
from __future__ import annotations
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4

class Borrow(Base):
    __tablename__ = "borrows"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    reader_id: Mapped[str] = mapped_column(String, ForeignKey("readers.id"), nullable=False)
    book_id: Mapped[str] = mapped_column(String, ForeignKey("books.id"), nullable=False)
    reader: Mapped["Reader"] = relationship("Reader", back_populates="borrows") # type: ignore
    book: Mapped["Book"] = relationship("Book", back_populates="borrows") # type: ignore