from datetime import datetime
from pydantic import BaseModel


class JWTPayload(BaseModel):
    uid: int
    exp: float | None = None
    iat: float | None = None
    token_type: str | None = None


class UserTokens(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str