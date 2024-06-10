import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Define get_engine_and_session function
def get_engine_and_session():
    return async_engine, SessionLocal


# Ensure DB_URL is correctly accessed
engine_url = os.getenv('DB_URL')
if not engine_url:
    raise ValueError("DB_URL environment variable is not set")

# Create async engine
async_engine = create_async_engine(engine_url, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

# Base model
Base = declarative_base()


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
