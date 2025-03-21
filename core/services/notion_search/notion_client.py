from datetime import datetime
from typing import List, Dict, Any
from notion_client import Client
from .config import settings

class NotionClient:
    def __init__(self):
        self.client = Client(auth=settings.notion.api_key)
        self.database_id = settings.notion.database_id
    
    def get_database_changes(
        self,
        since: datetime,
        batch_size: int = settings.search.sync_batch_size
    ) -> List[Dict[str, Any]]:
        """
        Get all changes from Notion database since the specified timestamp.
        Uses pagination to fetch all results, not just the first 100.
        
        Args:
            since: Timestamp to get changes since
            batch_size: Number of items to fetch per page (max 100)
            
        Returns:
            List of page items with their IDs and names
        """
        # Convert datetime to ISO format for Notion API
        since_iso = since.isoformat()
        
        # Ensure batch_size doesn't exceed Notion's maximum
        batch_size = min(batch_size, 100)
        
        items = []
        has_more = True
        next_cursor = None
        
        while has_more:
            # Query the database for pages updated since the timestamp
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "timestamp": "last_edited_time",
                    "last_edited_time": {
                        "after": since_iso
                    }
                },
                page_size=batch_size,
                start_cursor=next_cursor
            )
            
            # Extract relevant information from the response
            for page in response.get("results", []):
                # Get the page title (assuming it's the first property)
                title_property = page["properties"]["Name"]["title"]
                if len(title_property) == 0:
                    continue

                title = title_property[0]["text"]["content"]
                items.append({
                    "page_id": page["id"],
                    "name": title,
                    "last_edited_time": page["last_edited_time"],
                    "created_time": page["created_time"]
                })
            
            # Check if there are more results and get the next cursor
            has_more = response.get("has_more", False)
            next_cursor = response.get("next_cursor")
        
        return items
    
    def _extract_property_value(self, property_data: Dict[str, Any]) -> Any:
        """Extract the value from a Notion property based on its type."""
        prop_type = property_data["type"]
        
        if prop_type == "rich_text":
            return property_data["rich_text"][0]["plain_text"] if property_data["rich_text"] else ""
        elif prop_type == "select":
            return property_data["select"]["name"] if property_data["select"] else None
        elif prop_type == "multi_select":
            return [option["name"] for option in property_data["multi_select"]]
        elif prop_type == "date":
            return property_data["date"]["start"] if property_data["date"] else None
        elif prop_type == "checkbox":
            return property_data["checkbox"]
        elif prop_type == "number":
            return property_data["number"]
        elif prop_type == "url":
            return property_data["url"]
        elif prop_type == "email":
            return property_data["email"]
        elif prop_type == "phone_number":
            return property_data["phone_number"]
        else:
            return None 