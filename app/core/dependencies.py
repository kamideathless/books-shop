from typing import AsyncGenerator
from fastapi import Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import session_fabric
from app.models import User
from app.models.user import UserRole
from app.utils.utils import oauth2_scheme, decode_jwt_token


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_fabric() as session:
        yield session


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status_code=401, detail="Не авторизован")
    payload = decode_jwt_token(token)
    if payload["token_type"] != "access":
        raise HTTPException(status_code=401, detail="Неправильный тип токена")
    result = await db.execute(select(User).where(User.id == int(payload["uid"])))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user


async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Недостаточно прав")