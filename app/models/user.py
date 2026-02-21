from typing import List
from enum import Enum as PyEnum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class UserRole(PyEnum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(String(32))
    hashed_password: Mapped[str] = mapped_column(String(128))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    name: Mapped[str] = mapped_column(String(56))
    age: Mapped[int | None] = mapped_column()

    reviews: Mapped[List["Review"]] = relationship(  # noqa: F821
        "Review",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"