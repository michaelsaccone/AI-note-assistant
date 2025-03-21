from telegram import Update
from core.database.models import TelegramUser
from core.database import get_db

async def start(update: Update, context):
    user = update.effective_user
    db = next(get_db())
    
    # Check if user already exists
    db_user = db.query(TelegramUser).filter(TelegramUser.telegram_id == user.id).first()
    
    if not db_user:
        # Create new user
        db_user = TelegramUser(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            has_permission=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
    if not db_user.has_permission:
        await update.message.reply_text(
            'Welcome! You have been registered. Please wait for an administrator to grant you access to use the bot.'
        )
    else:
        await update.message.reply_text('Welcome back! Send me an audio message, and I will transcribe it for you!') 