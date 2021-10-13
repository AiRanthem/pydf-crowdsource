from pydf import PyDF, log
from pydf.config import Config


class PyDFactory:
    def __init__(self, config: Config):
        self.config = config

    def get(self, merge_all: bool = True):
        instance = PyDF(self.config)
        instance.init()
        log.info(f"PyDF instance inited. Store path is {instance.root}")
        if merge_all:
            instance.merge_all()
        return instance

