# from browser_use.agent.service import Agent
# from langchain_openai import ChatOpenAI
from datetime import datetime, timedelta

from core.ai_pipelines.chains.client_extraction import oracle
from core.ai_pipelines.chains.text_note_organiser import note_organiser_chain, NoteInfo


def extract_client_name(user_message):
    # client_name = extraction_chain.invoke({"user_message": user_message})
    client_res = oracle(question="Qual è il nome dell'azienda/cliente?", context=user_message)

    client_name = client_res["answer"].strip(",.!? \n'\"")
    return client_name

async def agent_web_search(user_message):
    print("Not implemented yet")
    # agent = Agent(
    #     task=user_message,
    #     llm=ChatOpenAI(model="gpt-4o"),
    # )
    # return await agent.run()

def organise_note(note):
    note: NoteInfo = note_organiser_chain.invoke({
        "user_note": note
    })

    if note.date == 'today':
        note.date = datetime.now().strftime("%Y-%m-%d")
    elif note.date == 'yesterday':
        note.date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    return note
