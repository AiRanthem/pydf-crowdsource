import logging
from typing import Any

logging.getLogger().setLevel(logging.INFO)


class Logger:
    def info(self, msg: Any):
        ...

    def warning(self, msg: Any):
        ...

    def error(self, msg: Any):
        ...


class DefaultLogger(Logger):

    def info(self, msg: Any):
        logging.info(msg)

    def warning(self, msg: Any):
        logging.warning(msg)

    def error(self, msg: Any):
        logging.error(msg)


logger = DefaultLogger()


def set_logger(new_logger: Logger):
    global logger
    logger = new_logger


def get_logger() -> Logger:
    global logger
    return logger


def info(msg: Any):
    logger.info(msg)


def warning(msg: Any):
    logger.warning(msg)


def error(msg: Any):
    logger.error(msg)
