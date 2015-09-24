#!/usr/bin/env python
# encoding: utf-8

"""
The simplest way to interact with the `Matlab2cpp`-toolbox is to use the
`mconvert` frontend.  The script automatically creates files with various
extensions containing translations and/or meta-information.
Even though `mconvert` is sufficient for performing all code translation, many
of the examples in this manual are done through a python interface, since some
of the python functionallity also will be discussed.  Given that `Matlab2cpp` is
properly installed on your system, the python library is available in Python's
path.  For the examples, the module is assumed imported as

    >>> import matlab2cpp as mc

The simplest way to use the library is to use the quick translation functions.
They are as follows:

=========   =================================================================
Function    Description
=========   =================================================================
`mc.qcpp`   Quick code translation of scripts into runnable C++ code content.
`mc.qhpp`   Quick code translation of matlab module files into C++ header
            content, or header files for runnable scripts.
`mc.qpy`    Quick extraction of variable and header meta information and
            creation of suppliment file content.
`mc.qlog`   Quick creation of error log.
=========   =================================================================

Each function can take a string as input and output.  However, for more advanced
usage, see their respective documentaions. For most intents and puposes,
`mconvert` creates files with the same content as these quick functions creates.
"""

import supplement
import utils
import collection

import time
from datetime import datetime as date
import os
from os.path import sep
import imp

from treebuilder import Treebuilder
from supplement import set_variables, get_variables, str_variables
from utils import translate, build, qcpp, qpy, qhpp, qlog, qtree


def main(args):

    builder = Treebuilder(disp=args.disp, comments=args.comments)

    paths = [os.path.abspath(os.path.dirname(args.filename))]

    if args.disp:
        print "building tree..."

    filenames = [os.path.abspath(args.filename)]
    stack = []
    while filenames:

        filename = filenames.pop(0)
        assert os.path.isfile(filename)

        if filename in stack:
            continue

        if args.disp:
            print "loading", filename

        stack.append(filename)

        f = open(filename, "rU")
        code = f.read()
        f.close()

        program = builder.load(filename, code)

        unknowns = builder.get_unknowns(filename)

        for i in xrange(len(unknowns)-1, -1, -1):

            for path in paths:
                if os.path.isfile(path + sep + unknowns[i] + ".m"):
                    unknowns[i] = unknowns[i] + ".m"
                if os.path.isfile(path + sep + unknowns[i]):
                    program.include(path + sep + unknowns[i])
                    filenames.append(path + sep + unknowns.pop(i))

        if os.path.isfile(filename + ".py") and not args.reset:

            try:
                cfg = imp.load_source("cfg", filename + ".py")

                types_f, types_s, types_i, suggest =\
                    get_variables(builder.project[-1])
                for name in types_f.keys():

                    if name in cfg.functions:
                        for key in cfg.functions[name].keys():
                            types_f[name][key] = cfg.functions[name][key]

                for name in types_s.keys():

                    if name in cfg.structs:
                        for key in cfg.structs[name].keys():
                            types_s[name][key] = cfg.structs[name][key]

                for key in cfg.includes:
                    if key not in types_i:
                        types_i.append(key)

                set_variables(program, types_f, types_s, types_i)

            except:
                raise ImportError("""Suplliment file:
%s.py
is formated incorrectly. Change the format or convert with '-r' option to create
a new file.""" % filename)

    if args.disp:
        print "configure tree"

    builder.configure(suggest=2*args.suggest)

    if args.disp:
        print builder.project.summary()
        print "generate translation"

    builder.project.translate_tree(args)

    for program in builder.project:

        name = program.name

        cpp = qcpp(program)
        hpp = qhpp(program)
        py = qpy(program, prefix=True)
        log = qlog(program)

        if hpp and cpp:
            cpp = '#include "%s.hpp"\n' % name + cpp

        if log:
            t = time.time()
            log = "Translated on " +\
                date.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S\n\n') + log
        
        if args.disp:
            print "Writing files..."

        if args.reset:
            for ext in [".cpp", ".hpp", ".log", ".py"]:
                if os.path.isfile(name+ext):
                    os.remove(name+ext)

        if cpp:
            f = open(name+".cpp", "w")
            f.write(cpp)
            f.close()

        if hpp:
            f = open(name+".hpp", "w")
            f.write(hpp)
            f.close()

        if log:
            f = open(name+".log", "w")
            f.write(log)
            f.close()

        f = open(name+".py", "w")
        f.write(py)
        f.close()

        if os.path.isfile(name+".pyc"):
            os.remove(name+".pyc")


    program = builder[0]

    if args.tree:
        print utils.node_summary(program, args)
    elif args.line:
        nodes = utils.flatten(program[1], False, False, False)
        for node_ in nodes:
            if node_.line == args.line and node_.cls != "Block":
                print node_["str"].replace("__percent__", "%")
                break
    else:
        print program[1]["str"].replace("__percent__", "%")

