# GPIO Pin State Monitoring and Logging

This Python scripts are designed to monitor the state of GPIO pins on a Raspberry Pi and:
- Log changes to a SQLite database
- Show changes in a simple web server listening on port 8000
- send email alert
- send text message alert via Telegram Bot


## Prerequisites

- Raspberry Pi with GPIO pins
- Python 3 installed on the Raspberry Pi
- email_config.json file containing email configurations:
    ```json
    [
    {"pin_number": 24, "description": "BRUCIATORE"},
    {"pin_number": 23, "description": "CALDAIA"}
   ]

- email_config.json file containing email configurations:
    ```json
    {
  "sender_email": "your_email@example.com",
  "sender_password": "your_email_password",
  "smtp_server": "smtp.your_email_provider.com",
  "smtp_port": 587,
  "recipients": ["recipient1@example.com", "recipient2@example.com"]
  }
  
- telegram_config.json file containing telegram configurations (assuming you are able to create a TelegramBot):
    ```json
    {
  "bot_token": "your_telegram_bot_token",
  "chat_ids": [123456789, 987654321]
  }


## Installation

1. **Clone the repository on your Raspberry Pi:**

    ```bash
    git clone https://github.com/marcofochesato/piGuardianAlertSystem.git
    ```


2. **Start services on boot:**

   There are many ways to start scripts at boot.

   * Open the autostart file for editing:

      ```bash
      sudo nano /etc/xdg/lxsession/LXDE-pi/autostart 
      ```
      
      - Add the following lines:
      
      ```bash
      @xset s off
      @xset -dpms
      @xset s noblank
      @cd /home/pi/piGuardianAlertSystem;python pin_recorder.py
      @cd /home/pi/piGuardianAlertSystem;python web-server.py
       ```
   
   * Open /etc/profile

        ```bash
        sudo nano /etc/profile
        ```
      
        - Add the following lines:
      
        ```bash
        cd /home/pi/piGuardianAlertSystem
        python pin_recorder.py &
        nohup python web-server.py > web-server.log 2>&1 &

3. **Send alert via email:**

   Open the crontab file for editing:

    ```bash
    crontab -e
   ```

    Add the following lines:
      
    ```
   cd /home/pi/piGuardianAlertSystem;python email_alerter.py
   cd /home/pi/piGuardianAlertSystem;python telegram_alerter.py


