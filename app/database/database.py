from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DB_URL

engine = create_async_engine(
    DB_URL,
    echo=True,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


# Define get_db() as an asynchronous function
@asynccontextmanager
async def get_db():
    async with async_session() as session:
        yield session
