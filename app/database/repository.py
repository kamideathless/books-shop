from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.exceptions import NotFoundError


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_or_raise(self, id: int, options=None):
        stmt = select(self.model).where(self.model.id == id)
        if options:
            stmt = stmt.options(*options)
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        if item is None:
            raise NotFoundError(f"{self.model.__name__} {id} не найдена")
        return item

