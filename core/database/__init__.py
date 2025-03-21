from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .models import Base
from core.services.notion_search.config import settings

engine = create_engine(settings.database.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database with required extensions and tables."""
    # Create pgvector extension if it doesn't exist
    with engine.connect() as connection:
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS vector;'))
        connection.commit()

    # Create all tables
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
