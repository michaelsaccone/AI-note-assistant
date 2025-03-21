
from .service import NotionSearchService
from .service_manager import NotionSearchServiceManager

# Convenience function to get the service instance
def get_notion_search_service() -> NotionSearchService:
    """
    Get the singleton instance of NotionSearchService.
    This is the preferred way to access the service throughout the application.
    """
    return NotionSearchServiceManager.get_instance() 