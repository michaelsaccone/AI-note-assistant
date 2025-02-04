import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import speech_recognition as sr
from pydub import AudioSegment
import torch
from transformers import pipeline
from datasets import load_dataset
from notion_client import Client as NotionClient

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram bot token
TELEGRAM_BOT_TOKEN = '7767406326:AAFUFVyD1NkIoNAj7GhFdhkuogzBPvOFe4Y'



pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def transcribe_audio(file_path):
    """ uses the ..."""
    result = pipe(file_path)
    return result["text"]


async def start(update: Update, context):
    await update.message.reply_text('Send me an audio message, and I will transcribe it for you!')

async def handle_audio(update: Update, context):
    # Get the audio file
    audio_file = await update.message.voice.get_file()
    file_path = f"audio_{update.message.from_user.id}.ogg"
    await audio_file.download_to_drive(file_path)

    try:
        text = transcribe_audio(file_path=file_path)
        await update.message.reply_text(f"Transcribed text: {text}")
    except Exception:
        await update.message.reply_text("Sorry, I could not understand the audio.")
    



    # # Convert .ogg to .wav
    # audio = AudioSegment.from_file(file_path)
    # wav_path = f"audio_{update.message.from_user.id}.wav"
    # audio.export(wav_path, format="wav")

    # # Transcribe the audio
    # recognizer = sr.Recognizer()
    # with sr.AudioFile(wav_path) as source:
    #     audio_data = recognizer.record(source)
    #     try:
    #         text = recognizer.recognize_google(audio_data)
    #         await update.message.reply_text(f"Transcribed text: {text}")
    #     except sr.UnknownValueError:
    #         await update.message.reply_text("Sorry, I could not understand the audio.")
    #     except sr.RequestError as e:
    #         await update.message.reply_text(f"Could not request results from Google Speech Recognition service; {e}")

    # Clean up files
    os.remove(file_path)
    # os.remove(wav_path)


# Example usage
notion_api_key = "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"
database_id = "b8ea6e1af2d840ad80ff175885038c40"

def search_notion_database(query, notion_api_key, database_id):
    """
    Searches a Notion database using the official Notion Python client and returns the best matching item.

    :param query: The search string.
    :param notion_api_key: Your Notion API key.
    :param database_id: The ID of the Notion database to search.
    :return: The best matching item from the database, or None if no match is found.
    """
    # Initialize the Notion client
    notion = NotionClient(auth=notion_api_key)

    try:
        # Query the database
        response = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "Name",  # Replace "Name" with the property you want to search
                "title": {
                    "contains": query
                }
            }
        )

        results = response.get("results", [])

        if not results:
            print("No results found.")
            return None

        # For simplicity, return the first result as the best match
        best_match = results[0]
        return best_match

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def main():
    # Create the Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, handle_audio))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()