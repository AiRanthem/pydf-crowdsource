import os
import shutil
import sys
import threading
from typing import List
from queue import Queue

import PyPDF2

import pydf.log as log


class PyDF:

    def __init__(self, store_dir: str):
        self.root = os.path.normpath(store_dir)
        self.library = ""
        self.top = ""
        self.worklist = Queue()
        self.worklock = threading.Lock()
        self.init()
        log.info(f"PyDF instance inited. Store path is {self.root}")

    def init(self):
        """
        init file store path
        """
        splited = self.root.split(os.sep) + ["library"]
        path = ""
        for d in splited:
            path = os.path.join(path, d)
            if not os.path.isdir(path):
                raise RuntimeError(f"初始化失败：文件{path}已存在")
            if not os.path.exists(path):
                os.mkdir(path)
        self.root = os.path.abspath(path)
        self.library = os.path.join(self.root, "library")

    def upload(self, user: str, pdfs: List[str]) -> bool:
        """
        upload several pdf files
        :param user: the user who uploaded them
        :param pdfs: a list of path to find the files to upload
        :return: success or not
        """
        user_lib = os.path.join(self.library, user)
        if not os.path.exists(user_lib):
            os.mkdir(user_lib)

        for pdf in pdfs:
            if not os.path.exists(pdf):
                log.error(f"file {os.path.abspath(pdf)} not exits")
                return False
            shutil.copyfile(pdf, os.path.join(user_lib, pdf))
            self.worklist.put(pdf)
