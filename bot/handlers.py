import logging
from datetime import datetime

from pyrogram import Client, filters

from bot.triggers import handle_triggers
from database.db_session import get_engine_and_session
from models.models import User

# Initialize database session and engine
SessionLocal, async_engine = get_engine_and_session()


def init_handlers(app: Client):
    app.add_handler(ClientHandler(app))


class ClientHandler:
    def __init__(self, app: Client):
        self.app = app
        self.app.on_message(filters.private)(self.handle_incoming_message)

    async def handle_incoming_message(self, client, message):
        user_id = message.from_user.id
        text = message.text

        logging.info(f"Received message from user {user_id}: {text}")
        trigger_status = await handle_triggers(text)
        logging.info(f"Trigger status for message: {trigger_status}")

        async with SessionLocal() as session:
            user = await session.get(User, user_id)
            logging.info(f"Type of user object: {type(user)}")

            if user is not None:
                logging.info(f"User object details: {user}")

            if user is None:
                user = User(
                    id=user_id,
                    created_at=datetime.utcnow(),
                    status='alive',
                    status_updated_at=datetime.utcnow(),
                    last_message_time=datetime.utcnow(),
                    message_text=text
                )
                session.add(user)
                await session.commit()
                logging.info(f"New user {user_id} added to the database with initial message: {text}")
            else:
                if isinstance(user, User):
                    user.message_text = text
                    user.status_updated_at = datetime.utcnow()
                    await session.commit()
                    logging.info(f"Updated message text for user {user_id}: {text}")
                else:
                    logging.error(f"Unexpected user type: {type(user)}. User data: {user}")
                    raise TypeError(f"Expected User object, got {type(user)}")
