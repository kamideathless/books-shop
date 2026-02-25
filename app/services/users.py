from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.database.repository import BaseRepository
from app.schemas.auth import JWTPayload, UserTokens, RefreshTokenRequest
from app.schemas.user import UserRegister, UserCredentials
from app.models.user import User
from app.services.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    AuthError,
    WrongTokenType,
)
from app.utils.utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
)


class UserService(BaseRepository):
    model = User

    async def get_all_users(self) -> list[User]:
        result = await self.session.execute(select(User).order_by(User.id))
        return list(result.scalars().all())

    async def get_user_by_id(self, id: int) -> User:
        return await self._get_or_raise(id)

    async def register_new_user(self, body: UserRegister) -> User:
        result = await self.session.execute(
            select(User.username).where(User.username == body.username)
        )
        if result.scalar_one_or_none() is not None:
            raise AlreadyExistsError(
                f"Пользователь с ником {body.username} уже существует."
            )
        new_user = User(
            **body.model_dump(), hashed_password=hash_password(body.password)
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def login_exist_user(self, body: UserCredentials) -> UserTokens:
        result = await self.session.execute(
            select(User).where(User.username == body.username)
        )
        user = result.scalar_one_or_none()
        if user is None or not verify_password(body.password, user.hashed_password):
            raise AuthError("Неправильное имя пользователя или пароль")
        access_token = create_access_token(JWTPayload(uid=user.id))
        refresh_token = create_refresh_token(JWTPayload(uid=user.id))
        return UserTokens(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def refresh_access_token(body: RefreshTokenRequest) -> UserTokens:
        payload = decode_jwt_token(body.refresh_token)
        if payload["token_type"] != "refresh":
            raise WrongTokenType("Неправильный тип токена")
        new_access_token = create_access_token(JWTPayload(uid=int(payload["uid"])))
        return UserTokens(
            access_token=new_access_token, refresh_token=body.refresh_token
        )


def get_users_service(session: AsyncSession = Depends(get_db)):
    return UserService(session)


