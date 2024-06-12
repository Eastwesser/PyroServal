import os
import sys
import unittest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from app.database.database import engine, Base
from app.database.models.models import User

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestDatabase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        self.async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )

    async def asyncTearDown(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def test_add_user(self):
        async with self.async_session() as session:
            user = User(id=123, status='alive')
            session.add(user)
            await session.commit()

            result = await session.execute(select(User).where(User.id == 123))
            user_in_db = result.scalars().first()
            self.assertIsNotNone(user_in_db)
            self.assertEqual(user_in_db.status, 'alive')


if __name__ == '__main__':
    unittest.main()
