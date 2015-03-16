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
    parser.add_option("-r", '--recompile', action="store_true",
            help="Force fresh recompile")
    parser.add_option("-d", '--display', action="store_true",
            help="Display process output")
    parser.add_option("-g", '--group', type="int", dest="group",
            help="Only display fron particular group")
    parser.add_option("-o", '--output', type="str", dest="filename",
            metavar="FNAME",
            help="Save code to FNAME instead of piping to STDOUT")

    opt, args = parser.parse_args()

    path = os.path.abspath(args[0])

    if opt.recompile:

        filename = os.path.basename(path)
        dirname = os.path.dirname(path)
        name1 = dirname + os.sep + "." + filename + ".backup"
        name2 = dirname + os.sep + "." + filename + ".pickle"
        name3 = dirname + os.sep + filename + ".py"
        for name in [name1, name2, name3]:
            if os.path.isfile(name):
                os.remove(name)

    tree = matlab2cpp.main(path, opt.suggestion, disp=opt.display)
    out = ""
    if opt.tree_view:
        if opt.group:
            out = tree.summary(opt.display, opt.group)
        else:
            out = tree.summary(opt.display)
    elif opt.group:
        nodes = matlab2cpp.utils.flatten(tree)
        for node in nodes:
            if node["index"] == opt.group:
                out = node.parent["str"]
                break
        else:
            out = "<group not recognized>"

    else:
        out = tree

    if opt.filename:

        f = open(opt.filename, "wb")
        f.write(str(out))
        f.close()

    else:

        print out
