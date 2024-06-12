from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DB_URL

# Создание асинхронного двигателя базы данных
engine = create_async_engine(DB_URL, echo=True)

# Создание фабрики сессий для работы с базой данных
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


# Асинхронная функция для получения сессии базы данных
@asynccontextmanager
async def get_db():
    async with async_session() as session:
        yield session
