import os
import sys


def add_lib_path():
    upd = os.path.dirname
    lib_path = os.path.join(
        upd(upd(os.path.realpath(__file__))), 'lib', 'python')
    print(lib_path)
    sys.path = [lib_path] + sys.path