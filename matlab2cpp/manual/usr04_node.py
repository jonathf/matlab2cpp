"""
.. _usr04:

Node behavior
=============

So far the translation has been for the most part fairly simple, where the
translation is reduced to either a string or a tuple of strings for weaving
sub-nodes together. Consider the following example::

    >>> def Plus(node):
    ...     return "", " +", ""
    ...
    >>> print mc.qscript("2+3", Plus=Plus)
    2 +3 ;

The node argument represents the current node of the tree as it is translated.
We saw this being used in the last section :ref:`usr03` to get and set node
datatype. However, there are much more you can get out of the node. First, to
help understand the current situation from a coding perspective, one can use
the help function ``summary``, which gives a quick summary of the node and its
node children. It works the same way as the function
:py:func:`~matlab2cpp.qtree`, but can be used mid translation. For example::

    >>> def Plus(node):
    ...     print node.summary()
    ...     return "", " +", ""
    ...
    >>> print mc.qscript("2+3", Plus=Plus) # doctest: +NORMALIZE_WHITESPACE
     1  1Plus       expression   int
     1  1| Int        int          int
     1  3| Int        int          int
    2 +3 ;

The first line represent the current node
:py:class:`~matlab2cpp.collection.Plus`.

introduce the node tree structure and how the nodes relate to each other.
This will vary from program to program, so a printout of the current state is
a good startingpoint. This can either be done through the function
:py:mod:`~matlab2cpp.qtree`, or manually as follows::

    >>> builder = mc.Builder()
    >>> builder.load("unnamed", "function y=f(x); y=x+4")
    >>> builder[0].ftypes = {"f" : {"x": "int", "y": "double"}}
    >>> builder.translate()
    >>> print builder # doctest: +NORMALIZE_WHITESPACE
         Project    program      TYPE    project
         | Program    program      TYPE    unnamed
         | | Includes   program      TYPE
         | | | Include    program      TYPE    #include <armadillo>
         | | | Include    program      TYPE    using namespace arma ;
     1  1| | Funcs      program      TYPE    unnamed
     1  1| | | Func       func_return  TYPE    f
     1  1| | | | Declares   func_return  TYPE
     1  1| | | | | Var        double       double  y
     1  1| | | | Returns    func_return  TYPE
     1 10| | | | | Var        double       double  y
     1 13| | | | Params     func_return  TYPE
     1 14| | | | | Var        int          int     x
     1 16| | | | Block      code_block   TYPE
     1 18| | | | | Assign     unknown      int
     1 18| | | | | | Var        double       double  y
     1 20| | | | | | Plus       expression   int
     1 20| | | | | | | Var        int          int     x
     1 22| | | | | | | Int        int          int
         | | Inlines    program      TYPE    unnamed
         | | Structs    program      TYPE    unnamed
         | | Headers    program      TYPE    unnamed
         | | | Header     program      TYPE    f
         | | Log        program      TYPE    unnamed


The Project is the root of the tree. To move down from there can be done using
indexing. All nodes are interable, allowing standard Python movement::

    >>> funcs = builder[0][1]
    >>> func = funcs[0]
    >>> assign = func[3][0]
    >>> var_y, plus = assign
    >>> var_x, int_4 = plus

Moving upwards in the tree is done using the `parent` reference::

    >>> block = assign.parent
    >>> print assign is var_y.parent
    True

The node provided in the node function is the current node for which the parser
is trying to translate. This gives each node full control over context of which
is is placed. For example, consider the following::

    >>> print mc.qtree("x(end, end)", core=True) # doctest: +NORMALIZE_WHITESPACE
     1  1Block      code_block   TYPE
     1  1| Statement  code_block   TYPE
     1  1| | Get        unknown      TYPE    x
     1  3| | | End        expression   TYPE
     1  8| | | End        expression   TYPE
    >>> def End(node):
    ...     if node is node.parent[0]:
    ...         return node.parent.name + ".n_rows"
    ...     if node is node.parent[1]:
    ...         return node.parent.name + ".n_cols"
    ...
    >>> print mc.qscript("x(end, end)", End=End)
    x(x.n_rows, x.n_cols) ;

 Here the rule `End` was called twice, where the if-test produces two different
 results. Also, information about the parent is used in the value returned.

.. automodule:: matlab2cpp.node.frontend

"""
import matlab2cpp as mc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
