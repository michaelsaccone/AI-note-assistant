from core.services.notion_search.service_manager import NotionSearchServiceManager
from core.database import init_db

def initialize_services() -> None:
    """
    Initialize all services that need to be started when the application starts.
    This should be called at application startup.
    """
    # Initialize database
    init_db()
    
    # Initialize Notion search service
    NotionSearchServiceManager.initialize() 