import enum
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Enum, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StatusEnum(enum.Enum):
    ALIVE = "alive"
    DEAD = "dead"
    FINISHED = "finished"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(StatusEnum), default=StatusEnum.ALIVE)
    status_updated_at = Column(DateTime, default=datetime.utcnow)
    last_message_time = Column(DateTime, default=datetime.utcnow)
    message_text = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, status={self.status})>"
