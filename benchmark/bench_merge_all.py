import os
import shutil

from pydf import PyDF
from utils import bench


def bench_merge_all():
    if os.path.exists("store"):
        shutil.rmtree("store")
    p = PyDF("store", False)
    files = ["assets/1.pdf" for _ in range(200)]
    p.upload("xiaoming", files)
    bench(3, p.merge_all)
    shutil.rmtree("store")


if __name__ == '__main__':
    bench_merge_all()
