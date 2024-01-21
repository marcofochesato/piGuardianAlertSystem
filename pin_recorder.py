import RPi.GPIO as GPIO
import json
import sqlite3
from datetime import datetime, timedelta
import time



def setup_database():
    # Connect to SQLite database
    conn = sqlite3.connect('pin_records.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pin_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pin_number INTEGER,
            pin_description TEXT,
            pin_state INTEGER,
            sent_alert_by_email_at TEXT,
            sent_alert_by_telegram_at TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()

    return conn, cursor


def read_pin_state(pin, cursor):
    # print(pin['pin_number'])
    # GPIO.setup(pin['pin_number'], GPIO.IN)
    GPIO.setup(pin['pin_number'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pin_state = GPIO.input(pin['pin_number'])

    # Fetch the most recent state from the database
    cursor.execute('''
        SELECT pin_state
        FROM pin_records
        WHERE pin_number = ?
        ORDER BY created_at DESC
        LIMIT 1
    ''', (pin['pin_number'],))
    previous_state = cursor.fetchone()

    return pin_state, previous_state


def insert_record(pin, pin_state, timestamp, cursor, conn):
    cursor.execute('''
        INSERT INTO pin_records (pin_number, pin_description, pin_state, created_at)
        VALUES (?, ?, ?, ?)
    ''', (pin['pin_number'], pin['description'], pin_state, timestamp))
    conn.commit()

    # print(
    #     f"Inserted record: Pin {pin['pin_number']}, Description: {pin['description']}, State: {pin_state}, Created At: {timestamp}")


def delete_old_records(cursor, conn):
    # Calculate the date 30 days ago
    thirty_days_ago = datetime.now() - timedelta(days=30)

    # Delete records older than 30 days
    cursor.execute('''
        DELETE FROM pin_records
        WHERE created_at < ?
    ''', (thirty_days_ago.strftime('%Y-%m-%d %H:%M:%S'),))
    conn.commit()


# Open the configuration file
with open('pins.json', 'r') as file:
    pins_data = json.load(file)

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)

conn, cursor = setup_database()

try:
    while True:
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Delete old records
        delete_old_records(cursor, conn)

        # Iterate through pins
        for pin in pins_data:
            pin_state, previous_state = read_pin_state(pin, cursor)
            time.sleep(0.1)
            # print(pin_state, previous_state)

            # If there's no previous state or it's different, insert a new record
            if not previous_state or previous_state[0] != pin_state:
                insert_record(pin, pin_state, timestamp, cursor, conn)

        # Wait for one second
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    conn.close()
