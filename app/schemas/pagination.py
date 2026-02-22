from typing import Generic, List, TypeVar

from pydantic import BaseModel, field_validator, Field

T = TypeVar("T")


class PaginatedParams(BaseModel):
    page: int = Field(ge=1, default=1)
    page_size: int = 10

    @field_validator("page_size")
    @classmethod
    def validate_page_size(cls, v):
        allowed = [10, 25, 50, 100]
        if v not in allowed:
            raise ValueError(f"page_size должен быть одним из: {allowed}")
        return v


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True


class SearchParams(PaginatedParams):
    query: str = Field(min_length=1, max_length=128)