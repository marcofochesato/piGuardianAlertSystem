import telepot
from telepot.loop import MessageLoop


class TelegramService:
    def __init__(self, bot_token, chat_ids):
        self.bot = telepot.Bot(bot_token)
        self.chat_ids = chat_ids


def start_telegram_service(bot_token, chat_ids):
    telegram_service = TelegramService(bot_token, chat_ids)

    # Set up the message loop to handle incoming messages
    bot = telepot.Bot(bot_token)
    MessageLoop(bot, lambda msg: None).run_as_thread()

    return telegram_service
