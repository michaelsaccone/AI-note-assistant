from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import numpy as np
from . import models

def upsert_notion_item(
    db: Session,
    page_id: str,
    name: str,
    embedding: List[float],
    created_time: datetime,
    last_edited_time: datetime
) -> models.NotionItem:
    """
    Create a new Notion item or update an existing one if it has changed.
    Returns the created/updated item.
    """
    # Check if item exists
    existing_item = db.query(models.NotionItem).filter(models.NotionItem.page_id == page_id).first()
    
    if existing_item:
        # Update only if name or embedding has changed
        if existing_item.name != name:
            existing_item.name = name
            existing_item.embedding = embedding
            existing_item.last_edited_time = last_edited_time
            db.commit()
            db.refresh(existing_item)
        return existing_item
    
    # Create new item if it doesn't exist
    new_item = models.NotionItem(
        page_id=page_id,
        name=name,
        embedding=embedding,
        created_time=created_time,
        last_edited_time=last_edited_time
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def find_similar_texts(
    db: Session,
    query_embedding: List[float],
    limit: int = 3,
    similarity_threshold: float = 0.5
) -> List[models.NotionItem]:
    """
    Find similar texts using PostgreSQL's native vector similarity search.
    Returns the top 'limit' most similar items above the similarity threshold.
    
    Args:
        db: Database session
        query_embedding: The embedding vector to search with
        limit: Maximum number of results to return
        similarity_threshold: Minimum similarity score (0-1) for results
    
    Returns:
        List of NotionItem objects sorted by similarity
    """
    # Using cosine similarity with pgvector
    query = text("""
        WITH similarity_results AS (
            SELECT id, page_id, name, embedding, created_time, last_edited_time,
                   (1 - (embedding <=> CAST(:embedding AS vector(1024)))) as similarity
            FROM notion_items
            WHERE (1 - (embedding <=> CAST(:embedding AS vector(1024)))) > :threshold
            ORDER BY similarity DESC
            LIMIT :limit
        )
        SELECT id, REPLACE(page_id, '-', '') as page_id, name, embedding, created_time, last_edited_time
        FROM similarity_results;
    """)
    
    result = db.execute(
        query,
        {
            "embedding": query_embedding,
            "threshold": similarity_threshold,
            "limit": limit
        }
    )
    
    # Convert SQLAlchemy Row objects to dictionaries using _mapping
    return [models.NotionItem(**row._mapping) for row in result] 