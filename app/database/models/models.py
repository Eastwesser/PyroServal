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
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50))
    status_updated_at = Column(DateTime, default=datetime.utcnow)
    last_message_time = Column(DateTime, default=datetime.utcnow)
    message_text = Column(String)
