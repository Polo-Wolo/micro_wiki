import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .indexer import load_pages
from .config import get_config

CONFIG = get_config()
NOTES_DIR = str(CONFIG["paths"]["notes"])

class NotesHandler(FileSystemEventHandler):
    def __init__(self, pages_ref):
        self.pages_ref = pages_ref
        self.last_reload = 0

    def on_modified(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(".md"): # type: ignore
            return

        now = time.time()
        if now - self.last_reload < 0.5:
            return

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] [HOT RLD] [NOTES] notes modifiées")

        self.pages_ref.clear()
        self.pages_ref.update(load_pages())
        self.last_reload = now

def start_watcher(pages_ref):
    observer = Observer()
    observer.schedule(NotesHandler(pages_ref), NOTES_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
