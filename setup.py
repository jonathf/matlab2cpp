#!/usr/bin/env python
# encoding: utf8


import platform
import os
import sys

system = platform.system()

from distutils.core import setup

setup(
    name='matlab2cpp',
    version='0.3',
    packages=['matlab2cpp', 'matlab2cpp/node', 'matlab2cpp/tree',
        'matlab2cpp/rules', 'matlab2cpp/testsuite', 'matlab2cpp/supplement',
        'matlab2cpp/manual', 'matlab2cpp/configure'],
    # package_dir={'': ''},
    url='http://github.com/jonathf/matlab2cpp',
    license='BSD',
    author="Jonathan Feinberg",
    author_email="jonathan@feinberg.no",
    description='Matlab to C++ converter'
)

"""OPTIONAL this will not add path to environment variable, only make m2cpp script"""
if system == "Windows":
    system_path = sys.executable
    cwdir = os.getcwd()

    new_file = open('m2cpp.bat', 'w')
    command_run = '@echo off\n' + system_path + ' ' + cwdir + os.sep + 'mconvert.py' + ' %*'
    new_file.write(command_run)
    new_file.close()

    #copy m2cpp.bat to sys.executable
    bat_dst = sys.executable
    bat_dst = os.path.dirname(bat_dst)

    from shutil import copy
    copy("m2cpp.bat", bat_dst)

    print 
    print "Program now runnable through 'mconvert.py'"
    print "> m2cpp -h"
    
else:
    mconvert = "cp -v mconvert.py /usr/local/bin/mconvert"
    os.system(mconvert)
    chmod = "chmod 755 /usr/local/bin/mconvert"
    print chmod
    os.system(chmod)

