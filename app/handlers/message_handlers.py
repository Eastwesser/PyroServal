import logging
from datetime import datetime

from pyrogram import Client, filters
from sqlalchemy.future import select

from app.database.database import get_db
from app.database.models.models import User

logger = logging.getLogger(__name__)


def register_handlers(app: Client):
    @app.on_message(filters.text)
    async def handle_message(client, message):
        logger.info("handle_message called")
        user_id = message.from_user.id
        text = message.text

        logger.info(f"Received message from {user_id}: {text}")

        async with get_db() as db:
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()

            if not user:
                logger.info(f"User {user_id} not found in database. Adding user.")
                user = User(id=user_id, message_text=text)
                db.add(user)
                await db.commit()
                logger.info(f"User {user_id} successfully added.")

            # Process message for trigger words
            if "прекрасно" in text or "ожидать" in text:
                user.status = "finished"
                user.status_updated_at = datetime.now()
                await db.commit()
                logger.info(f"User {user_id}'s status updated to 'finished'.")
                await message.reply("Your status has been updated to 'finished'.")
            else:
                logger.info(f"No trigger words found in message from {user_id}")
