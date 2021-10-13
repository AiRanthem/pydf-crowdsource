import os.path
import shutil

from pydf import PyDF
from utils import bench


def bench_upload():
    if os.path.exists("store"):
        shutil.rmtree("store")
    p = PyDF("store")
    l = ["assets/1.pdf" for _ in range(50)]
    bench(2, p.async_upload, "xiaoming", l)
    bench(2, p.upload, "xiaohong", l)
    shutil.rmtree("store")


if __name__ == '__main__':
    bench_upload()
