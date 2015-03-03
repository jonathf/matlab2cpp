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

    print
    print "Program now runnable through 'mconvert.py'"
    print "To start:"
    print "> python mconvert.py -h"

else:

    os.system("python setup_antlr.py "+args)
    os.system("python setup_matlab2cpp.py " + args)

    mconvert = "cp mconvert.py /usr/local/bin/mconvert"
    print mconvert
    os.system(mconvert)
