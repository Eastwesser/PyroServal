import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models.models import Base


def init_db():
    db_url = os.getenv('DB_URL')
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

    async def init():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return SessionLocal, async_engine, init


SessionLocal, async_engine, init = init_db()
