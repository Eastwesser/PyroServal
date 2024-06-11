import asyncio
import logging
from datetime import datetime, timedelta

from sqlalchemy.future import select

from app.database.database import get_db
from app.database.models.models import User

logger = logging.getLogger(__name__)


async def send_message(client, user, message_text):
    try:
        await client.send_message(user.id, message_text)
        user.status_updated_at = datetime.now()
        user.last_message_time = datetime.now()
        user.message_text = message_text
        logger.info(f"Message sent to {user.id}: {message_text}")

    except Exception as e:
        logger.error(f"Error sending message to {user.id}: {e}")
        user.status = "dead"
        user.status_updated_at = datetime.now()


async def check_and_send_messages(client):
    while True:
        async with get_db() as db:
            now = datetime.now()
            async with db.begin():
                users = await db.execute(select(User).where(User.status == "alive"))
                users = users.scalars().all()

                for user in users:
                    time_since_last_message = now - user.last_message_time

                    if user.status == "alive" and time_since_last_message >= timedelta(
                            minutes=6) and user.message_text is None:
                        await send_message(client, user, "Текст1")
                        user.message_text = "Текст1"
                        user.status_updated_at = now

                    elif user.message_text == "Текст1" and time_since_last_message >= timedelta(minutes=39):
                        await send_message(client, user, "Текст2")
                        user.message_text = "Текст2"
                        user.status_updated_at = now

                    elif user.message_text == "Текст2" and time_since_last_message >= timedelta(days=1, hours=2):
                        await send_message(client, user, "Текст3")
                        user.message_text = "Текст3"
                        user.status = "finished"
                        user.status_updated_at = now

                    db.add(user)
                    await db.commit()

        await asyncio.sleep(60)
