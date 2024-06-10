from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import Config
from models.models import Base


def get_engine_and_session():
    db_url = Config.DB_URL
    async_engine = create_async_engine(
        db_url,
        echo=False,
        future=True
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession
    )

    return SessionLocal, async_engine


async def init_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
