from datetime import datetime, UTC
from typing import List
from sqlalchemy.orm import Session
from mistralai import Mistral

from core.database import crud, models
from .config import settings
from .notion_client import NotionClient

class NotionSearchService:
    def __init__(self, db: Session):
        self.db = db
        self.mistral_client = Mistral(api_key=settings.llm_api_keys.mistral)
        self.notion_client = NotionClient()
        self.last_sync = self._get_last_sync_time()
        
    def _get_last_sync_time(self) -> datetime:
        """Get the timestamp of the most recently updated item."""
        latest_item = self.db.query(models.NotionItem).order_by(
            models.NotionItem.last_edited_time.desc()
        ).first()
        return latest_item.last_edited_time if latest_item else datetime.min.replace(tzinfo=UTC)
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using Mistral's embedding model."""
        response = self.mistral_client.embeddings.create(
            model=settings.model_names.embedding,
            inputs=[text]
        )
        return response.data[0].embedding
    
    def sync_notion_items(self) -> None:
        """
        Synchronize Notion items with the database:
        1. Get changes from Notion since last sync
        2. Generate embeddings for new/updated items in batches
        3. Update database
        """
        # Get changes from Notion
        changes = self.notion_client.get_database_changes(
            since=self.last_sync,
            batch_size=settings.search.sync_batch_size
        )
        
        if not changes:
            return
            
        # Generate embeddings for all items in one batch
        texts = [item["name"] for item in changes]
        embeddings_response = self.mistral_client.embeddings.create(
            model=settings.model_names.embedding,
            inputs=texts
        )
        
        # Update database with items and their embeddings
        for item, embedding_data in zip(changes, embeddings_response.data):
            crud.upsert_notion_item(
                self.db,
                page_id=item["page_id"],
                name=item["name"],
                embedding=embedding_data.embedding,
                created_time=item["created_time"],
                last_edited_time=item["last_edited_time"]
            )
        
        # Update last sync time
        self.last_sync = datetime.now(UTC)
    
    def search_similar_texts(
        self,
        query: str,
        limit: int = None,
        similarity_threshold: float = None
    ) -> List[models.NotionItem]:
        """
        Search for similar texts in the Notion items.
        
        Args:
            query: The text to search for
            limit: Maximum number of results to return
            similarity_threshold: Minimum similarity score (0-1) for results
            
        Returns:
            List of similar NotionItem objects
        """
        # Use default values from settings if not provided
        if limit is None:
            limit = settings.search.max_results
        if similarity_threshold is None:
            similarity_threshold = settings.search.similarity_threshold

        # Generate embedding for the query
        query_embedding = self._generate_embedding(query)
        
        # Search for similar items
        return crud.find_similar_texts(
            self.db,
            query_embedding=query_embedding,
            limit=limit,
            similarity_threshold=similarity_threshold
        ) 