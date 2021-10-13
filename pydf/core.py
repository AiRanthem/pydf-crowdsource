import asyncio
import os
import random
import shutil
import threading
import time
from typing import List

import pydf.log as log
from pydf.config import Config
from pydf.pdf import create_watermark, add_watermark, merge


def create_dir(path: str) -> str:
    """
    create a directory
    :param path: directory path
    :return: absolute path of the directory created
    """
    os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)


class PyDF:

    def __init__(self, config: Config = None):
        self.root = config.store_dir
        self.with_watermark = config.with_watermark
        self.config = config
        self.library = ""
        self.top = ""
        self.worklist = []
        self.worklock = threading.Lock()

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
            with self.worklock:
                self.worklist.append(f)
            out_file = os.path.join(user_lib, f"{time.time()}_{random.randrange(1, 1000)}.pdf")
            if self.with_watermark:
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

    def append_worklist(self) -> None:
        """
        merge all pdf files in worklist, which are unmerged, with the file stored in "self.top", replace "self.top"
        with the new file. the old file will not be kept.
        """
        if self.top == "":
            return self.merge_all()  # todo

    def collect(self):
        """
        collect everything in "self.worklist"
        """
        with self.worklock:
            files = self.worklist + [self.top] if self.top != "" else self.worklist
            self.worklist = []
        try:
            self.top = merge(files, self.root)
            log.info(f"{len(files)} pdf files merged to {self.top}")
        except Exception as e:
            log.error(f"collect failed: {e}")

    def download(self):
        return self.top
