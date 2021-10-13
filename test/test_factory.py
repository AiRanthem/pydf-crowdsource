import os.path
import shutil
import unittest

from pydf import PyDF
from pydf.config import Config
from pydf.factory import PyDFactory
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
        config = Config(store_dir="a/b/c/d/e", with_watermark=False)
        factory = PyDFactory(config)
        p1 = factory.get(False)
        self.assertTrue(os.path.exists(libpath))
        self.assertTrue(logger.last_info.endswith(abspath))
        p2 = factory.get(False)
        self.assertTrue(logger.last_info.endswith(abspath))
        shutil.rmtree("a")


if __name__ == '__main__':
    unittest.main()
