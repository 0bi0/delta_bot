import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

BOT_SCRIPT = "your_bot_file.py"  # Replace with your actual bot filename

class SettingsChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("settings.json"):
            print("[WATCHDOG] Detected settings.json change.")
            restart_bot()

process = None

def start_bot():
    global process
    print("[WATCHDOG] Starting bot...")
    process = subprocess.Popen(["python", BOT_SCRIPT])

def restart_bot():
    global process
    if process:
        print("[WATCHDOG] Restarting bot...")
        process.terminate()
        process.wait()
    start_bot()

if __name__ == "__main__":
    observer = Observer()
    event_handler = SettingsChangeHandler()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        start_bot()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
