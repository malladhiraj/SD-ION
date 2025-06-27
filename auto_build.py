import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

CSV_FILE = "MasterTemplate.csv"  # Change to your CSV filename if needed
JINJA_FILE = "MasterTemplate.jinja"  # Change to your Jinja filename if needed
BUILD_CMD = ["python", "build.py", "-C", CSV_FILE, "-J", JINJA_FILE]

class CSVChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(CSV_FILE):
            print(f"{CSV_FILE} changed, running build...")
            subprocess.run(BUILD_CMD)

if __name__ == "__main__":
    event_handler = CSVChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    print(f"Watching {CSV_FILE} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
