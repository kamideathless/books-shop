from typing import Any
from pydantic import BaseModel, Field, field_validator


class ReviewBase(BaseModel):
    rate: float = Field(ge=1, le=5)
    description: str | None = None

    @field_validator("rate")
    @classmethod
    def validate_rate(cls, value: Any) -> float:
        if value % 0.5 != 0:
            raise ValueError("Рейтинг должен быть кратным 0.5")
        return value


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    book_id: int
    user_id: int

    class Config:
        from_attributes = True