import logging
from core.startup import initialize_services
from core.services.telegram_bot_service import start_telegram_bot

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting AI assistant...")
    initialize_services()
    logger.info("Services initialized")

    start_telegram_bot()


if __name__ == '__main__':
    main()