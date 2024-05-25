import json

from email_sender import send_email


def send_online_check_email():
    email_subject = f"piGuardianAlertSystem"
    email_message = f"I'm online."

    send_email(email_subject, email_message)


if __name__ == "__main__":
    with open('email_config.json', 'r') as file:
        email_config = json.load(file)

    try:
        send_online_check_email()

    except Exception as e:
        print(f"Error: {e}")
