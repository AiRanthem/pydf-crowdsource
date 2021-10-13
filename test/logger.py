from typing import Any

from pydf.log import DefaultLogger


class TestLogger(DefaultLogger):
    last_info, last_warning, last_error = "", "", ""

    def info(self, msg: Any):
        super().info(msg)
        self.last_info = msg

    def warning(self, msg: Any):
        super().warning(msg)
        self.last_warning = msg

    def error(self, msg: Any):
        super().error(msg)
        self.last_error = msg
