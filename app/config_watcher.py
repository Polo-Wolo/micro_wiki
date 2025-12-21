import time
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .config import reload_config, CONFIG_PATH

CONFIG_FILE = CONFIG_PATH.resolve()


class ConfigHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_reload = 0

    def _handle(self, event):
        if event.is_directory:
            return

        try:
            path = Path(event.src_path).resolve()
        except FileNotFoundError:
            return

        if path != CONFIG_FILE:
            return

        now = time.time()
        if now - self.last_reload < 0.5:
            return

        reload_config()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] [HOT RLD] [CONFIG] config.yml rechargé")

        self.last_reload = now

    def on_modified(self, event):
        self._handle(event)

    def on_created(self, event):
        self._handle(event)

    def on_moved(self, event):
        self._handle(event)


# ----------------------------
# Fonction au niveau module
# ----------------------------
def start_config_watcher():
    observer = Observer()
    observer.schedule(
        ConfigHandler(),
        CONFIG_PATH.parent, # type: ignore
        recursive=False
    )
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
