#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
"""

The toolbox is sorted into the following modules:

+----------------------------------+----------------------------------------+
| Module                           | Description                            |
+==================================+========================================+
| :py:mod:`~matlab2cpp.qfunctions` | Functions for performing simple        |
|                                  | translations                           |
+----------------------------------+----------------------------------------+
| :py:class:`~matlab2cpp.Builder`  | Constructing a tree from Matlab code   |
+----------------------------------+----------------------------------------+
| :py:class:`~matlab2cpp.Node`     | Components in the tree representation  |
|                                  | of the code                            |
+----------------------------------+----------------------------------------+
| :py:mod:`~matlab2cpp.collection` | The collcetion of various node         |
+----------------------------------+----------------------------------------+
| :py:mod:`~matlab2cpp.configure`  | Rutine for setting datatypes and       |
|                                  | backends of the various nodes          |
+----------------------------------+----------------------------------------+
| :py:mod:`~matlab2cpp.rules`      | Translation rules                      |
+----------------------------------+----------------------------------------+
| :py:mod:`~matlab2cpp.supplement` | Functions for inserting and extraction |
|                                  | datatypes                              |
+----------------------------------+----------------------------------------+
| :py:mod:`~matlab2cpp.testsuite`  | Suite for testing software             |
+----------------------------------+----------------------------------------+


The simplest way to use the library is to use the quick translation functions.
They are available through the `mc.qfunctions` module and mirrors the
functionality offered by the `m2cpp` function.
"""
__version__ = "2.0"

try:
    import argcomplete
except ImportError:
    argcomplete = None

from .parser import create_parser
from .qfunctions import *


def m2cpp(args=None):
    """
    Execute main parser.

    Args:
        args (Optional[List[str]]):
            Argument to be parsed. If omitted, use ``sys.args``.
    """
    parser = create_parser()
    if argcomplete is not None:
        argcomplete.autocomplete(parser)

    args = parser.parse_args(args)

    from matlab2cpp.frontend import execute_parser
    execute_parser(args)
