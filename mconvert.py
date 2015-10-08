#!/usr/bin/env python
# encoding: utf8

import matlab2cpp
import argparse
from textwrap import dedent

def create_parser():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=dedent("""\
The toolbox frontend of the Matlab2cpp library.  Use this to try to do automatic
and semi-automatic translation.  The program will create files with the same
name as the input, but with various extra extensions.  Scripts will receive the
extension `.cpp`, headers and modules `.hpp`.  A file containing data type and
header information will be stored in a `.py` file. Any errors will be stored in
`.log`.
    """))

    parser.add_argument("filename",
            help="File containing valid Matlab code.")

    parser.add_argument("-t", '--tree', action="store_true",
            help="""\
Print the underlying node tree. Each line in the output represents a node and
is formated as follows:

`<codeline> <position> <class> <backend> <datatype> <name> <translation>`

The indentation represents the tree structure.
            """)

    parser.add_argument("-T", "--tree-full", action="store_true",
            help="""\
Same as -t, but the full node tree, not only code related.""")

    parser.add_argument("-s", '--suggest', action="store_true",
            help="""\
Automatically populate the `<filename>.py` file with datatype with suggestions
if possible.""")

    parser.add_argument("-r", '--reset', action="store_true",
            help="""\
Ignore the content of `<filename>.py` and make a fresh translation.""")

    parser.add_argument("-d", '--disp', action="store_true",
            help="""\
Print out the progress of the translation process.""")

    parser.add_argument("-c", '--comments', action="store_true",
            help="""\
Strip away all the comments in the output of the translation.""")

    parser.add_argument("-l", '--line', type=int, dest="line",
            help="Only display code related to code line number `<line>`.")

    return parser


parser = create_parser()

if __name__ == "__main__":

    args = parser.parse_args()
    matlab2cpp.main(args)

