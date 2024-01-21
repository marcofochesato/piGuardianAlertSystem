import telepot
from telepot.loop import MessageLoop


class TelegramService:
    def __init__(self, bot_token, chat_ids):
        self.bot = telepot.Bot(bot_token)
        self.chat_ids = chat_ids

    def send_alert(self, message):
        for chat_id in self.chat_ids:
            try:
                self.bot.sendMessage(chat_id, message, parse_mode='Markdown')
                print(f"Telegram alert sent to chat ID {chat_id}")
            except Exception as e:
                print(f"Error sending Telegram alert to chat ID {chat_id}: {e}")


def start_telegram_service(bot_token, chat_ids):
    telegram_service = TelegramService(bot_token, chat_ids)

    # Set up the message loop to handle incoming messages
    bot = telepot.Bot(bot_token)
    MessageLoop(bot, lambda msg: None).run_as_thread()

    return telegram_service
