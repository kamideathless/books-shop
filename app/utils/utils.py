from datetime import datetime, timezone
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from app.auth.auth import auth
from app.schemas.auth import JWTPayload
from app.schemas.pagination import PaginatedResponse
from app.services.exceptions import TokenExpired, InvalidToken, NotFoundError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login/")


def create_jwt_token(payload: JWTPayload) -> str:
    now = datetime.now(timezone.utc)
    payload.iat = now.timestamp()
    encoded = jwt.encode(
        payload.model_dump(), auth.secret_key, algorithm=auth.algorithm
    )
    return encoded


def decode_jwt_token(token: str | bytes) -> dict[str, str]:
    try:
        return jwt.decode(token, auth.secret_key, algorithms=[auth.algorithm])
    except jwt.ExpiredSignatureError:
        raise TokenExpired(f"Токен {token} истёк")
    except jwt.InvalidTokenError:
        raise InvalidToken("Невалидный токен")


def create_access_token(payload: JWTPayload) -> str:
    now = datetime.now(timezone.utc).timestamp()
    payload.exp = now + auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload.token_type = "access"
    access_token = create_jwt_token(payload)
    return access_token


def create_refresh_token(payload: JWTPayload) -> str:
    now = datetime.now(timezone.utc).timestamp()
    payload.exp = now + auth.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    payload.token_type = "refresh"
    refresh_token = create_jwt_token(payload)
    return refresh_token


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    except ValueError:
        return False


async def paginate(
    session: AsyncSession,
    stmt,
    page: int,
    page_size: int,
) -> PaginatedResponse:
    count_query = select(func.count()).select_from(stmt.subquery())
    result = await session.execute(count_query)
    total = result.scalar()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0

    if page > total_pages > 0:
        raise NotFoundError(
            f"Страница {page} не существует, всего страниц: {total_pages}"
        )

    offset = (page - 1) * page_size
    result = await session.execute(stmt.offset(offset).limit(page_size))
    items = result.scalars().all()
    return PaginatedResponse(
        items=list(items),
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


EN_TO_RU = str.maketrans(
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~",
    "йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё",
)

# Русская → Английская
RU_TO_EN = str.maketrans(
    "йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё",
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~",
)


def switch_layout(text: str) -> list[str]:

    variants = [text]
    ru_variant = text.translate(EN_TO_RU)
    if ru_variant != text:
        variants.append(ru_variant)
    en_variant = text.translate(RU_TO_EN)
    if en_variant != text:
        variants.append(en_variant)

    return list(set(variants))
