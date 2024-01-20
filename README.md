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
```
- other

## Installation

1. Clone the repository in a Raspberry:

   ```bash
   https://github.com/marcofochesato/piGuardianAlertSystem.git

2. Open crontab

 ```bash
   crontab -e
 ```

3. Add these lines

 ```crontab
   * * * * * cd /home/pi/PiGuardianAlertSystem;python pin_recorder.py
