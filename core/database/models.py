from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, UTC
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.declarative import declarative_base
from .config import Base

Base = declarative_base()

class NotionItem(Base):
    __tablename__ = "notion_items"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    embedding = Column(Vector(1024))  # Using pgvector for efficient similarity search
    created_time = Column(DateTime)
    last_edited_time = Column(DateTime)

    def __repr__(self):
        return f"<NotionItem(page_id='{self.page_id}', name='{self.name}')>"

class TelegramUser(Base):
    __tablename__ = "telegram_users"

    telegram_id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    has_permission = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    def __repr__(self):
        return f"<TelegramUser(telegram_id={self.telegram_id}, username='{self.username}')>"
