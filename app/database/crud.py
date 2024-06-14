import logging
from datetime import datetime

from app.database.database import get_db
from app.database.models.models import User


# Функция для добавления нового пользователя в базу данных
async def add_user(user_id):
    logging.info(f"Adding user with ID: {user_id}")
    async with get_db() as db:
        user = User(
            id=user_id,
            created_at=datetime.now(),
            status="alive",
            status_updated_at=datetime.now(),
            last_message_time=datetime.now(),
        )
        db.add(user)
        await db.commit()
        logging.info(f"User {user_id} added to the database")
