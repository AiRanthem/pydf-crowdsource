import os
import shutil

from pydf import PyDF


def bench_merge_all():
    if os.path.exists("store"):
        shutil.rmtree("store")
    p = PyDF("store", False)
    files = ["assets/1.pdf" for _ in range(200)]
    p.upload("xiaoming", files)


if __name__ == '__main__':
    bench_merge_all()
