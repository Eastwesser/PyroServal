import asyncio
import os
import sys

# Убедитесь, что директория проекта добавлена в sys.path перед импортом
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_URL


@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session")
async def engine():
    return create_async_engine(DB_URL, echo=True)


@pytest.fixture(scope="session")
async def async_session_factory(engine):
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest.fixture(scope="function")
async def session(async_session_factory):
    async with async_session_factory() as session:
        async with session.begin():
            yield session


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
