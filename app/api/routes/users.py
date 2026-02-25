from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Response, Request, HTTPException
from app.core.dependencies import require_admin
from app.schemas.auth import UserTokens, RefreshTokenRequest
from app.services.users import UserService, get_users_service
from app.schemas.user import UserRegister, UserResponse, UserCredentials
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/users")
users_tag = ["Пользователи"]


@router.get(
    "/", tags=users_tag, name="Получить информацию о зарегистрированных пользователях"
)
@cache(expire=60)
async def get_users(
    service: UserService = Depends(get_users_service),
    _: None = Depends(require_admin),
) -> list[UserResponse]:
    users = await service.get_all_users()
    return [UserResponse.model_validate(user) for user in users]


@router.get("/{user_id}/", tags=users_tag, name="Получить информацию по user_id")
async def get_user(
    user_id: int, service: UserService = Depends(get_users_service)
) -> UserResponse:
    user = await service.get_user_by_id(user_id)
    return UserResponse.model_validate(user)


@router.post("/register/", tags=users_tag, name="Регистрация пользователя")
async def register_user(
    response: Response,
    user: UserRegister, service: UserService = Depends(get_users_service)
) -> UserResponse:
    new_user = await service.register_new_user(user)
    tokens = await service.login_exist_user(UserCredentials(username=user.username, password=user.password))
    response.set_cookie("access_token", tokens.access_token)
    response.set_cookie("refresh_token", tokens.refresh_token)
    return UserResponse.model_validate(new_user)


@router.post("/login/", tags=users_tag, name="Авторизация пользователя")
async def login_user(
    response: Response,
    formdata: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_users_service),
) -> UserTokens:
    tokens = await service.login_exist_user(
        UserCredentials(username=formdata.username, password=formdata.password)
    )
    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True, samesite="lax")
    return tokens

@router.post("/logout/")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Выход выполнен"}

@router.post("/refresh/", tags=users_tag, name="Обновление токена")
async def refresh_access_tkn(
    request: Request,
    response: Response,
    service: UserService = Depends(get_users_service)
) -> UserTokens:
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Refresh токен не найден")
    tokens = service.refresh_access_token(RefreshTokenRequest(refresh_token=refresh_token))
    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True, samesite="lax")
    return tokens