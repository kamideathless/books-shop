from app.api.routes.books import router as books_router
from app.api.routes.users import router as users_router
from app.api.routes.shop import router as shop_router


__all__ = ["books_router", "users_router", "shop_router"]