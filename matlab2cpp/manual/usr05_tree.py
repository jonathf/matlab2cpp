"""
Creating node tree
===================

Translating Matlab code is noted in the last chapter done in three steps:
interpret Matlab code and construct the node tree, configuring the data types
in the tree and translating the tree into C++ code. Here we are going to look
at the first step: interpreting the Matlab code using the
:py:class:`~matlab2cpp.Builder` class.  See :py:mod:`~matlab2cpp.datatype` and
:py:mod:`~matlab2cpp.rules` for the two other steps respecticly.

The class :py:mod:`~matlab2cpp.Builder` creates a tree representation of the
code where each segment of code is represented by a node.  To observe the node
structure it possible to either use :program:`mconvert` with the `-t` option,
or the python function :py:func:`~matlab2cpp.qtree`. For example::

    >>> print mc.qtree("a = 2+2") # doctest: +NORMALIZE_WHITESPACE
       Program    program      TYPE    unamed
       | Includes   program      TYPE
       | | Include    program      TYPE    #include <armadillo>
       | | Include    program      TYPE    using namespace arma ;
    1 1| Funcs      program      TYPE    unamed
    1 1| | Main       func_return  TYPE    main
    1 1| | | Declares   func_return  TYPE
    1 1| | | | Var        unknown      (int)   a
    1 1| | | Returns    func_return  TYPE
    1 1| | | Params     func_return  TYPE
    1 1| | | Block      code_block   TYPE
    1 1| | | | Assign     unknown      TYPE
    1 1| | | | | Var        unknown      (int)   a
    1 5| | | | | Plus       expression   int
    1 5| | | | | | Int        int          int
    1 7| | | | | | Int        int          int
       | Inlines    program      TYPE    unamed
       | Structs    program      TYPE    unamed
       | Headers    program      TYPE    unamed
       | Log        program      TYPE    unamed
       | | Error      program      TYPE    Var:0

There is quite a lot going on in this picture. First of all, each line
represents a node. The columns represents respectively

+--------+------------------------------------+---------------------------------+
| Column | Description                        | Object                          |
+========+====================================+=================================+
| 1      | Matlab code line number (if any)   | :py:obj:`~matlab2cpp.Node.line` |
+--------+------------------------------------+---------------------------------+
| 2      | Matlab code cursor number (if any) | :py:obj:`~matlab2cpp.Node.cur`  |
+--------+------------------------------------+---------------------------------+
| 3      | The node categorization type       | :py:class:`~matlab2cpp.node`    |
+--------+------------------------------------+---------------------------------+
| 4      | The rule used for translation      | :py:obj:`~matlab2cpp.rules`     |
+--------+------------------------------------+---------------------------------+
| 5      | The data type of the node          | :py:mod:`~matlab2cpp.datatype`  |
+--------+------------------------------------+---------------------------------+
| 6      | Name of the node (if any)          | :py:obj:`~matlab2cpp.Node.name` |
+--------+------------------------------------+---------------------------------+

For more on node meta-information, see :py:mod:`~matlab2cpp.node`.

In addition to include nodes that represents the translation, there is a bit of
meta-information in the code. This will not be assigned neither line number nor
cursor number. The remaining lines are the nodes used to do the actual code
translation. The can be interpreted as follows:

* The program consists of a collection of functions
  :py:class:`~matlab2cpp.Funcs`
* The collection of funcs contains one main function
  :py:class:`~matlab2cpp.Main`
* The main function contains information about
  :py:class:`declarations <matlab2cpp.Declares>`,
  :py:class:`return values <matlab2cpp.Returns>` and
  :py:class:`parameters <matlab2cpp.Params>` in the first three node children.
* The fourth child is the :py:class:`code block <matlab2cpp.Block>` which
  contains the function content.
* The code block contains one code line, an :py:class:`assignment
  <matlab2cpp.Assign>`.
* The assignment contains a left hand side :py:class:`variable
  <matlab2cpp.Var>` and an expression right hand side :py:class:`addition
  operator <matlab2cpp.Plus>`
* The :py:class:`addition <matlab2cpp.Plus>` contains the two
  :py:class:`integers <matlab2cpp.Int>`.

The class of each node is determined as the are created as the Matlab code is
translated. The translation handler and the datatype however varies a bit. Some
are fixed, like that `Program` is handled by the `program` translation rule or
that `Int` have the datatype `int`. Others, like the variable `Var` can change
upon how the configuration is set up. Intuitively enough, if datatype is set to
`int`, then the translation handler will follow and also be `int`:

    >>> print mc.qtree("a = 2+2", suggest=True) # doctest: +NORMALIZE_WHITESPACE
       Program    program      TYPE    unamed
       | Includes   program      TYPE
       | | Include    program      TYPE    #include <armadillo>
       | | Include    program      TYPE    using namespace arma ;
    1 1| Funcs      program      TYPE    unamed
    1 1| | Main       func_return  TYPE    main
    1 1| | | Declares   func_return  int
    1 1| | | | Var        int          int     a
    1 1| | | Returns    func_return  TYPE
    1 1| | | Params     func_return  TYPE
    1 1| | | Block      code_block   TYPE
    1 1| | | | Assign     unknown      TYPE
    1 1| | | | | Var        int          int     a
    1 5| | | | | Plus       expression   int
    1 5| | | | | | Int        int          int
    1 7| | | | | | Int        int          int
       | Inlines    program      TYPE    unamed
       | Structs    program      TYPE    unamed
       | Headers    program      TYPE    unamed
       | Log        program      TYPE    unamed

In other words, there are for these nodes, multiple translation for depending
on context. This is important to achieve the desired behavior.

.. automodule:: matlab2cpp.tree

Builder class
-------------

.. automodule:: matlab2cpp.tree.builder
.. autoclass:: matlab2cpp.Builder
    :members:

"""
import matlab2cpp as mc
