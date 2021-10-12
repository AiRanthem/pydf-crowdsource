import logging
from typing import Any

logging.getLogger().setLevel(logging.INFO)


def info(msg: Any):
    logging.info(msg)


def warning(msg: Any):
    logging.warning(msg)


def error(msg: Any):
    logging.error(msg)
