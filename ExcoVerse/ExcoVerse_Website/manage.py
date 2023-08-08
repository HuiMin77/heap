#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
import subprocess
import psutil
import time

def start_telegram_bot():
    for process in psutil.process_iter(['pid', 'name']):
        
        if 'python' in process.info['name'] and 'bot_form.py' in ' '.join(process.cmdline()):
            print("Telegram bot is already running.")
            return
    
    # If the bot is not running, start it
    print("Starting Telegram bot...")
    # Replace "path/to/your/bot_script.py" with the actual path to your Telegram bot script (main.py)
    subprocess.Popen(["python", "Payment/bot_form.py"])
    time.sleep(3)  # Wait for the bot to start
    print("Telegram bot started.")
    
def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ExcoVerse_Website.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    start_telegram_bot()
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
