from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import json

SETTINGS_FILE = "settings.json"

class SettingsHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if event.src_path.endswith(SETTINGS_FILE):
            print("🔄 settings.json modified! Reloading...")
            self.callback()

def start_settings_watcher(callback):
    event_handler = SettingsHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    print("👀 Watching settings.json for changes...")
    return observer