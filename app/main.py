import asyncio
import logging

from pyrogram import Client

from app.config import API_ID, API_HASH, BOT_TOKEN
from app.handlers.message_handlers import register_handlers
from app.triggers.trigger_words import check_and_send_messages

logger = logging.getLogger(__name__)


async def create_client():
    client = Client(
        "pyro_serval",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

    await client.start()

    return client


async def main():
    client = await create_client()

    register_handlers(client)

    # Run other coroutines in the background if needed
    await check_and_send_messages(client)

    # Wait until the client disconnects
    await client.idle()


if __name__ == "__main__":
    asyncio.run(main())