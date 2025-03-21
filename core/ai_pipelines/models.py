import os

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

def get_llm_model(model_name):
    if 'gpt' in model_name:
        model = ChatOpenAI(model=model_name, temperature=0.4)
    else:
        model = ChatOllama(model=model_name, temperature=0.4)
    return model

# client_extractor_llm = get_llm_model(os.environ['CLIENT_EXTRACTOR_MODEL_NAME'])
reasoner_llm = get_llm_model(os.environ['REASONER_MODEL_NAME'])
tool_caller_llm = get_llm_model(os.environ['TOOL_CALLER_MODEL_NAME'])
writer_llm = get_llm_model(os.environ['WRITER_MODEL_NAME'])