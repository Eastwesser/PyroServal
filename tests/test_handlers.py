import unittest
from datetime import datetime
from unittest.mock import AsyncMock

from pyrogram import Client

from bot.handlers import ClientHandler
from database.db_session import SessionLocal, init_db, async_engine
from models.models import User


class TestHandlers(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.app = AsyncMock(Client)
        await init_db(async_engine)
        self.client_handler = ClientHandler(self.app)

    async def asyncTearDown(self):
        async with SessionLocal() as session:
            await session.execute(User.__table__.delete())
            await session.commit()

    async def test_handle_incoming_message_new_user(self):
        user_id = 123456789
        message = AsyncMock()
        message.from_user.id = user_id
        message.text = "Hello, world!"

        await self.client_handler.handle_incoming_message(self.app, message)

        async with SessionLocal() as session:
            user = await session.get(User, user_id)
            self.assertIsNotNone(user)
            self.assertEqual(user.id, user_id)
            self.assertEqual(user.message_text, "Hello, world!")

    async def test_handle_incoming_message_existing_user(self):
        user_id = 123456789
        initial_text = "Initial message"
        new_text = "Updated message"

        async with SessionLocal() as session:
            user = User(
                id=user_id,
                created_at=datetime.utcnow(),
                status='alive',
                status_updated_at=datetime.utcnow(),
                last_message_time=datetime.utcnow(),
                message_text=initial_text
            )
            session.add(user)
            await session.commit()

        message = AsyncMock()
        message.from_user.id = user_id
        message.text = new_text

        await self.client_handler.handle_incoming_message(self.app, message)

        async with SessionLocal() as session:
            user = await session.get(User, user_id)
            self.assertIsNotNone(user)
            self.assertEqual(user.id, user_id)
            self.assertEqual(user.message_text, new_text)


if __name__ == '__main__':
    unittest.main()
