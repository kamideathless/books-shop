from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.services.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    AuthError,
    WrongTokenType,
    TokenExpired,
    InvalidToken,
)


def register_exception_handlers(app):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_handler(request: Request, exc: AlreadyExistsError):
        return JSONResponse(status_code=409, content={"detail": exc.detail})

    @app.exception_handler(AuthError)
    async def auth_error_handler(request: Request, exc: AuthError):
        return JSONResponse(status_code=401, content={"detail": exc.detail})

    @app.exception_handler(WrongTokenType)
    async def wrong_token_type_handler(request: Request, exc: WrongTokenType):
        return JSONResponse(status_code=401, content={"detail": exc.detail})

    @app.exception_handler(TokenExpired)
    async def token_expired_handler(request: Request, exc: TokenExpired):
        return JSONResponse(status_code=401, content={"detail": exc.detail})

    @app.exception_handler(InvalidToken)
    async def invalid_token_handler(request: Request, exc: InvalidToken):
        return JSONResponse(status_code=401, content={"detail": exc.detail})

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "detail": [
                    {"field": e["loc"][-1], "msg": e["msg"]} for e in exc.errors()
                ]
            },
        )