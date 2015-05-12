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
    parser.add_option("-r", '--reset', action="store_true",
            help="Force reset on configuration")
    parser.add_option("-d", '--display', action="store_true",
            help="Display process output")
    parser.add_option("-c", '--comments', action="store_true",
            help="Strip comments from file")
    parser.add_option("-l", '--line', type="int", dest="line",
            help="Only display fron particular code line")

    opt, args = parser.parse_args()

    path = os.path.abspath(args[0])
    filename = os.path.basename(path)
    dirname = os.path.dirname(path)

    if opt.reset:
        os.remove(dirname + os.sep + filename + ".py")

    tree = matlab2cpp.main(path, opt.suggestion, disp=opt.display,
            comments=opt.comments)
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

    os.remove(dirname + os.sep + filename + ".pyc")

    f = open(path + ".cpp", "w")
    f.write(tree["str"])
    f.close()

