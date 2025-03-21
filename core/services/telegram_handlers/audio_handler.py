import os
import logging
from telegram import Update
from core.ai_pipelines.ai_requests import extract_client_name, organise_note, agent_web_search
from core.ai_pipelines.chains.text_note_organiser import NoteInfo
from core.ai_pipelines.chains.speech_recognition import transcribe_audio
from core.services.notion_search import get_notion_search_service
from core.services.notion_search_service import add_note_block

logger = logging.getLogger(__name__)

async def handle_audio(update: Update, context):
    await update.message.reply_text(f"Sto analizzando il tuo audio...")
    # Get the audio file
    audio_file = await update.message.voice.get_file()
    file_path = f"audio_{update.message.from_user.id}.ogg"
    await audio_file.download_to_drive(file_path)

    text = ""
    try:
        text = transcribe_audio(file_path=file_path)
        await update.message.reply_text(f"Ho trascritto: {text}")
        logger.info(f"Transcribed text from audio message: {text}")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Sorry, I could not understand the audio.")
        return

    try:
        await handle_client_note_notion(text, update)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Sorry, I could not process the note.")
        return

    # Clean up files
    os.remove(file_path)

async def handle_client_note_notion(text, update: Update):
    client_name = extract_client_name(text)
    await update.message.reply_text(f"Sto cercando il cliente '{client_name}' su Notion...")
    notion_results = get_notion_search_service().search_similar_texts(client_name, limit=1)
    
    if len(notion_results) == 0:
        await update.message.reply_text(f"Non ho trovato nessun cliente con questo nome.")
        logger.warning(f"No client found with name: {client_name}")
    elif len(notion_results) == 1:
        client_found = notion_results[0]
        logger.info(f"Cliente trovato: {client_found.name}")
        await update.message.reply_text(f"Ho trovato un cliente di nome '{client_found.name}'. Sto organizzando la nota...")
        
        organised_note: NoteInfo = organise_note(text)
        await add_note_block(client_found.page_id, organised_note)
        
        notion_link = f"https://www.notion.so/{client_found.page_id}"
        await update.message.reply_text(f"Ho aggiunto la nota organizzata nella pagina del cliente su Notion\n\n{notion_link}")
