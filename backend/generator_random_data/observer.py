from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


class Handler(FileSystemEventHandler):
    # def on_created(self, event):
    #     print(event)

    def on_deleted(self, event):
        print(event)

    def on_moved(self, event):
        print(event)

    def on_modified(self, event):
        print(event)


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(Handler(), path='./devices/', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
