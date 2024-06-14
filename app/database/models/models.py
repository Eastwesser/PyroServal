from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    String,
    BigInteger,
)

from app.database.database import Base


# Определение модели пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String(10), default="alive")
    status_updated_at = Column(DateTime, default=datetime.now)
    last_message_time = Column(DateTime, default=datetime.now)
    message_text = Column(String)
