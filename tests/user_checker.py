import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv('DB_URL')

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def check_user():
    async with async_session() as session:
        result = await session.execute("SELECT * FROM users LIMIT 1;")
        user = result.fetchone()
        print(type(user))
        if user:
            print(user._mapping)  # For async results, use _mapping to access columns


asyncio.run(check_user())
