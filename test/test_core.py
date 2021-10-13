import os.path
import shutil
import unittest

from pydf import PyDF
from pydf.log import set_logger, get_logger
from logger import TestLogger


class TestCore(unittest.TestCase):
    def setUp(self) -> None:
        set_logger(TestLogger())

    def test_create(self):
        logger = get_logger()
        abspath = os.path.abspath("a/b/c/d/e")
        libpath = os.path.join(abspath, "library")
        if os.path.exists(libpath):
            shutil.rmtree("a")
        p1 = PyDF("a/b/c/d/e")
        self.assertTrue(os.path.exists(libpath))
        self.assertTrue(logger.last_info.endswith(abspath))
        p2 = PyDF("a/b/c/d/e")
        self.assertTrue(logger.last_info.endswith(abspath))
        shutil.rmtree("a")


if __name__ == '__main__':
    unittest.main()
