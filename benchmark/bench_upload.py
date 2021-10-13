import os.path
import shutil

from pydf import PyDF
from utils import bench


def bench_upload():
    if os.path.exists("store"):
        shutil.rmtree("store")
    p = PyDF("store")
    l = ["assets/1.pdf" for _ in range(20)]
    bench(2, p.upload, "xiaoming", l)
    p.water_mark = False
    bench(2, p.upload, "xiaohong", l)
    shutil.rmtree("store")


if __name__ == '__main__':
    bench_upload()
