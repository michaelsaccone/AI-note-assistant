from sqlalchemy import Column, Integer, String, DateTime
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
