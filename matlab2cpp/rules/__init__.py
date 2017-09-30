"""
.. _rules:

Datatype driven rules have the same name as datatypes reference in
:py:mod:`~matlab2cpp.datatype`. They are as follows:

+-----------+----------------------------------------+------------------+
| Datatype  | Rule                                   | Description      |
+===========+========================================+==================+
| cell      | :py:mod:`~matlab2cpp.rules._cell`      | Cell structure   |
+-----------+----------------------------------------+------------------+
| char      | :py:mod:`~matlab2cpp.rules._char`      | Word character   |
+-----------+----------------------------------------+------------------+
| cube      | :py:mod:`~matlab2cpp.rules._cube`      | Armadillo cube   |
+-----------+----------------------------------------+------------------+
| cx_cube   | :py:mod:`~matlab2cpp.rules._cx_cube`   | Armadillo cube   |
+-----------+----------------------------------------+------------------+
| cx_double | :py:mod:`~matlab2cpp.rules._cx_double` | Scalar complex   |
+-----------+----------------------------------------+------------------+
| cx_mat    | :py:mod:`~matlab2cpp.rules._cx_mat`    | Armadillo matrix |
+-----------+----------------------------------------+------------------+
| cx_rowvec | :py:mod:`~matlab2cpp.rules._cx_rowvec` | Armadillo rowvec |
+-----------+----------------------------------------+------------------+
| cx_vec    | :py:mod:`~matlab2cpp.rules._cx_vec`    | Armadillo colvec |
+-----------+----------------------------------------+------------------+
| double    | :py:mod:`~matlab2cpp.rules._double`    | Scalar double    |
+-----------+----------------------------------------+------------------+
| fcube     | :py:mod:`~matlab2cpp.rules._fcube`     | Armadillo cube   |
+-----------+----------------------------------------+------------------+
| float     | :py:mod:`~matlab2cpp.rules._float`     | Scalar float     |
+-----------+----------------------------------------+------------------+
| fmat      | :py:mod:`~matlab2cpp.rules._fmat`      | Armadillo matrix |
+-----------+----------------------------------------+------------------+
| frowvec   | :py:mod:`~matlab2cpp.rules._frowvec`   | Armadillo rowvec |
+-----------+----------------------------------------+------------------+
| fvec      | :py:mod:`~matlab2cpp.rules._fvec`      | Armadillo colvec |
+-----------+----------------------------------------+------------------+
| icube     | :py:mod:`~matlab2cpp.rules._icube`     | Armadillo cube   |
+-----------+----------------------------------------+------------------+
| imat      | :py:mod:`~matlab2cpp.rules._imat`      | Armadillo matrix |
+-----------+----------------------------------------+------------------+
| int       | :py:mod:`~matlab2cpp.rules._int`       | Scalar integer   |
+-----------+----------------------------------------+------------------+
| irowvec   | :py:mod:`~matlab2cpp.rules._irowvec`   | Armadillo rowvec |
+-----------+----------------------------------------+------------------+
| ivec      | :py:mod:`~matlab2cpp.rules._ivec`      | Armadillo colvec |
+-----------+----------------------------------------+------------------+
| mat       | :py:mod:`~matlab2cpp.rules._mat`       | Armadillo matrix |
+-----------+----------------------------------------+------------------+
| rowvec    | :py:mod:`~matlab2cpp.rules._rowvec`    | Armadillo rowvec |
+-----------+----------------------------------------+------------------+
| string    | :py:mod:`~matlab2cpp.rules._string`    | Character string |
+-----------+----------------------------------------+------------------+
| struct    | :py:mod:`~matlab2cpp.rules._struct`    | Struct           |
+-----------+----------------------------------------+------------------+
| structs   | :py:mod:`~matlab2cpp.rules._structs`   | Array of structs |
+-----------+----------------------------------------+------------------+
| ucube     | :py:mod:`~matlab2cpp.rules._ucube`     | Armadillo cube   |
+-----------+----------------------------------------+------------------+
| umat      | :py:mod:`~matlab2cpp.rules._umat`      | Armadillo matrix |
+-----------+----------------------------------------+------------------+
| urowvec   | :py:mod:`~matlab2cpp.rules._urowvec`   | Armadillo rowvec |
+-----------+----------------------------------------+------------------+
| uvec      | :py:mod:`~matlab2cpp.rules._uvec`      | Armadillo colvec |
+-----------+----------------------------------------+------------------+
| uword     | :py:mod:`~matlab2cpp.rules._uword`     | Scalar uword     |
+-----------+----------------------------------------+------------------+
| vec       | :py:mod:`~matlab2cpp.rules._vec`       | Armadillo colvec |
+-----------+----------------------------------------+------------------+

These basic types are then glued together through the following:

+-------------------------------------------+---------------------------------------+
| Rule                                      | Description                           |
+===========================================+=======================================+
| :py:mod:`~matlab2cpp.rules._code_block`   | Branches, loops etc.                  |
+-------------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.rules._expression`   | Operators and special characters      |
+-------------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.rules._func_lambda`  | Anonymous functions                   |
+-------------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.rules._func_return`  | Functions with one return value       |
+-------------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.rules._func_returns` | Functions with multiple return values |
+-------------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.rules._matrix`       | Matrix constructor                    |
+-------------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.rules._program`      | Program postprocessing                |
+-------------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.rules._reserved`     | Reserved names from Matlab library    |
+-------------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.rules._unknown`      | Structures with unknown origin        |
+-------------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.rules._verbatim`     | Special verbatim translations         |
+-------------------------------------------+---------------------------------------+
"""

import glob
import os

import matlab2cpp as mc
sep = os.path.sep

for name in glob.glob(os.path.dirname(__file__)+os.path.sep+"*.py"):

    name = name.split(sep)[-1]
    if name != "__init__":
        exec("from . import %s" % name[:-3])

from ._reserved import reserved

if __name__ == "__main__":
    import doctest
    doctest.testmod()
