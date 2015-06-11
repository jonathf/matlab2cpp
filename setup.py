#!/usr/bin/env python
# encoding: utf8

import platform
import os

system = platform.system()

from distutils.core import setup

setup(
    name='matlab2cpp',
    version='0.2',
    packages=['matlab2cpp', 'matlab2cpp.translations',
              'matlab2cpp.testsuite', 'matlab2cpp.snippets'],
    package_dir={'': 'src'},
    url='http://github.com/jonathf/matlab2cpp',
    license='BSD',
    author="Jonathan Feinberg",
    author_email="jonathan@feinberg.no",
    description='Matlab to C++ converter'
)

if system == "Windows":

    print
    print "Program now runnable through 'mconvert.py'"
    print "To start:"
    print "> python mconvert.py -h"

else:

    mconvert = "cp mconvert.py /usr/local/bin/mconvert"
    print mconvert
    os.system(mconvert)
