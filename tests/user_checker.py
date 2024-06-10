import unittest
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import Config
from models.models import User, Base


class TestUserChecker(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.engine = create_async_engine(Config.DB_URL, echo=False)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession
        )
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def asyncTearDown(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await self.engine.dispose()

    async def test_user_in_database(self):
        user_id = 123456789
        async with self.SessionLocal() as session:
            new_user = User(
                id=user_id,
                created_at=datetime.utcnow(),
                status='alive',
                status_updated_at=datetime.utcnow(),
                last_message_time=datetime.utcnow(),
                message_text="Initial message"
            )
            session.add(new_user)
            await session.commit()

            user = await session.get(User, user_id)
            self.assertIsNotNone(user)
            self.assertEqual(user.id, user_id)
            self.assertEqual(user.message_text, "Initial message")

    async def test_user_not_in_database(self):
        user_id = 987654321
        async with self.SessionLocal() as session:
            user = await session.get(User, user_id)
            self.assertIsNone(user)


if __name__ == '__main__':
    unittest.main()
