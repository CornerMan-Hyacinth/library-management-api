from __future__ import annotations
from ..database import Base
from ..enums import Gender
from sqlalchemy import String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from uuid import uuid4

class Reader(Base):
    __tablename__ = "readers"
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[Gender] = mapped_column(SqlEnum(Gender), nullable=False)
    borrows: Mapped[List["Borrow"]] = relationship("Borrow", back_populates="reader") # type: ignore
    