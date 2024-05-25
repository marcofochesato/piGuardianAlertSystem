import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from common_services import get_internal_ip


def send_email(subject, message):
    try:
        # Load email configuration from JSON file
        with open('email_config.json', 'r') as file:
            email_config = json.load(file)

        # Email configuration
        sender_name = email_config['sender_name']
        sender_email = email_config['sender_email']
        sender_password = email_config['sender_password']
        smtp_server = email_config['smtp_server']
        smtp_port = email_config['smtp_port']
        recipients = email_config['recipients']

        # Get the internal IP address
        internal_ip = get_internal_ip()

        if internal_ip:
            # Message about reaching an internal web server
            web_server_message = f"You can reach an internal web server (if activated) at http://{internal_ip}:8000"

            # Append internal IP and web server message to the message
            message += f"\n\nInternal IP Address: {internal_ip}\n{web_server_message}"

        # Create the email content
        email_message = MIMEMultipart()
        email_message['From'] = f"{sender_name} <{sender_email}>"
        email_message['To'] = ', '.join(recipients)
        email_message['Subject'] = subject

        # Attach the message to the email
        email_message.attach(MIMEText(message, 'plain'))

        # Setup the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, email_message.as_string())

        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
