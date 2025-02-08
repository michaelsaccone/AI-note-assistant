from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from core.ai_pipelines.llm_prompts import TEXT_EXTRACTION_PROMPT
from core.ai_pipelines.models import client_extractor_llm


extraction_template = ChatPromptTemplate([
    ('system', TEXT_EXTRACTION_PROMPT),
    ('user', '{user_message}')
])
extraction_chain = extraction_template | client_extractor_llm | StrOutputParser()