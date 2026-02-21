from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    author: Mapped[str] = mapped_column(String(128))
    year: Mapped[int | None] = mapped_column()

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
    )
    shop: Mapped[Optional["ShopItem"]] = relationship(
        back_populates="book",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"