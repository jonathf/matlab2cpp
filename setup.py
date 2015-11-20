#!/usr/bin/env python
# encoding: utf8

import platform
import os

system = platform.system()

from distutils.core import setup

setup(
    name='matlab2cpp',
    version='0.3',
    packages=['matlab2cpp', 'matlab2cpp/node', 'matlab2cpp/tree',
        'matlab2cpp/rules', 'matlab2cpp/testsuite', 'matlab2cpp/supplement',
        'matlab2cpp/manual'],
    # package_dir={'': ''},
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

    mconvert = "cp -v mconvert.py /usr/local/bin/mconvert"
    os.system(mconvert)
    chmod = "chmod 755 /usr/local/bin/mconvert"
    print chmod
    os.system(chmod)
