from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class YearValidatorMixin(BaseModel):
    @field_validator("year", check_fields=False)
    @classmethod
    def validate_year(cls, v):
        if v is not None and v > datetime.now().year:
            raise ValueError("Значение не может быть в будущем")
        return v

class BookBase(YearValidatorMixin):
    title: str = Field(min_length=1, max_length=128)
    author: str = Field(min_length=1, max_length=128)
    year: int | None = None

class BookCreate(BookBase):
    pass

class BookUpdate(YearValidatorMixin):
    title: str | None = Field(None, min_length=1, max_length=128)
    author: str | None = Field(None, min_length=1, max_length=128)
    year: int | None = None

class BookResponse(BookBase):
    id: int
    avg_rating: float | None = None
    reviews_count: int = 0

    class Config:
        from_attributes = True