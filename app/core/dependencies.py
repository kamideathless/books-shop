from typing import AsyncGenerator

from fastapi import Depends, HTTPException
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
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_jwt_token(token)
    if payload["token_type"] != "access":
        raise HTTPException(status_code=401, detail="Неправильный тип токена")
    stmt = select(User).where(User.id == int(payload["uid"]))
    res = await session.execute(stmt)
    current_user = res.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return current_user


async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Недостаточно прав")