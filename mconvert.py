#!/usr/bin/env python
# encoding: utf8

"""

"""

import matlab2cpp
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Convert Matlab code to C++")
        # "usage: %prog [options] matlab_file.m"

    parser.add_argument("filename",
            help="File containing valid Matlab code.")

    parser.add_argument("-t", '--tree-view', action="store_true",
            help="View the token tree and some of its attributes")
    parser.add_argument("-s", '--suggestion', action="store_true",
            help="Use suggestions automatically")
    parser.add_argument("-r", '--reset', action="store_true",
            help="Force reset on configuration")
    parser.add_argument("-d", '--disp', action="store_true",
            help="Display process output")
    parser.add_argument("-c", '--comments', action="store_true",
            help="Strip comments from file")
    parser.add_argument("-l", '--line', type=int, dest="line",
            help="Only display single code line")

    args = parser.parse_args()
    tree = matlab2cpp.main(args)

