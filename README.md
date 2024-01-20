# GPIO Pin State Monitoring and Logging

This Python scripts are designed to monitor the state of GPIO pins on a Raspberry Pi and:
- Log changes to a SQLite database
- Show changes in a simple web server listening on port 8000


## Prerequisites

- Raspberry Pi with GPIO pins
- Python 3 installed on the Raspberry Pi
- pins.json file containing pin configurations:
    ```json
    [
    {"pin_number": 24, "description": "BRUCIATORE"},
    {"pin_number": 23, "description": "CALDAIA"}
   ]

- other

## Installation

1. **Clone the repository on your Raspberry Pi:**

    ```bash
    git clone https://github.com/marcofochesato/piGuardianAlertSystem.git
    ```


3. **Start services on boot:**

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
      @cd /home/pi/piGuardianAlertSystem;python3 pin_recorder.py
      @cd /home/pi/piGuardianAlertSystem;python3 web-server.py
       ```
   
   * Open /etc/profile

        ```bash
        sudo nano /etc/profile
        ```
      
        - Add the following lines:
      
        ```bash
        cd /home/pi/piGuardianAlertSystem
        python3 pin_recorder.py &
        nohup python3 web-server.py > web-server.log 2>&1 &
