from pydantic import BaseModel
from app.models.transaction import TransactionStatus


class TransactionResponse(BaseModel):
    id: int
    idempotence_key: str
    shop_item_id: int
    user_id: int
    amount: float
    status: TransactionStatus

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    shop_item_id: int