#!/usr/bin/env python

import platform
import sys
import os

system = platform.system()

path = os.path.abspath(sys.argv[0])
dirname = os.path.dirname(path)
os.chdir(dirname)

args = " ".join(sys.argv[1:])

if system == "Windows":

    os.system("python.exe setup_antlr.py " + args)
    os.system("python.exe setup_matlab2cpp.py " + args)

else:

    os.system("python setup_antlr.py "+args)
    os.system("python setup_matlab2cpp.py " + args)

    mconvert = "cp mconvert /usr/local/bin"
    print mconvert
    os.system(mconvert)
