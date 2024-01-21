import json
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


def handle(msg):
    content_type, _, _ = telepot.glance(msg)

    if content_type == 'text':
        # Respond to a text message
        print(f"Received text message: {msg['text']}")


if __name__ == "__main__":
    # Load Telegram configuration from JSON file
    with open('telegram_config.json', 'r') as file:
        telegram_config = json.load(file)

    # Extract Telegram configuration
    bot_token = telegram_config['bot_token']
    chat_ids = telegram_config['chat_ids']

    # Create TelegramService instance
    telegram_service = TelegramService(bot_token, chat_ids)

    # Set up the message loop to handle incoming messages
    bot = telepot.Bot(bot_token)
    MessageLoop(bot, handle).run_as_thread()

    # Example usage
    alert_message = "This is a test alert."
    telegram_service.send_alert(alert_message)

    # Keep the program running
    while True:
        pass
