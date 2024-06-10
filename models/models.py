import os
from datetime import datetime
from sqlalchemy import BigInteger
from sqlalchemy import Column, Integer, DateTime, String, create_engine
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Assuming you have the engine_url defined somewhere as a string
engine_url = os.getenv('DB_URL')

# Create the engine
engine = create_engine(engine_url)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

StatusEnum = ENUM('alive', 'dead', 'finished', name='status_enum')


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(StatusEnum, default='alive')
    status_updated_at = Column(DateTime, default=datetime.utcnow)
    last_message_time = Column(DateTime, default=datetime.utcnow)
    message_text = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, status={self.status})>"
