#!/usr/bin/env python

import platform
#  import sys
import os

system = platform.system()

#  path = os.path.abspath(sys.argv[0])
#  dirname = os.path.dirname(path)
#  os.chdir(dirname)

#  args = " ".join(sys.argv[1:])

from distutils.core import setup

setup(
    name='matlab2cpp',
    version='0.2',
    packages=['matlab2cpp', 'matlab2cpp.targets',
              'matlab2cpp.testsuite', 'matlab2cpp.snippets'],
    package_dir={'': 'src'},
    url='http://github.com/jonathf/matlab2cpp',
    license='BSD',
    author="Jonathan Feinberg",
    author_email="jonathan@feinberg.no",
    description='Matlab to C++ converter'
)

if system == "Windows":

#      os.system("python.exe setup_antlr.py " + args)
#      os.system("python.exe setup_matlab2cpp.py " + args)

    print
    print "Program now runnable through 'mconvert.py'"
    print "To start:"
    print "> python mconvert.py -h"

else:

#      os.system("python setup_antlr.py "+args)
#      os.system("python setup_matlab2cpp.py " + args)

    mconvert = "cp mconvert.py /usr/local/bin/mconvert"
    print mconvert
    os.system(mconvert)
