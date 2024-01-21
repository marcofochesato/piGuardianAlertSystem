# check_and_send_telegram.py
import json
import sqlite3
from datetime import datetime, timedelta
from telegram_sender import start_telegram_service
from common_services import get_internal_ip


def check_and_send_telegram(cursor, conn):
    # Fetch record that needs Telegram alerts
    cursor.execute('''
        SELECT id, pin_number, pin_description, pin_state, created_at
        FROM pin_records
        WHERE sent_alert_by_telegram_at IS NULL
        ORDER BY created_at ASC
        LIMIT 1
    ''')
    record = cursor.fetchone()

    if record:
        # Extract record information
        record_id, pin_number, pin_description, pin_state, created_at = record

        # Get the internal IP address
        internal_ip = get_internal_ip()

        telegram_message = (
            f"Alert: Pin {pin_number} State Change\n"
            f"Pin {pin_number} ({pin_description}) changed state to {pin_state} at {created_at}.\n"
            f"You can reach an internal web server at {internal_ip}:8000."
        )

        # Load Telegram configuration from JSON file
        with open('telegram_config.json', 'r') as file:
            telegram_config = json.load(file)

        # Create and start TelegramService instance
        telegram_service = start_telegram_service(telegram_config['bot_token'], telegram_config['chat_ids'])

        # Attempt to send Telegram alert
        telegram_service.send_alert(telegram_message)

        # Update the record with the Telegram sent timestamp
        cursor.execute('''
            UPDATE pin_records
            SET sent_alert_by_telegram_at = ?
            WHERE id = ?
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), record_id))
        conn.commit()

        print(f"Telegram alert sent for record ID {record_id}.")
    else:
        print("No records found for Telegram alert.")


if __name__ == "__main__":
    # Connect to SQLite database
    conn = sqlite3.connect('pin_records.db')
    cursor = conn.cursor()

    try:
        # Check and send Telegram alerts
        check_and_send_telegram(cursor, conn)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close database connection
        conn.close()
