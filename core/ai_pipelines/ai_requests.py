from core.ai_pipelines.chains.client_extraction import extraction_chain


def extract_client_name(user_message):
    client_name = extraction_chain.invoke({"user_message": user_message})
    return client_name
