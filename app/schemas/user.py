from pydantic import BaseModel, Field

from app.models.user import UserRole


class UserBase(BaseModel):
    username: str = Field(min_length=6, max_length=32)
    name: str = Field(max_length=56)
    age: int | None = Field(None, gt=0, le=120)
    role: UserRole = Field(default=UserRole.USER)


class UserCredentials(BaseModel):
    username: str = Field(min_length=6, max_length=32)
    password: str = Field(min_length=8, max_length=32)


class UserRegister(UserCredentials):
    name: str = Field(max_length=56)
    age: int | None = Field(None, gt=0, le=120)


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserLogin(UserCredentials):
    pass