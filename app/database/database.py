from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.settings import settings
import app.models

engine = create_async_engine(settings.DATABASE_URL, echo=False)
session_fabric = async_sessionmaker(bind=engine, expire_on_commit=False)