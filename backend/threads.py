import os
import threading
import time
from queue import Queue

seen = []

queue = Queue()


def scan_fs(path: str):
    path = os.path.abspath(path)
    while True:
        files = os.listdir(path)
        for file in files:
            if file not in seen:
                seen.append(file)
                queue.put(file)
        time.sleep(2)


def print_fs():
    while True:
        get = queue.get()
        print(f"get {get}")


if __name__ == '__main__':
    s = threading.Thread(target=scan_fs, args=("../spec/threads",))
    p = threading.Thread(target=print_fs)
    s.start()
    p.start()
    s.join()
