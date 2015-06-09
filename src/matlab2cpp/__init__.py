#!/usr/bin/env python
"""
Matlab2cpp is a semi-automatic tool for converting code from Matlab to C++.

Note that it is not meant as a complete tool for creating runnable C++ code.
For example, the `eval`-function will not be supported because there is no
general way to implement it in C++.
Instead the program is aimed as support tool, which aims at speed up the
conversion process as much as possible for a user that needs to convert Matlab
programs by hand anyway.
The software does this by converting the basic structures of the
Matlab-program (functions, branches, loops, etc.), adds
variable declarations, and for some lower level code, do a complete
translation.
Any problem the program encounters will be written in a log-file.

Currently, the code will not convert the large library collection
of functions that Matlab currently possesses.
However, there is no reason for the code not to support these features in time.
"""

import supplement
import utils

import os
import imp
import argparse

from treebuilder import Treebuilder, build
from supplement import set_variables, get_variables, str_variables
from utils import translate

def create_parser():

    parser = argparse.ArgumentParser(
        description="Convert Matlab code to C++")
        # "usage: %prog [options] matlab_file.m"

    parser.add_argument("filename",
            help="File containing valid Matlab code.")

    parser.add_argument("-t", '--tree-view', action="store_true",
            help="View the token tree and some of its attributes")
    parser.add_argument("-s", '--suggestion', action="store_true",
            help="Use suggestions automatically")
    parser.add_argument("-r", '--reset', action="store_true",
            help="Force reset on configuration")
    parser.add_argument("-d", '--disp', action="store_true",
            help="Display process output")
    parser.add_argument("-c", '--comments', action="store_true",
            help="Strip comments from file")
    parser.add_argument("-l", '--line', type=int, dest="line",
            help="Only display single code line")

    return parser


def main(args):

    path = os.path.abspath(args.filename)
    dirname = os.path.dirname(path) + os.path.sep
    os.chdir(dirname)

    if args.disp:
        print "building tree..."

    builder = Treebuilder(dirname, args.disp, args.comments, args.suggestion)

    filenames = [os.path.basename(path)]

    stack = []
    while filenames:

        filename = filenames.pop(0)
        if filename in stack:
            continue

        if args.disp:
            print "loading", filename

        stack.append(filename)

        unassigned = builder.load(filename)
        for i in xrange(len(unassigned)-1, -1, -1):

            if os.path.isfile(unassigned[i] + ".m"):
                unassigned[i] = unassigned[i] + ".m"

            if not os.path.isfile(unassigned[i]):
                # TODO error for unassigned
                del unassigned[i]

        filenames.extend(unassigned)

        if os.path.isfile(filename + ".py") and not args.reset:

            cfg = imp.load_source("cfg", filename + ".py")
            scope = cfg.scope

            types, suggestions = supplement.get_variables(builder.project[-1])
            for name in types.keys():
                if name in scope:
                    for key in scope[name].keys():
                        types[name][key] = scope[name][key]
            supplement.set_variables(builder.project[-1], types)

    if args.disp:
        print "configure tree"

    builder.configure()

    if args.disp:
        print builder.project.summary()
        print "generate translation"

    for program in builder.project[2:]:
        program.translate_tree(args)
    builder.project[0].translate_tree(args)
    builder.project[1].translate_tree(args)

    filename = builder.project[2].name

    library = str(builder.project[0])
    if library:

        if args.disp:
            print "creating library..."

        f = open(filename + ".h", "w")
        f.write(library)
        f.close()

    elif args.reset and os.path.isfile(filename+".h"):
        os.remove(filename+".h")

    errors = str(builder.project[1])
    if errors:

        if args.disp:
            print "creating error-log..."

        f = open(filename + ".log", "w")
        f.write(errors)
        f.close()

    elif args.reset and os.path.isfile(filename+".log"):
        os.remove(filename+".log")


    first = True
    for program in builder.project[2:]:

        types, suggestions = supplement.get_variables(program)
        program["str"] = program["str"].replace("__percent__", "%")

        annotation = supplement.str_variables(types, suggestions)

        filename = program.name
        f = open(filename + ".py", "w")
        f.write(annotation)
        f.close()

        if args.disp:
            print "writing translation..."

        f = open(filename + ".cpp", "w")
        f.write(str(program))
        f.close()

        if os.path.isfile(filename+".pyc"):
            os.remove(filename+".pyc")

        if first:

            first = False

            if args.tree_view:
                print utils.summary(builder.project, args)
            elif args.line:
                nodes = utils.flatten(program, False, False, False)
                for node_ in nodes:
                    if node_.line == args.line and node_.cls != "Block":
                        print node_["str"]
                        break
            else:
                print program["str"]

