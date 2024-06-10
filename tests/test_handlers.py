import os
import sys
import unittest
import warnings
from datetime import datetime
from unittest.mock import MagicMock

from pyrogram.types import Message, User as PyrogramUser
from sqlalchemy import select

from bot.handlers import ClientHandler
from database.db_session import init_db
from models.models import User

# Add the 'tests' directory to the module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


async def query_user(session, user_id):
    result = await session.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


class TestHandlers(unittest.TestCase):
    def setUp(self):
        # Initialize the database
        self.SessionLocal, self.async_engine, self.init = init_db()
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        self.init()

    def tearDown(self):
        # Clean up the database after each test
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        self.async_engine.dispose()

    async def test_handle_incoming_message(self):
        # Create a fake client and message
        app = MagicMock(name="Client")
        app.send_message = MagicMock()

        fake_user_id = 12345
        fake_text = "test message"
        fake_message = Message(
            id=1,
            date=datetime.utcnow(),
            chat=PyrogramUser(id=fake_user_id, is_bot=False, first_name="Test"),
            from_user=PyrogramUser(id=fake_user_id, is_bot=False, first_name="Test"),
            text=fake_text,
            client=app
        )

        # Initialize the handler and call the message handler
        handler = ClientHandler(app)
        await handler.handle_incoming_message(app, fake_message)

        # Check the database for the new user
        async with self.SessionLocal() as session:
            user = await query_user(session, fake_user_id)
            self.assertIsNotNone(user)
            self.assertEqual(user.message_text, fake_text)


if __name__ == '__main__':
    unittest.main()
