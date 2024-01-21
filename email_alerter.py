import json
import sqlite3
from email_sender import send_email
from datetime import datetime, timedelta


def check_and_send_email(cursor, conn):
    # Fetch record that need email alerts
    cursor.execute('''
        SELECT id, pin_number, pin_description, pin_state, created_at
        FROM pin_records
        WHERE sent_alert_by_email_at IS NULL
        ORDER BY created_at ASC
        LIMIT 1
    ''')
    record = cursor.fetchone()

    if record:
        # Extract record information
        record_id, pin_number, pin_description, pin_state, created_at = record

        # Example email content
        email_subject = f"Alert: Pin {pin_number} State Change"
        email_message = f"Pin {pin_number} ({pin_description}) changed state to {pin_state} at {created_at}."

        # Attempt to send email
        success = send_email(email_subject, email_message)

        if success:
            # Update the record with the email sent timestamp
            cursor.execute('''
                UPDATE pin_records
                SET sent_alert_by_email_at = ?
                WHERE id = ?
            ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), record_id))
            conn.commit()

            print(f"Email alert sent for record ID {record_id}.")
        else:
            print(f"Failed to send email alert for record ID {record_id}.")


if __name__ == "__main__":
    # Load email configuration from JSON file
    with open('email_config.json', 'r') as file:
        email_config = json.load(file)

    # Connect to SQLite database
    conn = sqlite3.connect('pin_records.db')
    cursor = conn.cursor()

    try:
        # Check and send email alerts
        check_and_send_email(cursor, conn)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close database connection
        conn.close()
