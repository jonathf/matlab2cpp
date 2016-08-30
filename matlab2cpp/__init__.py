"""

The toolbox is sorted into the following modules:

+----------------------------------+----------------------------------------+
| Module                           | Description                            |
+==================================+========================================+
| :py:mod:`~matlab2cpp.qfunctions` | Functions for performing simple        |
|                                  | translations                           |
+----------------------------------+----------------------------------------+
| :py:class:`~matlab2cpp.Builder`  | Constructing a tree from Matlab code   |
+----------------------------------+----------------------------------------+
| :py:class:`~matlab2cpp.Node`     | Components in the tree representation  |
|                                  | of the code                            |
+----------------------------------+----------------------------------------+
| :py:mod:`~matlab2cpp.collection` | The collcetion of various node         |
+----------------------------------+----------------------------------------+
| :py:mod:`~matlab2cpp.configure`  | Rutine for setting datatypes and       |
|                                  | backends of the various nodes          |
+----------------------------------+----------------------------------------+
| :py:mod:`~matlab2cpp.rules`      | Translation rules                      |
+----------------------------------+----------------------------------------+
| :py:mod:`~matlab2cpp.supplement` | Functions for inserting and extraction |
|                                  | datatypes                              |
+----------------------------------+----------------------------------------+
| :py:mod:`~matlab2cpp.testsuite`  | Suite for testing software             |
+----------------------------------+----------------------------------------+


The simplest way to use the library is to use the quick translation functions.
They are available through the `mc.qfunctions` module and mirrors the
functionality offered by the `mconvert` function.
"""

__version__ = 0.5

import time
from datetime import datetime as date
import os
from os.path import sep
import imp

import supplement
import node
import tree

import qfunctions
import collection
import configure
import rules
import manual
import re


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

    builder = tree.builder.Builder(disp=args.disp, comments=args.comments,
                                   original=args.original, enable_omp=args.enable_omp, enable_tbb=args.enable_tbb)

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

            code = re.sub('%#', '##', code)

            if os.path.isfile(filename + ".py") and not args.reset:

                try:
                    cfg = imp.load_source("cfg", filename + ".py")

                except:
                    raise ImportError("""Supplement file:
    %s.py
    is formated incorrectly. Change the format or convert with '-r' option to create
    a new file.""" % filename)

                if "verbatims" in cfg.__dict__ and cfg.verbatims:
                    verbatims = cfg.verbatims
                    code = supplement.verbatim.set(verbatims, code)

                builder.load(filename, code)
                program = builder[-1]

                if "functions" in cfg.__dict__:

                    funcs = program.ftypes

                    for name in funcs.keys():
                        if name in cfg.functions:
                            for key in cfg.functions[name].keys():
                                funcs[name][key] = cfg.functions[name][key]

                    program.ftypes = funcs

                if "structs" in cfg.__dict__:

                    structs = program.stypes

                    for name in structs.keys():
                        if name in cfg.structs:
                            for key in cfg.structs[name].keys():
                                structs[name][key] = cfg.structs[name][key]

                    program.stypes = structs

                if "includes" in cfg.__dict__:

                    includes = program.itypes

                    for key in cfg.includes:
                        if key not in includes:
                            includes.append(key)

                    program.itypes = includes

            else:
                builder.load(filename, code)
                program = builder[-1]

            # add unknown variables to stack if they exists as files
            unknowns = builder.get_unknowns(filename)

            for i in xrange(len(unknowns)-1, -1, -1):

                for path in paths:
                    if os.path.isfile(path + sep + unknowns[i] + ".m"):
                        unknowns[i] = unknowns[i] + ".m"
                    if os.path.isfile(path + sep + unknowns[i]):
                        program.include(path + sep + unknowns[i])
                        filenames.append(path + sep + unknowns.pop(i))


    else:
        builder.load("unnamed", args.filename)
        program = builder[-1]

    #--- work in progress ---
    #Run this mlabwrap code
    #Have this in a try-except block
    #import mwrapmat
    #wrapmat = mwrapmat.Wrapmat()
    #wrapmat.eval_code(builder)
    #------------------------

    #--- work in progress ---
    #Get data types from matlab
    if args.matlab_suggest:
        import matlab_types
        builder = matlab_types.mtypes(builder)
    #------------------------

    if args.disp:
        print "configure tree"

    #if args.enable_omp:
        #print "Hello world!"

    builder.configure(suggest=(2*args.suggest or args.matlab_suggest))

    #--- work in progress ---
    #Modify the Abstract Syntax Tree (AST)
    import modify
    builder.project = modify.transform_AST(builder.project, args.nargin)
    #------------------------
    
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

        if args.disp:
            print "Writing files..."

        if args.reset:
            for ext in [".cpp", ".hpp", ".log", ".py"]:
                if os.path.isfile(name+ext):
                    os.remove(name+ext)

        if cpp:
            cpp = """// Automatically translated using Matlab2cpp %g on %s

%s""" % (__version__, stamp, cpp)
            f = open(name+".cpp", "w")
            f.write(cpp)
            f.close()

        if hpp:
            hpp = """// Automatically translated using Matlab2cpp %g on %s
            
%s""" % (__version__, stamp, hpp)
            f = open(name+".hpp", "w")
            f.write(hpp)
            f.close()

        if log:
            log = "Automatically translated using Matlab2cpp %g on %s\n\n%s"\
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
                print node_.str.replace("__percent__", "%")
                break
    else:
        print program[1].str.replace("__percent__", "%")


