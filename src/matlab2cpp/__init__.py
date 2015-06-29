#!/usr/bin/env python

import supplement
import utils
import collection

import os
from os.path import sep
import imp

from treebuilder import Treebuilder
from supplement import set_variables, get_variables, str_variables
from utils import translate, qtranslate, qsupplement, build


def main(args):

    builder = Treebuilder(disp=args.disp, comments=args.comments)
    print "args.comments", args.comments

    paths = os.path.abspath(os.path.dirname(args.filename))

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
                if os.path.isfile(path +sep+ unknowns[i] + ".m"):
                    unknowns[i] = unknowns[i] + ".m"
                if os.path.isfile(path +sep+ unknowns[i]):
                    filenames.append(path +sep+ unknowns.pop(i))

        if os.path.isfile(filename + ".py") and not args.reset:

            # try:
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

#             except:
#                 raise ImportError("""Suplliment file:
# %s.py
# is formated incorrectly. Change the format or convert with '-r' option to create
# a new file.""" % filename)

        if program[1][0].cls == "Main":

            if program[2]:
                program[2].include("ipp")

        if program[3]:
            program[3].include("hpp")
        elif program[4]:
            program[4].include("hpp")

    if args.disp:
        print "configure tree"

    builder.configure(suggest=2*args.suggest)

    if args.disp:
        print builder.project.summary()
        print "generate translation"

    builder.project.translate_tree(args)

    for program in builder.project:

        name = program.name
        includes, funcs, inlines, structs, headers, errorlog = program

        cpp, ipp, hpp, log, py = "", "", "", "", ""


        if funcs[0].cls == "Main":

            if inlines:
                ipp += str(inlines)

            if includes:
                cpp += str(includes) + "\n\n"

            cpp += str(funcs)
        
        else:
            if inlines:
                ipp += str(inlines) + "\n\n"

            if includes:
                ipp += str(includes) + "\n\n"

            ipp += str(funcs)

        if structs:
            hpp += str(structs) + "\n\n"

        hpp += str(headers)

        log += str(errorlog)

        py += supplement.str_variables(*supplement.get_variables(program),
                prefix=True)

        cpp = cpp.replace("__percent__", "%")
        ipp = ipp.replace("__percent__", "%")
        hpp = hpp.replace("__percent__", "%")
        log = log.replace("__percent__", "%")
        py = py.replace("__percent__", "%")
        
        if args.disp:
            print "Writing files..."

        if args.reset:
            for ext in [".cpp", ".hpp", ".ipp", ".log", ".py"]:
                if os.path.isfile(name+ext):
                    os.remove(name+ext)

        if cpp:
            f = open(name+".cpp", "w")
            f.write(cpp)
            f.close()

        if ipp:
            f = open(name+".ipp", "w")
            f.write(ipp)
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
                print node_["str"]
                break
    else:
        print program[1]["str"]

