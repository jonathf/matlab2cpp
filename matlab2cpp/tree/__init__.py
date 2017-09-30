"""
Parsing of Matlab code is solely done through the
:py:class:`~matlab2cpp.Builder` class. It contains three main use methods:
:py:func:`~matlab2cpp.Builder.load`, :py:func:`~matlab2cpp.Builder.configure`
and :py:func:`~matlab2cpp.Builder.translate`. In addition there are
a collection of method with names starting with ``create_`` that creates
various structures of the node tree.

In addition to :py:class:`~matlab2cpp.Builder` there are submodules with
support function for modules. Constructor help functions are as follows:

+--------------------------------------+--------------------------------------+
| Module                               | Description                          |
+======================================+======================================+
| :py:mod:`matlab2cpp.tree.assign`     | Support functions for variable       |
|                                      | assignments                          |
+--------------------------------------+--------------------------------------+
| :py:mod:`matlab2cpp.tree.branches`   | Support functions for if-tests,      |
|                                      | loops, try-blocks                    |
+--------------------------------------+--------------------------------------+
| :py:mod:`matlab2cpp.tree.codeblock`  | Support functions for filling in     |
|                                      | codeblock content                    |
+--------------------------------------+--------------------------------------+
| :py:mod:`matlab2cpp.tree.expression` | Support functions for filling in     |
|                                      | expression content                   |
+--------------------------------------+--------------------------------------+
| :py:mod:`matlab2cpp.tree.functions`  | Support functions for constructing   |
|                                      | Functions, both explicit and lambda, |
|                                      | and program content                  |
+--------------------------------------+--------------------------------------+
| :py:mod:`matlab2cpp.tree.misc`       | Miscelenious support functions       |
+--------------------------------------+--------------------------------------+
| :py:mod:`matlab2cpp.tree.variables`  | Support functions for constructing   |
|                                      | various variables                    |
+--------------------------------------+--------------------------------------+

In addition a collectio of genereal purpose modules are available:

+-------------------------------------+---------------------------------------+
| Module                              | Description                           |
+=====================================+=======================================+
| :py:mod:`matlab2cpp.tree.constants` | A collection of usefull constants     |
|                                     | used by various interpretation  rules |
+-------------------------------------+---------------------------------------+
| :py:mod:`matlab2cpp.tree.findend`   | Look-ahead functions for finding the  |
|                                     | end of various code structures        |
+-------------------------------------+---------------------------------------+
| :py:mod:`matlab2cpp.tree.identify`  | Look-ahead functions for identifying  |
|                                     | ambigous contexts                     |
+-------------------------------------+---------------------------------------+
| :py:mod:`matlab2cpp.tree.iterate`   | Support functions for segmentation of |
|                                     | lists                                 |
+-------------------------------------+---------------------------------------+
"""

import matlab2cpp as mc

from . import findend, identify, constants
from .builder import Builder

__all__ = ["Builder"]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
