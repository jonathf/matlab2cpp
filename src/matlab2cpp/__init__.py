#!/usr/bin/env python
"""
Matlab2cpp
==========
Toolbox for automatically converting Matlab into C++ code.
"""

import collection
import node
import targets
import snippets

import os
import imp

import utils
from treebuilder import Treebuilder


def main(opt, args):

    path = os.path.abspath(args[0])
    dirname = os.path.dirname(path) + os.path.sep
    os.chdir(dirname)

    if opt.disp:
        print "building tree..."

    builder = Treebuilder(dirname, opt.disp, opt.comments, opt.suggestion)

    filenames = [os.path.basename(path)]

    stack = []
    while filenames:

        filename = filenames.pop(0)
        if filename in stack:
            continue

        if opt.disp:
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

        if os.path.isfile(filename + ".py") and not opt.reset:

            cfg = imp.load_source("cfg", filename + ".py")
            scope = cfg.scope

            cfg, scfg = utils.get_cfg(builder.project[-1])
            for name in cfg.keys():
                if name in scope:
                    for key in scope[name].keys():
                        cfg[name][key] = scope[name][key]
            utils.set_cfg(builder.project[-1], cfg)

    if opt.disp:
        print "configure tree"

    builder.configure()

    if opt.disp:
        print builder.project.summary()
        print "generate translation"

    for program in builder.project[2:]:
        program.translate_tree(opt)
    builder.project[0].translate_tree(opt)
    builder.project[1].translate_tree(opt)

    filename = builder.project[2].name

    library = str(builder.project[0])
    if library:

        if opt.disp:
            print "creating library..."

        f = open(filename + ".h", "w")
        f.write(library)
        f.close()

    elif opt.reset and os.path.isfile(filename+".h"):
        os.remove(filename+".h")

    errors = str(builder.project[1])
    if errors:

        if opt.disp:
            print "creating error-log..."

        f = open(filename + ".log", "w")
        f.write(errors)
        f.close()

    elif opt.reset and os.path.isfile(filename+".log"):
        os.remove(filename+".log")


    first = True
    for program in builder.project[2:]:

        cfg, scfg = utils.get_cfg(program)
        program["str"] = program["str"].replace("__percent__", "%")

        annotation = """# Supplement file
#
# Valid inputs:
#
# uword   int     float   double cx_double
# uvec    ivec    fvec    vec    cx_vec
# urowvec irowvec frowvec rowvec cx_rowvec
# umat    imat    fmat    mat    cx_mat
# ucube   icube   fcube   cube   cx_cube
#
# char    struct  func_lambda

""" + utils.str_cfg(cfg, scfg)

        filename = program.name
        f = open(filename + ".py", "w")
        f.write(annotation)
        f.close()

        if opt.disp:
            print "writing translation..."

        f = open(filename + ".cpp", "w")
        f.write(str(program))
        f.close()

        if os.path.isfile(filename+".pyc"):
            os.remove(filename+".pyc")

        if first:

            first = False

            if opt.tree_view:
                print utils.summary(builder.project, opt)
            elif opt.line:
                nodes = utils.flatten(program, False, False, False)
                for node_ in nodes:
                    if node_.line == opt.line and node_.cls != "Block":
                        print node_["str"]
                        break
            else:
                print program["str"]

