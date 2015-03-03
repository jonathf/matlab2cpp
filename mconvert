#!/usr/bin/env python

import matlab2cpp
import optparse


if __name__ == "__main__":

    parser = optparse.OptionParser(
        usage="usage: %prog [options] matlab_file.m")

    parser.add_option("-t", '--tree-view', action="store_true",
            help="View the token tree and some of its attributes")
    parser.add_option("-s", '--suggestion', action="store_true",
            help="Use suggestions automatically")

    opt, args = parser.parse_args()

    tree = matlab2cpp.main(args[0], opt.suggestion)
    if opt.tree_view:
        print tree.summary()
    else:
        print tree
