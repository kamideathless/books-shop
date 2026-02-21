from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base



class ShopItem(Base):
    __tablename__ = "shop_books"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), unique=True
    )
    price: Mapped[float] = mapped_column()
    stock: Mapped[int] = mapped_column(default=0)

    book: Mapped["Book"] = relationship("Book", back_populates="shop")