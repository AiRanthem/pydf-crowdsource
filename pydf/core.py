import os
import shutil
import threading
from typing import List
from queue import Queue

from pydf.pdf import create_watermark, add_watermark
import pydf.log as log


def create_dir(path: str) -> str:
    """
    create a directory
    :param path: directory path
    :return: absolute path of the directory created
    """
    os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)


class PyDF:

    def __init__(self, store_dir: str):
        self.root = store_dir
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

    def upload(self, user: str, pdfs: List[str]) -> bool:
        """
        upload several pdf files
        :param user: the user who uploaded them
        :param pdfs: a list of path to find the files to upload
        :return: success or not
        """
        user_lib = self.get_user_lib(user)

        for pdf in pdfs:
            if not os.path.exists(pdf):
                log.error(f"file {os.path.abspath(pdf)} not exits")
                return False
            shutil.copyfile(pdf, os.path.join(user_lib, pdf))
            self.worklist.put(pdf)
