import asyncio
import logging

from pyrogram import Client

from bot.handlers import init_handlers
from bot.utils import process_messages
from config import Config
from database.db_session import get_engine_and_session, init_db


async def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    app = Client(
        'pyro_bot',
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN
    )

    process_task = None
    try:
        logging.info("Starting the bot")
        await app.start()

        SessionLocal, async_engine = get_engine_and_session()
        await init_db(async_engine)

        init_handlers(app)
        process_task = asyncio.create_task(process_messages(app, SessionLocal))
        await process_task
    except KeyboardInterrupt:
        logging.info("Bot stopped by the user")
    except Exception as e:
        logging.error(f"An error occurred while running the bot: {e}")
    finally:
        if process_task is not None:
            process_task.cancel()
            try:
                await process_task
            except asyncio.CancelledError:
                pass
        logging.info("Stopping the bot")
        await app.stop()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by the user")
