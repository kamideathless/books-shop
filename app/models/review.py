from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from sqlalchemy import ForeignKey, UniqueConstraint


class Review(Base):
    __tablename__ = "reviews"

    __table_args__ = (
        UniqueConstraint("book_id", "user_id", name="uq_review_book_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    rate: Mapped[float] = mapped_column()
    description: Mapped[str | None] = mapped_column()

    book: Mapped["Book"] = relationship("Book", back_populates="reviews")
    user: Mapped["User"] = relationship("User", back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review(id={self.id}, book_id={self.book_id}, user_id={self.user_id})>"