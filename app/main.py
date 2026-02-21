from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.api.routes import books_router, users_router, shop_router
from app.core.exception_handlers import register_exception_handlers

app = FastAPI()
app.include_router(books_router)
app.include_router(users_router)
app.include_router(shop_router)


register_exception_handlers(app)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", tags=["ROOT"])
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())