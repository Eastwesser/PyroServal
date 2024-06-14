import asyncio
import logging

from pyrogram import Client, idle

from app.config import (
    API_ID,
    API_HASH,
    SESSION_NAME,
)
from app.handlers.message_handlers import register_handlers
from app.triggers.trigger_words import check_and_send_messages

logger = logging.getLogger(__name__)


# Функция для создания клиента Pyrogram
async def create_client():
    client = Client(
        SESSION_NAME,
        api_id=API_ID,
        api_hash=API_HASH,
    )
    await client.start()
    return client


# Основная функция
async def main():
    client = await create_client()
    register_handlers(client)

    # Запуск задачи для проверки и отправки сообщений в фоновом режиме
    asyncio.create_task(check_and_send_messages(client))

    # Ожидание отключения клиента
    await idle()


if __name__ == "__main__":
    asyncio.run(main())
