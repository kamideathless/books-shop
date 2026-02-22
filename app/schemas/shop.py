from pydantic import BaseModel, Field

from app.schemas.book import BookResponse


class ShopItemBase(BaseModel):
    price: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)


class ShopItemCreate(ShopItemBase):
    book_id: int


class ShopItemUpdate(ShopItemBase):
    pass


class ShopItemResponse(ShopItemBase):
    id: int
    book: BookResponse

    class Config:
        from_attributes = True
