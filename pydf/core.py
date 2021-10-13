import os
import shutil
import threading
import asyncio
import time
from typing import List
from queue import Queue

from pydf.pdf import create_watermark, add_watermark, merge
import pydf.log as log


def create_dir(path: str) -> str:
    """
    create a directory
    :param path: directory path
    :return: absolute path of the directory created
    """
    os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)


async def run_all(jobs: list):
    await asyncio.gather(*jobs)


async def store_pdf(in_file: str, user_lib: str, water_mark: bool):
    out_file = os.path.join(user_lib, f"{time.time()}.pdf")
    if water_mark:
        add_watermark(in_file, os.path.join(user_lib, "mark.pdf"), out_file)
    else:
        shutil.copyfile(in_file, out_file)


class PyDF:

    def __init__(self, store_dir: str, with_water_mark: bool = True):
        self.root = store_dir
        self.water_mark = with_water_mark
        self.library = ""
        self.top = ""
        self.worklist = Queue()
        self.worklock = threading.Lock()
        self.init()
        log.info(f"PyDF instance inited. Store path is {self.root}")

    def new_dir(self, path: str):
        """
        create a new directory in root dir
        :param path: directory path
        :return: the absolute path of dir
        """
        return create_dir(os.path.join(self.root, path))

    def get_user_lib(self, user: str):
        """
        create a new lib in library dir
        :param user: username
        :return: the absolute path of dir
        """
        path = create_dir(os.path.join(self.library, user))
        watermark = os.path.join(path, "mark.pdf")
        if not os.path.exists(watermark):
            create_watermark(user, watermark)
        return path

    def init(self):
        """
        init file store path
        """
        self.root = create_dir(self.root)
        self.library = self.new_dir("library")

    def async_upload(self, user: str, pdfs: List[str]) -> bool:
        """
        never use this only when you're running benchmarks.
        :param user: the user who uploaded them
        :param pdfs: a list of path to find the files to upload
        :return: success or not
        """
        user_lib = self.get_user_lib(user)
        store_jobs = []

        for f in pdfs:
            if not os.path.exists(f):
                log.error(f"file {os.path.abspath(f)} not exits")
                return False
            self.worklist.put(f)
            store_jobs.append(store_pdf(f, user_lib, self.water_mark))
        asyncio.run(run_all(store_jobs))
        return True

    def upload(self, user: str, pdfs: List[str]) -> bool:
        """
        upload some pdf files. this sync way is always a little bit faster than the async one
        sync ones is always a little faster
        :param user: the user who uploaded them
        :param pdfs: a list of path to find the files to upload
        :return: success or not
        """
        user_lib = self.get_user_lib(user)
        for f in pdfs:
            if not os.path.exists(f):
                log.error(f"file {os.path.abspath(f)} not exits")
                return False
            self.worklist.put(f)
            out_file = os.path.join(user_lib, f"{time.time()}.pdf")
            if self.water_mark:
                add_watermark(f, os.path.join(user_lib, "mark.pdf"), out_file)
            else:
                shutil.copyfile(f, out_file)
        return True

    def merge_all(self) -> None:
        """
        merge all pdf files in library and store the file in "self.top" attribute.
        take care to use this method because it will take a lot time.
        """
        files = [os.path.join(self.library, user_dir, f)
                 for user_dir in os.listdir(self.library) for f in os.listdir(os.path.join(self.library, user_dir))
                 if f.endswith(".pdf") and not f.startswith("m")]
        try:
            self.top = merge(files, self.root)
            log.info(f"{len(files)} pdf files merged to {self.top}")
        except Exception as e:
            log.error(f"merge_all failed: {e}")
            self.top = ""

    def append_worklist(self) -> None:
        """
        merge all pdf files in worklist, which are unmerged, with the file stored in "self.top", replace "self.top"
        with the new file. the old file will not be kept.
        """
        if self.top == "":
            return self.merge_all()
