import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NoesisHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith((".py", ".json", ".md", ".txt", ".ipynb")):
            print(f"🌀 Cambio detectado en {event.src_path}")
            subprocess.call(["bash", "upload_to_github.sh"])

if __name__ == "__main__":
    path = "."
    event_handler = NoesisHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("👁️ Noēsis Watcher Activo — Escuchando cambios...")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

