# WATCHER: Monitores /scheme folders and call theme_compiler.py when changes are detected
import time
import os
import glob
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the default theme directory relative to the location of this Python file
DIRECTORY_TO_WATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../theme')

# Use glob to find all subdirectories matching the pattern
FOLDERS_TO_WATCH = glob.glob(os.path.join(DIRECTORY_TO_WATCH, '**/scheme'), recursive=True)

class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        for folder in FOLDERS_TO_WATCH:
            self.observer.schedule(event_handler, folder, recursive=True)
        try:
            self.observer.start()
            print(f"Watching for changes to scheme folders")
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            # print("Observer stopped due to keyboard interrupt.")
        except Exception as e:
            self.observer.stop()
            print(f"Observer stopped due to an error: {e}")
        finally:
            self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            print(f"🆕 Created: {event.src_path}")
            subprocess.run(["python3", DIRECTORY_TO_WATCH+"/../tools/aurify.py"])
        elif event.event_type == 'modified':
            print(f"🚧 Modified: {event.src_path}")
            subprocess.run(["python3", DIRECTORY_TO_WATCH+"/../tools/aurify.py"])
        elif event.event_type == 'deleted':
            print(f"❌ Deleted: {event.src_path}")
            subprocess.run(["python3", DIRECTORY_TO_WATCH+"/../tools/aurify.py"])
if __name__ == '__main__':
    w = Watcher()
    w.run()