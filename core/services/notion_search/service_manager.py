from typing import Optional
from sqlalchemy.orm import Session
from .service import NotionSearchService
from core.database import get_db

class NotionSearchServiceManager:
    _instance: Optional[NotionSearchService] = None
    _initialized: bool = False

    @classmethod
    def get_instance(cls, db: Optional[Session] = None) -> NotionSearchService:
        """
        Get or create the singleton instance of NotionSearchService.
        
        Args:
            db: Optional database session. If not provided, a new one will be created.
            
        Returns:
            The singleton instance of NotionSearchService
        """
        if cls._instance is None:
            if db is None:
                db = next(get_db())
            cls._instance = NotionSearchService(db)
        return cls._instance

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the service by syncing with Notion.
        This should be called at application startup.
        """
        if not cls._initialized:
            service = cls.get_instance()
            service.sync_notion_items()
            cls._initialized = True

    @classmethod
    def reset(cls) -> None:
        """
        Reset the singleton instance.
        Useful for testing or when you need to force a new instance.
        """
        cls._instance = None
        cls._initialized = False 