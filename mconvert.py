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
    parser.add_option("-r", '--reset', action="store_true",
            help="Force reset on configuration")
    parser.add_option("-d", '--disp', action="store_true",
            help="Display process output")
    parser.add_option("-c", '--comments', action="store_true",
            help="Strip comments from file")
    parser.add_option("-l", '--line', type="int", dest="line",
            help="Only display single code line")

    opt, args = parser.parse_args()
    tree = matlab2cpp.main(opt, args)

