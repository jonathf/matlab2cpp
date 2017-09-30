"""Create parser for m2cpp."""

import argparse
from textwrap import dedent
import glob
import matlab2cpp


HELP_DESCRIPTION = """\
*** Matlab2cpp ***

The toolbox frontend of the Matlab2cpp library.  Use this to try to do automatic
and semi-automatic translation from Matlab source file to C++.  The program
will create files with the same name as the input, but with various extra
extensions.  Scripts will receive the extension `.cpp`, headers and modules
`.hpp`.  A file containing data type and header information will be stored in
a `.py` file. Any errors will be stored in `.log`.
"""


def matlab_file_completer(prefix, **kws):
    """Complete files with matlab extensions."""
    return glob.glob("{}*.m".format(prefix))


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=dedent(HELP_DESCRIPTION))

    parser.add_argument(
        "filename", help="File containing valid Matlab code."
    ).completer = matlab_file_completer

    parser.add_argument(
        "-o", '--original', action="store_true", help=(
            "Include original Matlab code line as comment before the "
            "C++ translation of the code line"),
    )

    parser.add_argument(
        "-c", '--comments', action="store_true", help=(
            "Include Matlab comments in the generated C++ files."),
    )
    parser.add_argument(
        "-s", '--suggest', action="store_true", help=(
            "Automatically populate the `<filename>.py` file with datatype "
            "with suggestions if possible."),
    )
    parser.add_argument(
        "-S", '--matlab-suggest', action="store_true", help=(
            "Creates a folder m2cpp_temp. In the folder the matlab file(s) to "
            "be translated are also put. These matlab file(s) are slightly "
            "modified so that they output data-type information of the "
            "variables to file(s). This output can then be used to set the "
            "datatypes for the translation."),
    )
    parser.add_argument(
        "-r", '--reset', action="store_true", help=(
            "Ignore the content of `<filename>.py` and make a fresh translation."),
    )
    parser.add_argument(
        "-t", '--tree', action="store_true", help=(
            "Print the underlying node tree. Each line in the output "
            "represents a node and is formated as follows: \n\n"
            "`<codeline> <position> <class> <backend> <datatype> <name> <translation>`\n\n"
            "The indentation represents the tree structure."),
    )

    parser.add_argument(
        "-T", "--tree-full", action="store_true", help=(
            "Same as -t, but the full node tree, but include meta-nodes."),
    )
    parser.add_argument(
        "-d", '--disp', action="store_true", help=(
            "Print out the progress of the translation process."),
    )
    parser.add_argument(
        "-p", "--paths_file", type=str, dest="paths_file", help=(
            "Flag and paths_file (-p path_to_pathsfile). m2cpp will look for "
            "matlab files in the location specified in the paths_file"),
    )
    parser.add_argument(
        "-omp", '--enable-omp', action="store_true", help=(
            "OpenMP code is inserted for Parfor and loops marked with the "
            "pragma %%#PARFOR (in Matlab code) when this flag is set."),
    )
    parser.add_argument(
        "-tbb", '--enable-tbb', action="store_true", help=(
            "TBB code is inserted for Parfor and loops marked with the "
            "pragma %%#PARFOR (in Matlab code) when this flag is set."),
    )
    parser.add_argument(
        "-ref", '--reference', action="store_true", help=(
            'For the generated C++ code, function input parameters are '
            '"copied by value" as default. With this flag some input '
            'parameters in the generated code can be const references. '
            'There can be some performance advantage of using const '
            'references instead of "copied by value". Note that Matlab '
            '"copies by value". The Matlab code you try to translate to '
            'C++ code could try read as well as write to this input variable. '
            "The code generator doesn't perform an analysis to detect this "
            'and then "copy by value" for this variable.'),
    )
    parser.add_argument(
        "-l", '--line', type=int, dest="line", help=(
            "Only display code related to code line number `<line>`."),
    )
    parser.add_argument(
        "-n", '--nargin', action="store_true", help=(
            "Don't remove if and switch branches which use nargin variable."),
    )

    return parser
