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

from MatlabLexer import MatlabLexer
from MatlabParser import MatlabParser
from MatlabListener import MatlabListener
import antlr4 as antlr

import os
import sys
import shutil
import cPickle
import imp
import re

import utils
import preproc

def build(arg, disp=False):
    """Contruct token tree from file"""

    if disp:
        print "loading Antlr..."

    input = antlr.FileStream(arg)
    lexer = MatlabLexer(input)
    stream = antlr.CommonTokenStream(lexer)
    parser = MatlabParser(stream)
    program = parser.program()

    if disp:
        print "running tree-walker..."

    listener = MatlabListener()
    walker = antlr.ParseTreeWalker()
    walker.walk(listener, program)

    program = program.program
    program.index = 0

    return program


def main(path, suggestion=False, disp=False):

    filename = os.path.basename(path)
    dirname = os.path.dirname(path)
    os.chdir(dirname)

    if disp:
        print "reading file..."
    f = open(filename, "rb")
    code1 = f.read()
    f.close()

    # Deal with backup and pickled files
    if os.path.isfile("." + filename + ".backup")\
            and os.path.isfile("." + filename + ".pickle"):

        if disp:
            print "reading backup..."

        f = open("." + filename + ".backup", "rb")
        code2 = f.read()
        f.close()

        if code1 != code2:

            if disp:
                print "code mismatch!"
                print "running preproc..."

            code3, error = preproc.prefix_hack(code1)

            if error:
                print error
                sys.exit(1)

            if disp:
                print "writing preproc..."

            f = open("."+filename, "wb")
            f.write(code3)
            f.close()

            if disp:
                print "building token-tree..."

            tree = build("."+filename, disp=disp)

            if disp:
                print "writing pickle..."

            f = open("." + filename + ".pickled", "wb")
            cPickle.dump(tree, f)
            f.close()

            if disp:
                print "writing backup..."

            f = open("." + filename+".backup", "wb")
            f.write(code1)
            f.close()

        else:

            if disp:
                print "reading pickle..."

            f = open("." + filename + ".pickled", "rb")
            tree = cPickle.load(f)
            f.close()

        if disp:
            print "writing backup..."

    else:

        if disp:
            print "running preproc..."
        code3, error = preproc.prefix_hack(code1)

        if error:
            print error
            sys.exit(1)

        if disp:
            print "writing preproc..."

        f = open("."+filename, "wb")
        f.write(code3)
        f.close()

        if error:
            print error
            sys.exit(1)

        if disp:
            print "building token-tree..."

        tree = build("."+filename)

        if disp:
            print "writing pickle..."

        f = open("."+filename+".pickled", "wb")
        cPickle.dump(tree, f)
        f.close()

        if disp:
            print "writing backup..."

        shutil.copyfile(filename, "." + filename + ".backup")

    if os.path.isfile(filename + ".py"):

        if disp:
            print "cfg found!"
            print "loading cfg..."

        cfg = imp.load_source("cfg", filename + ".py")
        scope = cfg.scope

#          shutil.copyfile(filename + ".py", "__cfg__.py")
#          from __cfg__ import scope
#  
#          if disp:
#              print "deleting temp cfg..."
#  
#          os.remove("__cfg__.py")
#          os.remove("__cfg__.pyc")

        if disp:
            print "loading scope..."

        cfg, scfg = utils.get_cfg(tree)
        for name in cfg.keys():
            if name in scope:
                for key in cfg[name].keys():
                    if key in scope[name]:
                        cfg[name][key] = scope[name][key]

    else:

        if disp:
            print "cfg missing!"
            print "loading scope..."

        cfg, scfg = utils.get_cfg(tree)

    if suggestion:
        print "suggestion-mode!"
        tree.generate(disp=disp)
        cfg, scfg = utils.get_cfg(tree)
        i = 1
        while [s for s in scfg.values() if s]:
            print "iteration", i
            for name in cfg.keys():
                cfg[name].update(scfg.get(name, {}))
            utils.set_cfg(tree, cfg)
            tree.generate(disp=disp)
            cfg, scfg = utils.get_cfg(tree)
            i += 1

    else:

        if disp:
            print "dumping scope..."
        utils.set_cfg(tree, cfg)

        if disp:
            print "generate tree..."
        tree.generate(disp=disp)

    if disp:
        print "creating cfg..."

    annotation = """# Supplement file
#
# Valid inputs:
# float
# int
# fvec
# ivec
# frowvec
# irowvec
# fmat
# imat

""" + utils.str_cfg(cfg, scfg)

    if disp:
        print "writing cfg..."

    f = open(filename + ".py", "wb")
    f.write(annotation)
    f.close()

    return tree

#      if tree.errors:
#          print "Problems while compiling."
#          print "The following unsupported structures was identified:"
#          print
#          print "* " + "\n* ".join(list(tree.errors))
#          print
#          print "Please remove these features to make the script compileable."
#          print
#  
