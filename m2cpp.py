#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argparse
from textwrap import dedent
from glob import glob

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
        help="File containing valid Matlab code.").completer=\
                lambda prefix, **kws: glob("*.m")

parser.add_argument("-o", '--original', action="store_true",
        help="Include original Matlab code line as comment before the C++ translation of the code line")

parser.add_argument("-c", '--comments', action="store_true",
        help="""\
Include Matlab comments in the generated C++ files.""")

parser.add_argument("-s", '--suggest', action="store_true",
        help="""\
Automatically populate the `<filename>.py` file with datatype with suggestions
if possible.""")
parser.add_argument("-S", '--matlab-suggest', action="store_true",
        help="""Creates a folder m2cpp_temp. In the folder the matlab file(s) to be translated are also put. These matlab file(s) are slightly modified so that they output data-type information of the variables to file(s). This output can then be used to set the datatypes for the translation.

1)m2cpp "file.m" -S, 2)run the code m2cpp_temp code with matlab to create the data-type files, 3)m2cpp "file.m" -S will create matlab file in m2cpp_temp again. Now that the data-type files are found, the extracted information will be used to set the data-types.""")

parser.add_argument("-r", '--reset', action="store_true",
        help="""\
Ignore the content of `<filename>.py` and make a fresh translation.""")

parser.add_argument("-t", '--tree', action="store_true",
        help="""\
Print the underlying node tree. Each line in the output represents a node and
is formated as follows:

`<codeline> <position> <class> <backend> <datatype> <name> <translation>`

The indentation represents the tree structure.
        """)

parser.add_argument("-T", "--tree-full", action="store_true",
        help="""\
Same as -t, but the full node tree, but include meta-nodes.""")

parser.add_argument("-d", '--disp', action="store_true",
        help="""\
Print out the progress of the translation process.""")

parser.add_argument("-p", "--paths_file", nargs='?', default='',
        help="""\
Flag and paths_file (-p path_to_pathsfile). m2cpp will look for matlab files in the location specified in the paths_file""")

parser.add_argument("-omp", '--enable-omp', action="store_true",
                    help="""\
OpenMP code is inserted for Parfor and loops marked with the pragma %%#PARFOR (in Matlab code) when this flag is set.""")

parser.add_argument("-tbb", '--enable-tbb', action="store_true",
                    help="""\
TBB code is inserted for Parfor and loops marked with the pragma %%#PARFOR (in Matlab code) when this flag is set.""")

parser.add_argument("-l", '--line', type=int, dest="line",
        help="Only display code related to code line number `<line>`.")

parser.add_argument("-n", '--nargin', action="store_true",
        help="Don't remove if and switch branches which use nargin variable.")


try:
    import argcomplete
    argcomplete.autocomplete(parser)
except:
    pass

if __name__ == "__main__":

    args = parser.parse_args()
    import matlab2cpp
    matlab2cpp.main(args)

