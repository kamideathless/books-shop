import uuid
from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, contains_eager
from app.core.dependencies import get_db
from app.database.repository import BaseRepository
from app.models import ShopItem, Book, Review, Transaction
from app.models.transaction import TransactionStatus
from app.schemas.pagination import PaginatedParams, PaginatedResponse
from app.schemas.shop import ShopItemCreate, ShopItemUpdate, ShopItemResponse
from app.schemas.transaction import TransactionResponse
from app.services.exceptions import NotFoundError, AlreadyExistsError
from app.utils.utils import paginate


class ShopService(BaseRepository):
    model = ShopItem

    async def get_item_by_id(self, id: int) -> ShopItem:
        return await self._get_or_raise(id, options=[joinedload(ShopItem.book)])

    @staticmethod
    def shop_row_mapper(row):
        item, avg_rating, reviews_count = row
        item.book.avg_rating = round(avg_rating, 2) if avg_rating else None
        item.book.reviews_count = reviews_count
        return ShopItemResponse.model_validate(item)

    async def get_shop_items(self, params: PaginatedParams) -> PaginatedResponse:
        stmt = (
            select(ShopItem, func.avg(Review.rate), func.count(Review.id))
            .join(ShopItem.book)
            .outerjoin(Review, Review.book_id == ShopItem.book_id)
            .options(contains_eager(ShopItem.book))
            .group_by(ShopItem.id, Book.id)
        )
        count_stmt = select(func.count()).select_from(ShopItem)
        paginated_items = await paginate(
            session=self.session,
            stmt=stmt,
            page=params.page,
            page_size=params.page_size,
            count_stmt=count_stmt,
            row_mapper=ShopService.shop_row_mapper,
        )
        return paginated_items

    async def create_shop_item(self, shop_item: ShopItemCreate) -> ShopItem:
        res = await self.session.execute(
            select(Book).where(Book.id == shop_item.book_id)
        )
        if res.scalar_one_or_none() is None:
            raise NotFoundError(f"Книга {shop_item.book_id} не найдена")
        try:
            new_shop_item = ShopItem(**shop_item.model_dump())
            self.session.add(new_shop_item)
            await self.session.commit()
            result = await self.session.execute(
                select(ShopItem)
                .options(joinedload(ShopItem.book))
                .where(ShopItem.id == new_shop_item.id)
            )
            return result.scalar_one()
        except IntegrityError:
            await self.session.rollback()
            raise AlreadyExistsError(f"Книга {shop_item.book_id} уже есть в магазине")

    async def update_shop_item(
        self, shop_item_id: int, shop_item: ShopItemUpdate
    ) -> ShopItem:
        item = await self.get_item_by_id(shop_item_id)
        for field, value in shop_item.model_dump(exclude_none=True).items():
            setattr(item, field, value)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete_shop_item(self, shop_item_id: int) -> None:
        item = await self.get_item_by_id(shop_item_id)
        await self.session.delete(item)
        await self.session.commit()

    async def create_item_purchase(self, shop_item_id: int, user_id: int) -> dict:
        result = await self.session.execute(
            select(Transaction).where(
                Transaction.shop_item_id == shop_item_id,
                Transaction.user_id == user_id,
                Transaction.status == TransactionStatus.PENDING,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise AlreadyExistsError(
                f"Транзакция уже существует, url: http://localhost:8000/shop/pay/{existing.idempotence_key}"
            )

        item = await self.get_item_by_id(shop_item_id)
        idempotence_key = str(uuid.uuid4())
        transaction = Transaction(
            idempotence_key=idempotence_key,
            shop_item_id=shop_item_id,
            user_id=user_id,
            amount=item.price,
            status=TransactionStatus.PENDING,
        )
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)

        return {
            "transaction_id": transaction.id,
            "payment_id": idempotence_key,
            "amount": item.price,
            "user_id": transaction.user_id,
            "status": transaction.status,
            "confirmation_url": f"http://localhost:8000/shop/pay/{idempotence_key}",
            "description": f"Оплата книги: {item.book.title}",
        }

    async def get_transaction_by_id(self, transaction_id: int) -> TransactionResponse:
        result = await self.session.execute(
            select(Transaction).where(Transaction.id == transaction_id))
        transaction = result.scalar_one_or_none()
        if transaction is None:
            raise NotFoundError(f"Транзакция id: {transaction_id} не найдена")
        return transaction


def get_shop_items_service(session: AsyncSession = Depends(get_db)):
    return ShopService(session)
