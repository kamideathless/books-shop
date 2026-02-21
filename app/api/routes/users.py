from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends

from app.core.dependencies import require_admin
from app.schemas.auth import UserTokens, RefreshTokenRequest
from app.services.users import UserService, get_users_service
from app.schemas.user import UserRegister, UserResponse, UserCredentials


router = APIRouter(prefix="/users")
users_tag = ["Пользователи"]


@router.get(
    "/", tags=users_tag, name="Получить информацию о зарегистрированных пользователях"
)
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
    user: UserRegister, service: UserService = Depends(get_users_service)
) -> UserResponse:
    new_user = await service.register_new_user(user)
    return UserResponse.model_validate(new_user)


@router.post("/login/", tags=users_tag, name="Авторизация пользователя")
async def login_user(
    formdata: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_users_service),
) -> UserTokens:
    return await service.login_exist_user(
        UserCredentials(username=formdata.username, password=formdata.password)
    )


@router.post("/refresh/", tags=users_tag, name="Обновление токена")
async def refresh_access_tkn(
    body: RefreshTokenRequest, service: UserService = Depends(get_users_service)
) -> UserTokens:
    return service.refresh_access_token(body)