import sys
from cx_Freeze import setup, Executable
import os
import shutil
from distutils.dir_util import copy_tree

def abs_path_maker(path):
    return os.path.join(os.getcwd(), path)

if os.path.exists(abs_path_maker("build")):
    print("deleting old builds...", end="")
    shutil.rmtree(abs_path_maker("build"))
    print("done")

if sys.platform == 'win32':
    base = 'Win32GUI'

if sys.platform == "win32" : base = "Win32GUI"

exe = Executable(script = "main.py", base= base)

setup(name = "photo_slider",
version = '0.1', 
description = 'photo slider',
options={"build_exe":{"includes": [], "excludes":["PyQt4", "PyQt5", "scipy", "numpy", "tkinter", "win32com", "distutils"], "packages":[]}},
executables = [exe])

shutil.copytree(abs_path_maker("files"), abs_path_maker("build\\exe.win-amd64-3.8\\files"))

pygame_example_path = abs_path_maker("build\\exe.win-amd64-3.8\\lib\\pygame\\examples")
print("deleting" + pygame_example_path + "...", end="")
shutil.rmtree(pygame_example_path)
print("done")

copy_from = abs_path_maker("build\\exe.win-amd64-3.8")
copy_to = abs_path_maker("build")
print("copying" + copy_from + " -> " + copy_to)
copy_tree(copy_from, copy_to)

shutil.rmtree(abs_path_maker("build\\exe.win-amd64-3.8"))

print("build complete")