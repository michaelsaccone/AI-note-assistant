import logging
import os

from dotenv import load_dotenv
load_dotenv()
from notion_client import Client as NotionClient, APIResponseError

from core.ai_pipelines.chains.text_note_organiser import NoteInfo
# from core.services.notion.models import BlockObject, Heading3Block

client = NotionClient(auth=os.environ['NOTION_API_KEY'])

logger = logging.getLogger(__name__)

def search_client_id_from_database(query):
    response = client.databases.query(
        database_id=os.environ['NOTION_DATABASE_ID'],
        filter={
            "property": "Name",  # Replace "Name" with the property you want to search
            "rich_text": {
                "contains": query  # This will search for entries where the text contains the query
            }
        }
    )
    print(response["results"][0])
    return [
        {
            "id": item["id"],
            "name": item["properties"]["Name"]["title"][0]["text"]["content"],
        } for item in response["results"]
    ]


async def add_note_block(page_id, note: NoteInfo):
    block = {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [
                {
                    "type": "mention",
                    "mention": {
                        "type": "date",
                        "date": {
                            "start": note.date,
                            "end": None,
                            "time_zone": None
                        }
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    "plain_text": note.date,
                    "href": None
                },
                {
                    "type": "text",
                    "text": {
                        "content": " " + note.title,
                        "link": None
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    "plain_text": " " + note.title,
                    "href": None
                }
            ],
            "is_toggleable": True,
            "color": "default",
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": p
                                }
                            }
                        ]
                    }
                } for p in note.content
            ]
            # "children": [child.model_dump(exclude_none=True) for child in note.content_children]
        }
    }

    # Insert the blocks
    insert_blocks_before_toggle(page_id, [block])


# Function to retrieve the page content
def get_page_content(page_id):
    try:
        response = client.pages.retrieve(page_id)
        return response
    except APIResponseError as e:
        print(f"Error retrieving page: {e}")
        return None


# Function to find the first toggle list item and insert blocks before it
def insert_blocks_before_toggle(page_id, blocks_to_insert):
    try:
        # Retrieve the page content
        page = get_page_content(page_id)
        if not page:
            return

        # Extract the blocks from the page
        blocks = client.blocks.children.list(page_id).get("results", [])

        # Find the index of the first toggle list item
        toggle_index = None
        for i, block in enumerate(blocks):
            if block.get("type") == "heading_3" and block.get("heading_3", {}).get("is_toggleable"):
                toggle_index = i
                break

        before_toggle_id = None
        # If no toggle list item is found, insert at the beginning
        if toggle_index is not None:
            before_toggle_id = blocks[toggle_index - 1]["id"]

        logger.info(f"Appending blocks in Notion page...")
        # Insert the new blocks before the toggle list item
        for block in reversed(blocks_to_insert):
            if before_toggle_id is None:
                client.blocks.children.append(page_id, children=[block])
            else:
                client.blocks.children.append(page_id, children=[block], after=before_toggle_id)

        logger.info("Blocks inserted successfully.")
    except APIResponseError as e:
        logger.error(f"Error inserting blocks: {e}")
