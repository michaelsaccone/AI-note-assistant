import os

from langchain.chains import LLMChain
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from llm_prompts import TEXT_EXTRACTION_PROMPT


def get_llm_model(model_name):
    if 'gpt' in model_name:
        model = ChatOpenAI(model=model_name, temperature=0.4)
    else:
        model = ChatOllama(model=model_name, temperature=0.4)
    return model

client_extractor = get_llm_model(os.environ['CLIENT_EXTRACTOR_MODEL_NAME'])
reasoner = get_llm_model(os.environ['REASERNEER_MODEL_NAME'])
tool_caller = get_llm_model(os.environ['TOOLCALL_MODEL_NAME'])
writer = get_llm_model(os.environ['WRITER_MODEL_NAME'])

extraction_template = ChatPromptTemplate([
    ('system', TEXT_EXTRACTION_PROMPT)
])

def extract_client_name(user_message):
    return client_extractor(user_message)