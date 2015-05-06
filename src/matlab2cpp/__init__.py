#!/usr/bin/env python
"""
Matlab2cpp
==========
Toolbox for automatically converting Matlab into C++ code.
"""

#  import collection
#  import node
#  import targets
#  import snippets

from MatlabLexer import MatlabLexer
from MatlabParser import MatlabParser
from MatlabListener import MatlabListener
import antlr4 as antlr

import os
#  import sys
import shutil
import cPickle
import imp

import utils
#  import preproc
import process

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
    f = open(filename, "rU")
    code1 = f.read()
    f.close()

#      # Deal with backup and pickled files
#      if os.path.isfile("." + filename + ".backup")\
#              and os.path.isfile("." + filename + ".pickled"):
#  
#          if disp:
#              print "reading backup..."
#  
#          f = open("." + filename + ".backup", "rU")
#          code2 = f.read()
#          f.close()
#  
#          if code1 != code2:
#  
#              if disp:
#                  print "code mismatch!"
#  
#              if disp:
#                  print "building token-tree..."
#  
#              tree = process.process(code1, disp=disp)
#  
#              if disp:
#                  print "writing pickle..."
#  
#              f = open("." + filename + ".pickled", "w")
#              cPickle.dump(tree, f)
#              f.close()
#  
#              if disp:
#                  print "writing backup..."
#  
#              f = open("." + filename+".backup", "w")
#              f.write(code1)
#              f.close()
#  
#          else:
#  
#              if disp:
#                  print "reading pickle..."
#  
#              f = open("." + filename + ".pickled", "r")
#              tree = cPickle.load(f)
#              f.close()
#  
#      else:


    if disp:
        print "building token-tree..."

    tree = process.process(code1, disp=disp)


#          if disp:
#              print "writing backup..."
#  
#          shutil.copyfile(filename, "." + filename + ".backup")

    if os.path.isfile(filename + ".py"):

        if disp:
            print "cfg found!"
            print "loading cfg..."

        scope = imp.load_source("cfg", filename + ".py").scope

        if disp:
            print "loading scope..."

        cfg, scfg = utils.get_cfg(tree)
        for name in cfg.keys():
            if name in scope:
                for key in cfg[name].keys():
                    if key in scope[name]:
                        cfg[name][key] = scope[name][key]
        utils.set_cfg(tree, cfg)

    else:

        if disp:
            print "cfg missing!"
            print "loading scope..."

    tree.configure(suggestion=suggestion, disp=disp)
    tree.generate(disp=disp)
    cfg, scfg = utils.get_cfg(tree)
    tree["str"] = tree["str"].replace("__percent__", "%")

    if disp:
        print "creating cfg..."

    annotation = """# Supplement file
#
# Valid inputs:
#
# uint    int     float   double cx_double
# uvec    ivec    fvec    vec    cx_vec
# urowvec irowvec frowvec rowvec cx_rowvec
# umat    imat    fmat    mat    cx_mat
# ucube   icube   fcube   cube   cx_cube
#
# char    struct  func_lambda

""" + utils.str_cfg(cfg, scfg)

    if disp:
        print "writing cfg..."

    f = open(filename + ".py", "w")
    f.write(annotation)
    f.close()

#      if disp:
#          print "writing pickle..."
#  
#      f = open("."+filename+".pickled", "w")
#      cPickle.dump(tree, f)
#      f.close()

    if disp:
        print "creating error-log..."

    errorlog = tree.error_log()

    if disp:
        print "writing error-log..."

    f = open(filename + ".log", "w")
    f.write(errorlog)
    f.close()

    if disp:
        print "writing translation..."

    f = open(filename + ".cpp", "w")
    f.write(str(tree))
    f.close()

    return tree
