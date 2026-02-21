from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.core.dependencies import get_db
from app.database.repository import BaseRepository
from app.models import ShopItem, Book
from app.schemas.pagination import PaginatedParams, PaginatedResponse
from app.schemas.shop import ShopItemCreate, ShopItemUpdate
from app.services.exceptions import NotFoundError, AlreadyExistsError
from app.utils.utils import paginate


class ShopService(BaseRepository):
    model = ShopItem

    async def get_item_by_id(self, id: int) -> ShopItem:
        return await self._get_or_raise(id)

    async def get_shop_items(self, params: PaginatedParams) -> PaginatedResponse:
        stmt = select(ShopItem).options(joinedload(ShopItem.book))
        paginated_items = await paginate(
            session=self.session, stmt=stmt, page=params.page, page_size=params.page_size
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
                .where(ShopItem.id == new_shop_item.id))
            return result.scalar_one()
        except IntegrityError:
            await self.session.rollback()
            raise AlreadyExistsError(f"Книга {shop_item.book_id} уже есть в магазине")

    async def update_shop_item(self, shop_item_id: int, shop_item: ShopItemUpdate) -> ShopItem:
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


def get_shop_items_service(session: AsyncSession = Depends(get_db)):
    return ShopService(session)
