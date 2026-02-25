from enum import Enum as PyEnum
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class TransactionStatus(PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    EXPIRED = "expired"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    idempotence_key: Mapped[str] = mapped_column(String(36), unique=True)
    shop_item_id: Mapped[int] = mapped_column(ForeignKey("shop_books.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    amount: Mapped[float] = mapped_column(Float())
    status: Mapped[TransactionStatus] = mapped_column(default=TransactionStatus.PENDING)