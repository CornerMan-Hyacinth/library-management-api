from __future__ import annotations
from ..database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4

class Borrow(Base):
    __tablename__ = "borrows"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_email: Mapped[str] = mapped_column(String, ForeignKey("users.email"), nullable=False)
    book_id: Mapped[str] = mapped_column(String, ForeignKey("books.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="borrows") # type: ignore
    book: Mapped["Book"] = relationship("Book", back_populates="borrows") # type: ignore