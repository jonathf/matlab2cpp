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

import utils
import preproc

def build(arg):
    """Contruct token tree from file"""

    input = antlr.FileStream(arg)
    lexer = MatlabLexer(input)
    stream = antlr.CommonTokenStream(lexer)
    parser = MatlabParser(stream)
    program = parser.program()

    listener = MatlabListener()
    walker = antlr.ParseTreeWalker()
    walker.walk(listener, program)

    program = program.program
    program.index = 0

    return program


def main(path, suggestion=False):

    filename = os.path.basename(path)
    dirname = os.path.dirname(path)
    os.chdir(dirname)

    f = open(filename, "r")
    code1 = f.read()
    f.close()

    # Deal with backup and pickled files
    if os.path.isfile("." + filename + ".backup")\
        and os.path.isfile("." + filename + ".pickle"):

        f = open("." + filename + ".backup", "r")
        code2 = f.read()
        f.close()

        if code1 != code2:

            code3, error = preproc.prefix_hack(code1)

            if error:
                print error
                sys.exit(1)

            f = open("."+filename, "w")
            f.write(code3)
            f.close()

            tree = build("."+filename)

            f = open("." + filename + ".pickled", "w")
            cPickle.dump(tree, f)
            f.close()

            f = open("." + filename, "w")
            f.write(code1)
            f.close()

        else:

            f = open("." + filename + ".pickled", "r")
            tree = cPickle.load(f)
            f.close()

    else:

        code3, error = preproc.prefix_hack(code1)

        if error:
            print error
            sys.exit(1)

        f = open("."+filename, "w")
        f.write(code3)
        f.close()

        if error:
            print error
            sys.exit(1)

        tree = build("."+filename)
        f = open("."+filename+".pickled", "w")
        cPickle.dump(tree, f)
        f.close()

        shutil.copyfile(filename, "." + filename + ".backup")

    if os.path.isfile(filename + ".py"):
        shutil.copyfile(filename + ".py", "__cfg__.py")
        from __cfg__ import scope
        os.remove("__cfg__.py")
        os.remove("__cfg__.pyc")

        cfg, scfg = utils.get_cfg(tree)
        for name in cfg.keys():
            if name in scope:
                for key in cfg[name].keys():
                    if key in scope[name]:
                        cfg[name][key] = scope[name][key]

    else:
        cfg, scfg = utils.get_cfg(tree)

    if suggestion:
        tree.generate()
        cfg, scfg = utils.get_cfg(tree)
        while [s for s in scfg.values() if s]:
            for name in cfg.keys():
                cfg[name].update(scfg.get(name, {}))
            utils.set_cfg(tree, cfg)
            tree.generate()
            cfg, scfg = utils.get_cfg(tree)

    else:
        utils.set_cfg(tree, cfg)
        tree.generate()

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

    f = open(filename + ".py", "w")
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
