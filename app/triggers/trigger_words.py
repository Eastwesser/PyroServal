import asyncio
import logging
from datetime import datetime, timedelta

from pyrogram import Client, filters
from sqlalchemy.future import select

from app.database.database import get_db
from app.database.models.models import User

logger = logging.getLogger(__name__)


# Функция для проверки наличия слов-триггеров в сообщениях пользователя
async def check_for_trigger_words(client: Client, user: User):
    async with get_db() as db:
        async with db.begin():
            result = await db.execute(select(User).where(User.id == user.id))
            user = result.scalars().first()
            if user.message_text:
                message_text_lower = user.message_text.lower()  # Преобразование сообщения в нижний регистр
                if "прекрасно" in message_text_lower or "ожидать" in message_text_lower:
                    user.status = "finished"
                    await db.commit()
                    return True
            return False


# Функция для отправки сообщения пользователю
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


# Функция для проверки и отправки сообщений по расписанию
async def check_and_send_messages(client: Client):
    @client.on_message(filters.text & filters.private)
    async def check_message(client, message):
        logger.info(f"Checking message from {message.from_user.id}")
        if "trigger" in message.text.lower():  # Преобразование сообщения в нижний регистр
            await message.reply("Trigger word detected!")
            logger.info(f"Replied to message with trigger word from {message.from_user.id}.")

    while True:
        logger.info("Running scheduled message checks")
        try:
            async with get_db() as db:
                now = datetime.now()
                async with db.begin():
                    users = await db.execute(select(User).where(User.status == "alive"))
                    users = users.scalars().all()

                    for user in users:
                        logger.info(f"Checking user {user.id} with status {user.status}")
                        time_since_last_message = now - user.last_message_time
                        logger.info(f"Time since last message for user {user.id}: {time_since_last_message}")

                        if user.status == "alive" and time_since_last_message >= timedelta(
                                minutes=6) and user.message_text is None:
                            if await check_for_trigger_words(client, user):
                                logger.info(f"Trigger word found for user {user.id}, stopping message sequence.")
                                continue
                            await send_message(client, user, "Текст1")
                            user.message_text = "Текст1"
                            user.status_updated_at = now

                        elif user.message_text == "Текст1" and time_since_last_message >= timedelta(minutes=39):
                            if await check_for_trigger_words(client, user):
                                logger.info(f"Trigger word found for user {user.id}, stopping message sequence.")
                                continue
                            await send_message(client, user, "Текст2")
                            user.message_text = "Текст2"
                            user.status_updated_at = now

                        elif user.message_text == "Текст2" and time_since_last_message >= timedelta(days=1, hours=2):
                            if await check_for_trigger_words(client, user):
                                logger.info(f"Trigger word found for user {user.id}, stopping message sequence.")
                                continue
                            await send_message(client, user, "Текст3")
                            user.message_text = "Текст3"
                            user.status = "finished"
                            user.status_updated_at = now

                        db.add(user)
                        await db.commit()
                        logger.info(f"Updated user {user.id} in the database")
        except Exception as e:
            logger.error(f"Error during scheduled message checks: {e}")

        await asyncio.sleep(60)
        logger.info("Sleeping for 60 seconds")
