"""
The simplest way to interact with the `Matlab2cpp`-toolbox is to use the
`mconvert` frontend.  The script automatically creates files with various
extensions containing translations and/or meta-information.
Even though `mconvert` is sufficient for performing all code translation, many
of the examples in this manual are done through a python interface, since some
of the python functionality also will be discussed.  Given that `Matlab2cpp`
is properly installed on your system, the python library is available in
Python's path.  For the examples, the module is assumed imported as

    >>> import matlab2cpp as mc

The toolbox is sorted into the following modules:

+----------------------------------+--------------------------------------+
| Module                           | Description                          |
+==================================+======================================+
| :py:mod:`~matlab2cpp.qfunctions` | Functions for performing simple      |
|                                  | translations                         |
+----------------------------------+--------------------------------------+
| :py:mod:`~matlab2cpp.tree`       | Constructing a tree from Matlab code |
+----------------------------------+--------------------------------------+
| :py:mod:`~matlab2cpp.datatype`   | The various node data types          |
+----------------------------------+--------------------------------------+
| :py:mod:`~matlab2cpp.node`       | Node behavior                        |
+----------------------------------+--------------------------------------+
| :py:mod:`~matlab2cpp.collection` | The collcetion of various node       |
+----------------------------------+--------------------------------------+
| :py:mod:`~matlab2cpp.rule`       | Translation rules                    |
+----------------------------------+--------------------------------------+
| :py:mod:`~matlab2cpp.inlines`    | Code insertion                       |
+----------------------------------+--------------------------------------+

The simplest way to use the library is to use the quick translation functions.
They are available through the `mc.qfunctions` module and mirrors the
functionality offered by the `mconvert` function.
"""

__version__ = 1.0

import time
from datetime import datetime as date
import os
from os.path import sep
import imp

import node
import tree

import supplement
import qfunctions
import collection
import inlines
import configure
import rules

__all__ = ["main"]

from qfunctions import *
__all__ += qfunctions.__all__

from tree import *
__all__ += tree.__all__

from node import *
__all__ += node.__all__

from collection import *
__all__ += collection.__all__


def main(args):
    """
Initiate the interpretation and conversion process.

Args:
    args (ArgumentParser): arguments parsed through mconvert
    """

    builder = tree.builder.Builder(disp=args.disp, comments=args.comments)

    if os.path.isfile(args.filename):

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

            builder.load(filename, code)
            program = builder[-1]
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
                        supplement.get_variables(builder.project[-1])
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

                    supplement.set_variables(program, types_f, types_s, types_i)

                except:
                    raise ImportError("""Supplement file:
    %s.py
    is formated incorrectly. Change the format or convert with '-r' option to create
    a new file.""" % filename)

    else:

        program = builder.load("unnamed", args.filename)

    if args.disp:
        print "configure tree"

    builder.configure(suggest=2*args.suggest)

    if args.disp:
        print builder.project.summary()
        print "generate translation"

    builder.project.translate(args)

    t = time.time()
    stamp = date.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

    for program in builder.project:

        name = program.name

        cpp = qfunctions.qcpp(program)
        hpp = qfunctions.qhpp(program)
        py = qfunctions.qpy(program, prefix=True)
        log = qfunctions.qlog(program)

        if hpp and cpp:
            cpp = '#include "%s.hpp"\n' % name + cpp

        if args.disp:
            print "Writing files..."

        if args.reset:
            for ext in [".cpp", ".hpp", ".log", ".py"]:
                if os.path.isfile(name+ext):
                    os.remove(name+ext)

        if cpp:
            cpp = "// Automatically translated using Matlab2cpp %d on %s\n\n%s"\
                    % (__version__, stamp, cpp)
            f = open(name+".cpp", "w")
            f.write(cpp)
            f.close()

        if hpp:
            hpp = "// Automatically translated using Matlab2cpp %d on %s\n\n%s"\
                    % (__version__, stamp, hpp)
            f = open(name+".hpp", "w")
            f.write(hpp)
            f.close()

        if log:
            log = "Automatically translated using Matlab2cpp %d on %s\n\n%s"\
                    % (__version__, stamp, log)
            f = open(name+".log", "w")
            f.write(log)
            f.close()

        f = open(name+".py", "w")
        f.write(py)
        f.close()

        if os.path.isfile(name+".pyc"):
            os.remove(name+".pyc")


    program = builder[0]

    if args.tree_full:
        print program.summary(args)

    elif args.tree:
        if program[1][0].cls == "Main":
            print program[1][0][3].summary(args)
        else:
            print program[1].summary(args)

    elif args.line:
        nodes = program[1].flatten(False, False, False)
        for node_ in nodes:
            if node_.line == args.line and node_.cls != "Block":
                print node_["str"].replace("__percent__", "%")
                break
    else:
        print program[1]["str"].replace("__percent__", "%")

