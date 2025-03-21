from telegram import Update

async def start(update: Update, context):
    await update.message.reply_text('Send me an audio message, and I will transcribe it for you!') 