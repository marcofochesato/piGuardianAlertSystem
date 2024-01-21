import json
from telegram import Bot
from telegram import ParseMode
from datetime import datetime, timedelta


def send_telegram_alert(bot_token, chat_ids, message):
    bot = Bot(token=bot_token)

    for chat_id in chat_ids:
        try:
            bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
            print(f"Telegram alert sent to chat ID {chat_id}")
        except Exception as e:
            print(f"Error sending Telegram alert to chat ID {chat_id}: {e}")


if __name__ == "__main__":
    # Load Telegram configuration from JSON file
    with open('telegram_config.json', 'r') as file:
        telegram_config = json.load(file)

    # Extract Telegram configuration
    bot_token = telegram_config['bot_token']
    chat_ids = telegram_config['chat_ids']

    # Example usage
    alert_message = "This is a test alert."

    send_telegram_alert(bot_token, chat_ids, alert_message)
