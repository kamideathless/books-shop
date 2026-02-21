from fastapi import APIRouter, Depends, Response
from app.core.dependencies import require_admin
from app.models.user import User
from app.schemas.review import ReviewResponse, ReviewCreate
from app.services.books import BooksService, get_books_service
from app.schemas.book import BookResponse, BookCreate, BookUpdate
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/books")
books_tag = ["Книги"]
reviews_tag = ["Отзывы"]


@router.get("/", tags=books_tag, name="Получить все книги")
async def get_books(
    service: BooksService = Depends(get_books_service),
) -> list[BookResponse]:
    db_books = await service.get_all_books()
    return [BookResponse.model_validate(book) for book in db_books]

@router.post("/", tags=books_tag, name="Добавить книгу")
async def create_book(
    body: BookCreate,
    service: BooksService = Depends(get_books_service),
    _: None = Depends(require_admin),
) -> BookResponse:
    book = await service.create_book(body)
    return BookResponse.model_validate(book)

@router.get("/search", tags=books_tag, name="Поиск книги по названию или автору")
async def search_book_by_title_author(query: str, service: BooksService = Depends(get_books_service)) -> list[BookResponse]:
    books = await service.search_books(query)
    return [BookResponse.model_validate(book) for book in books]

@router.get("/{book_id}", tags=books_tag, name="Получить книгу из базы данных")
async def get_book(
    book_id: int, service: BooksService = Depends(get_books_service)
) -> BookResponse:
    book = await service.get_book_by_id(book_id)
    return BookResponse.model_validate(book)


@router.delete("/{book_id}", tags=books_tag, name="Удалить книгу из базы")
async def delete_book(
    book_id: int,
    service: BooksService = Depends(get_books_service),
    _: None = Depends(require_admin),
) -> Response:
    await service.delete_book(book_id)
    return Response(status_code=204)


@router.patch("/{book_id}", tags=books_tag, name="Обновить всю информацию по книге")
async def update_book(
    book_id: int, body: BookUpdate,
    service: BooksService = Depends(get_books_service),
    _: None = Depends(require_admin),
) -> BookResponse:
    updated_book = await service.update_book(book_id, body)
    return BookResponse.model_validate(updated_book)


@router.get("/{book_id}/reviews", tags=reviews_tag, name="Получить отзывы по книге")
async def get_reviews(
    book_id: int, service: BooksService = Depends(get_books_service)
) -> list[ReviewResponse]:
    reviews = await service.get_review_by_book_id(book_id)
    return [ReviewResponse.model_validate(review) for review in reviews]


@router.post("/{book_id}/reviews", tags=reviews_tag, name="Добавить отзыв по книге")
async def add_review(
    book_id: int,
    body: ReviewCreate,
    current_user: User = Depends(get_current_user),
    service: BooksService = Depends(get_books_service),
) -> ReviewResponse:
    new_review = await service.create_book_review(book_id, body, current_user.id)
    return ReviewResponse.model_validate(new_review)