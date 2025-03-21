import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from .telegram_handlers import start, handle_audio

_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Create the Application
_application = ApplicationBuilder().token(_bot_token).build()

def start_telegram_bot():
    # Add handlers
    _application.add_handler(CommandHandler("start", start))
    _application.add_handler(MessageHandler(filters.VOICE, handle_audio))
    
    # Start the bot
    _application.run_polling()
