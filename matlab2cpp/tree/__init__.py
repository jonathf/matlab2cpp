"""
The module :py:mod:`~matlab2cpp.tree` contains the following submodule:

+--------------------------------------+---------------------------------------+
| Module                               | Description                           |
+===========+==========================+=======================================+
| :py:mod:`~matlab2cpp.tree.Builder`   | Contains the                          |
|                                      | :py:class:`~matlab2cpp.Builder` class |
|                                      | that is used to convert Matlab code   |
|                                      | into node tree representation         |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.constants` | A collection of usefull constants     |
|                                      | used by various interpretation  rules |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.assign`    | Support functions for variable        |
|                                      | assignments                           |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.branches`  | Support functions for if-tests,       |
|                                      | loops, try-blocks                     |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.codeblock` | Support functions for filling in      |
|                                      | codeblock content                     |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.expression`| Support functions for filling in      |
|                                      | expression content                    |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.findend`   | Look-ahead functions for finding the  |
|                                      | end of various code structures        |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.functions` | Support functions for constructing    |
|                                      | Functions, both explicit and lambda,  |
|                                      | and program content                   |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.identify`  | Look-ahead functions for identifying  |
|                                      | ambigous contexts                     |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.iterate`   | Support functions for segmentation of |
|                                      | lists                                 |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.misc`      | Miscelenious support functions        |
+--------------------------------------+---------------------------------------+
| :py:mod:`~matlab2cpp.tree.variables` | Support functions for constructing    |
|                                      | various variables                     |
+--------------------------------------+---------------------------------------+
"""

import matlab2cpp as mc
from builder import Builder
__all__ = ["Builder"]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
