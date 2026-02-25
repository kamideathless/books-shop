from typing import List
from fastapi.params import Depends
from sqlalchemy import select, func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.database.repository import BaseRepository
from app.models.book import Book
from app.models.review import Review
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.schemas.pagination import PaginatedResponse
from app.schemas.review import ReviewCreate
from app.services.exceptions import NotFoundError, AlreadyExistsError
from app.utils.utils import paginate


class BooksService(BaseRepository):
    model = Book

    async def get_book_by_id(self, id: int) -> Book:
        result = await self.session.execute(
            select(Book, func.avg(Review.rate), func.count(Review.id))
            .outerjoin(Review)
            .where(Book.id == id)
            .group_by(Book.id)
        )
        row = result.first()
        if row is None:
            raise NotFoundError(f"Книга {id} не найдена")
        book, avg_rating, reviews_count = row
        book.avg_rating = round(avg_rating, 2) if avg_rating else None
        book.reviews_count = reviews_count
        return book

    @staticmethod
    def book_row_mapper(row):
        book, avg_rating, reviews_count = row
        book.avg_rating = round(avg_rating, 2) if avg_rating else None
        book.reviews_count = reviews_count
        return BookResponse.model_validate(book)

    async def get_all_books(self, page: int, page_size: int) -> PaginatedResponse[BookResponse]:
        stmt = (
            select(Book, func.avg(Review.rate), func.count(Review.id))
            .outerjoin(Review)
            .group_by(Book.id)
            .order_by(Book.id)
        )
        return await paginate(
            session=self.session,
            stmt=stmt,
            page=page,
            page_size=page_size,
            count_stmt=select(func.count()).select_from(Book),
            row_mapper=BooksService.book_row_mapper,
            use_scalars=False
        )

    async def create_book(self, body: BookCreate) -> Book:
        book = Book(**body.model_dump())
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete_book(self, id: int) -> None:
        book = await self.get_book_by_id(id)
        await self.session.delete(book)
        await self.session.commit()

    async def update_book(self, id: int, body: BookUpdate) -> Book:
        book = await self.get_book_by_id(id)
        for field, value in body.model_dump(exclude_none=True).items():
            setattr(book, field, value)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def get_reviews_by_book_id(self, book_id: int) -> list[Review]:
        await self.get_book_by_id(book_id)
        stmt = await self.session.execute(
            select(Review).where(Review.book_id == book_id)
        )
        reviews = list(stmt.scalars().all())
        if not reviews:
            raise NotFoundError(f"Отзывы на книгу {book_id} не найдены")
        return reviews

    async def create_book_review(
        self, book_id: int, body: ReviewCreate, user_id: int
    ) -> Review:
        await self.get_book_by_id(book_id)
        try:
            new_review = Review(**body.model_dump(), book_id=book_id, user_id=user_id)
            self.session.add(new_review)
            await self.session.commit()
            await self.session.refresh(new_review)
            return new_review
        except IntegrityError:
            await self.session.rollback()
            raise AlreadyExistsError(f"Вы уже оставили отзыв на книгу {book_id}")

    async def search_books(self, query: str) -> List[Book]:
        result = await self.session.execute(
            select(Book, func.avg(Review.rate), func.count(Review.id))
            .outerjoin(Review)
            .where(
                or_(
                    func.similarity(func.lower(Book.title), query.lower()) > 0.2,
                    func.similarity(func.lower(Book.author), query.lower()) > 0.2,
                )
            )
            .group_by(Book.id)
            .order_by(
                func.greatest(
                    func.similarity(func.lower(Book.title), query.lower()),
                    func.similarity(func.lower(Book.author), query.lower()),
                ).desc()
            )
        )
        rows = result.all()
        books = []
        for book, avg_rating, reviews_count in rows:
            book.avg_rating = round(avg_rating, 2) if avg_rating else None
            book.reviews_count = reviews_count
            books.append(book)
        return books

def get_books_service(session: AsyncSession = Depends(get_db)):
    return BooksService(session)