#!/usr/bin/env python

import os
import matlab2cpp
import optparse


if __name__ == "__main__":

    parser = optparse.OptionParser(
        usage="usage: %prog [options] matlab_file.m")

    parser.add_option("-t", '--tree-view', action="store_true",
            help="View the token tree and some of its attributes")
    parser.add_option("-s", '--suggestion', action="store_true",
            help="Use suggestions automatically")
#      parser.add_option("-r", '--recompile', action="store_true",
#              help="Force fresh recompile")
    parser.add_option("-r", '--reset', action="store_true",
            help="Force reset on configuration")
    parser.add_option("-d", '--display', action="store_true",
            help="Display process output")
    parser.add_option("-l", '--line', type="int", dest="line",
            help="Only display fron particular code line")
#      parser.add_option("-o", '--output', type="str", dest="filename",
#              metavar="FNAME",
#              help="Save code to FNAME instead of piping to STDOUT")

    opt, args = parser.parse_args()

    path = os.path.abspath(args[0])

#      if opt.recompile or 
    if opt.reset:

        filename = os.path.basename(path)
        dirname = os.path.dirname(path)
#          name1 = dirname + os.sep + "." + filename + ".backup"
#          name2 = dirname + os.sep + "." + filename + ".pickle"
        name1 = dirname + os.sep + filename + ".py"
        name2 = dirname + os.sep + filename + ".pyc"

#          if opt.reset:
#              names = [name1, name2, name3, name4]
#          else:
#              names = [name1, name2, name4]

#          for name in names:
        for name in [name1,name2]:
            if os.path.isfile(name):
                os.remove(name)

    tree = matlab2cpp.main(path, opt.suggestion, disp=opt.display)
    if opt.tree_view:
        print tree.summary(opt.display, opt.line)
    elif opt.line:
        nodes = matlab2cpp.utils.flatten(tree, False, False, False)
        for node in nodes:
            if node.line == opt.line and node.cls != "Block":
                print node["str"]
                break

    else:
        print tree["str"]

    f = open(path + ".cpp", "w")
    f.write(tree["str"])
    f.close()

