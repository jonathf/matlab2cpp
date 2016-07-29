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
"""
if system == "Windows":
    system_path = sys.executable
    cwdir = os.getcwd()

    new_file = open('m2cpp.bat', 'w')
    command_run = '@echo off\n' + system_path + ' ' + cwdir + os.sep + 'mconvert.py' + ' %*'
    new_file.write(command_run)
    new_file.close()

    print 
    print "Program now runnable through 'mconvert.py'"
    print "> m2cpp -h"
"""


"""This will add path to environment variable, but it need to be update by closing and reopening cmd"""
if system == "Windows":
    system_path = sys.executable
    cwdir = os.getcwd()
    newdir = os.getcwd() + os.sep + "Windows"
    env_path = os.getenv("path")

    if not os.path.exists(newdir):
        os.makedirs(newdir)

    if not newdir in env_path:
        add_env = "adding to environment path: " + newdir
        print add_env

        install_file = open('Windows\install.bat', 'w')
        command_install = """powershell -Command "& {$new_entry = '""" + newdir + """';$old_path = [Environment]::GetEnvironmentVariable('path', 'user');$new_path = $old_path + ';' + $new_entry;[Environment]::SetEnvironmentVariable('path', $new_path,'User');}"""
        #command_temp = "SET PATH=%PATH%;" + newdir
        install_file.write(command_install)
        install_file.close()

        new_file = open('Windows\m2cpp.bat', 'w')
        command_run = '@echo off\n' + system_path + ' ' + cwdir + os.sep + 'mconvert.py' + ' %*'
        new_file.write(command_run)
        new_file.close()

        import subprocess
        env_path = newdir + os.sep + 'install.bat'
        p = subprocess.Popen(env_path, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print
        print "Restart command prompt"

    print "Program now runnable through 'mconvert.py'"
    print "> m2cpp -h"
else:
    mconvert = "cp -v mconvert.py /usr/local/bin/mconvert"
    os.system(mconvert)
    chmod = "chmod 755 /usr/local/bin/mconvert"
    print chmod
    os.system(chmod)
