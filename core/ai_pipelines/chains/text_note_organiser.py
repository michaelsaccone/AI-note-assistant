from langchain_core.prompts import ChatPromptTemplate
from sympy.categories import Object

from core.ai_pipelines.llm_prompts import NOTE_ORGANISER_PROMPT
from core.ai_pipelines.models import writer_llm
from typing import List

from pydantic import BaseModel, Field

# Pydantic
class NoteInfo(BaseModel):
    """Note for the client."""
    date: str = Field(description="Date of the note (it can be either 'today', 'yesterday', or a specific date in the format 'YYYY-MM-DD')")
    title: str = Field(description="The title of the note to be added inside the toggle in the Notion page (maximum 3-4 words). Usually 'installazione demo', 'incontro cliente', 'chiamata', etc.")
    # content_children: List[BlockObject] = Field(description="The note itself to be added inside the toggle in the Notion page formatted as a list of blocks")
    content: List[str] = Field(description="The note itself to be added inside the toggle in the Notion page formatted as a simple list of paragraphs")

note_organiser_template = ChatPromptTemplate([
    ('system', NOTE_ORGANISER_PROMPT),
    ('user', '{user_note}')
])

note_organiser_chain = note_organiser_template | writer_llm.with_structured_output(NoteInfo)