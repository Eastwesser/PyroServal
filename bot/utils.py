import asyncio
import logging
import re
from datetime import datetime, timedelta

from bot.triggers import handle_triggers
from models.models import StatusEnum
from models.models import User


def calculate_next_message_time(last_message_time, interval):
    return last_message_time + interval


def parse_interval(text):
    pattern = r'(?:(\d+)\s*day[s]*\s*)?(?:(\d+)\s*hour[s]*\s*)?(?:(\d+)\s*min[s]*\s*)?'
    match = re.search(pattern, text)
    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    interval = timedelta(days=days, hours=hours, minutes=minutes)
    return interval


# Function to send a message to a user
async def send_message(client, user_id, text):
    try:
        await client.send_message(user_id, text)
        logging.info(f"Message sent to user {user_id}: {text}")
    except Exception as e:
        logging.error(f"Error sending message to user {user_id}: {e}")
        raise e


# Function to process messages and send scheduled messages
async def process_messages(client, session_factory):
    try:
        while True:
            async with session_factory() as session:
                result = await session.execute(User.__table__.select().where(User.status == 'alive'))
                users = result.scalars().all()
                for user in users:
                    trigger_status = await handle_triggers(user.message_text)
                    if trigger_status == 'finished':
                        user.status = 'finished'
                        user.status_updated_at = datetime.utcnow()
                        logging.info(f"User {user.id} status updated to 'finished'")
                        await send_message(
                            client,
                            user.id,
                            "Ваша воронка успешно завершена!"
                        )
                    elif trigger_status == 'waiting':
                        user.status = 'waiting'
                        user.status_updated_at = datetime.utcnow()
                        logging.info(f"User {user.id} status updated to 'waiting'")
                        await send_message(
                            client,
                            user.id,
                            "Вы находитесь в состоянии ожидания. Мы свяжемся с вами в ближайшее время."
                        )
                    else:
                        interval = parse_interval(user.message_text)
                        next_message_time = calculate_next_message_time(user.last_message_time, interval)
                        sleep_duration = (next_message_time - datetime.utcnow()).total_seconds()

                        logging.info(
                            f"Sleeping for {sleep_duration} seconds before sending the next message to user {user.id}"
                        )

                        await asyncio.sleep(sleep_duration)
                        await send_message(client, user.id, "Текст2")
                        user.last_message_time = datetime.utcnow()
                        user.status_updated_at = datetime.utcnow()

                        logging.info(f"Message sent to user {user.id} and status updated")

                    await session.commit()
            logging.info("Sleeping for 60 seconds before checking the next batch of messages")
            await asyncio.sleep(60)
    except asyncio.CancelledError:
        logging.info("process_messages task cancelled")
    except Exception as e:
        logging.error(f"An error occurred while processing messages: {e}")
