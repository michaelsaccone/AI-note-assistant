from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from transformers import pipeline

from core.ai_pipelines.llm_prompts import TEXT_EXTRACTION_PROMPT


extraction_template = ChatPromptTemplate([
    ('system', TEXT_EXTRACTION_PROMPT),
    ('user', '{user_message}')
])
# extraction_chain = extraction_template | client_extractor_llm | StrOutputParser()


oracle = pipeline("question-answering", model="osiria/deberta-italian-question-answering")
