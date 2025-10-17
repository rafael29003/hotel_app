# app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    database_params = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    database_params = {}

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, **database_params)

# Создаем фабрику для асинхронных сесси
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass
