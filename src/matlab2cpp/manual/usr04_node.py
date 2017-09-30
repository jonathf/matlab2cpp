"""
.. _usr04:

Behind the frontends
====================

Common for all the various frontends in :py:mod:`~matlab2cpp.qfunctions` are
two classes: :py:class:`~matlab2cpp.Builder` and :py:class:`~matlab2cpp.Node`.
The former scans Matlab code and constructs a node tree consiting of instances
of the latter.

The Builder class
-----------------

Iterating through Matlab code always starts with constructing
a :py:class:`~matlab2cpp.Builder`::

    >>> builder = mc.Builder()

This is an empty shell without any content. To give it content, we supply it
with code::

    >>> builder.load("file1.m", "a = 4")

The function saves the code locally as `builder.code` and initiate the
`create_program` method with index 0. The various `create_*` methods are then
called and used to populate the node tree. The code is considered static,
instead the index, which refer to the position in the code is increased to move
forward in the code. The various constructors uses the support modules in the
:py:mod:`~matlab2cpp.mc.qtree` to build a full toke tree.  The result is as
follows::

    >>> print(builder) # doctest: +NORMALIZE_WHITESPACE
         Project    unknown      TYPE
         | Program    unknown      TYPE    file1.m
         | | Includes   unknown      TYPE
     1  1| | Funcs      unknown      TYPE    file1.m
     1  1| | | Main       unknown      TYPE    main
     1  1| | | | Declares   unknown      TYPE
     1  1| | | | | Var        unknown      TYPE    a
     1  1| | | | Returns    unknown      TYPE
     1  1| | | | Params     unknown      TYPE
     1  1| | | | Block      unknown      TYPE
     1  1| | | | | Assign     unknown      TYPE
     1  1| | | | | | Var        unknown      TYPE    a
     1  5| | | | | | Int        unknown      TYPE
         | | Inlines    unknown      TYPE    file1.m
         | | Structs    unknown      TYPE    file1.m
         | | Headers    unknown      TYPE    file1.m
         | | Log        unknown      TYPE    file1.m

It is possible to get a detailed output of how this process is done, by turning
the ``disp`` flag on::

    >>> builder = mc.Builder(disp=True)
    >>> builder.load("file1.m", "a = 4")
    loading file1.m
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Assign      assign.single        'a = 4'
       0     Var         variables.assign     'a'
       4     Expression  expression.create    '4'
       4     Int         misc.number          '4'

This printout lists the core Matlab translation. In the four columns the first
is the index to the position in the Matlab code, the second is the node created,
the third is the file and function where the node was created, and lastly the
fourth column is a code snippet from the Matlab code. This allows for quick
diagnostics about where an error in interpretation might have occurred.

Note that the tree above for the most part doesn't have any backends or
datatypes configured.  They are all set to ``unknown`` and ``TYPE``
respectivly.  To configure backends and datatypes, use the
:py:func:`~matlab2cpp.Builder.configure` method::

    >>> builder.configure(suggest=True)
    >>> print(builder) # doctest: +NORMALIZE_WHITESPACE
         Project    program      TYPE
         | Program    program      TYPE    file1.m
         | | Includes   program      TYPE
     1  1| | Funcs      program      TYPE    file1.m
     1  1| | | Main       func_return  TYPE    main
     1  1| | | | Declares   func_return  TYPE
     1  1| | | | | Var        int          int     a
     1  1| | | | Returns    func_return  TYPE
     1  1| | | | Params     func_return  TYPE
     1  1| | | | Block      code_block   TYPE
     1  1| | | | | Assign     int          int
     1  1| | | | | | Var        int          int     a
     1  5| | | | | | Int        int          int
         | | Inlines    program      TYPE    file1.m
         | | Structs    program      TYPE    file1.m
         | | Headers    program      TYPE    file1.m
         | | Log        program      TYPE    file1.m

Multiple program can be loaded into the same builder. This allows for building
of projects that involves multiple files. For example::

    >>> builder = mc.Builder()
    >>> builder.load("a.m", "function y=a(x); y = x+1")
    >>> builder.load("b.m", "b = a(2)")

The two programs refer to each other through their names. This can the
suggestion engine use::

    >>> print(mc.qscript(builder[0]))
    int a(int x)
    {
      int y ;
      y = x+1 ;
      return y ;
    }
    >>> print(mc.qscript(builder[1]))
    b = a(2) ;

Note that the frontend functions (like :py:func:`~matlab2cpp.qscript`)
configure the tree if needed.

The Node class
--------------

So far the translation has been for the most part fairly simple, where the
translation is reduced to either a string or a tuple of strings for weaving
sub-nodes together. Consider the following example::

    >>> def Plus(node):
    ...     return "", " +", ""
    ...
    >>> print(mc.qscript("2+3", Plus=Plus))
    2 +3 ;

Though not used, the argument `node` represents the current node in the tree as
the tree is translated.  We saw this being used in the last section
:ref:`usr03` to get and set node datatype. However, there are much more you can
get out of the node. First, to help understand the current situation from
a coding perspective, one can use the help function
:py:func:`~matlab2cpp.Node.summary`, which gives a quick summary of the node
and its node children. It works the same way as the function
:py:func:`~matlab2cpp.qtree`, but can be used mid translation. For example::

    >>> def Plus(node):
    ...     print(node.summary())
    ...     return "", " +", ""
    ...
    >>> print(mc.qscript("2+3", Plus=Plus)) # doctest: +NORMALIZE_WHITESPACE
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
    >>> print(builder) # doctest: +NORMALIZE_WHITESPACE
         Project    program      TYPE
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
     1 18| | | | | Assign     expression   int
     1 18| | | | | | Var        double       double  y
     1 20| | | | | | Plus       expression   int
     1 20| | | | | | | Var        int          int     x
     1 22| | | | | | | Int        int          int
         | | Inlines    program      TYPE    unnamed
         | | Structs    program      TYPE    unnamed
         | | Headers    program      TYPE    unnamed
         | | | Header     program      TYPE    f
         | | Log        program      TYPE    unnamed


The Project is the root of the tree. To traverse the tree in direction of the
leafs can be done using indexing::

    >>> funcs = builder[0][1]
    >>> func = funcs[0]
    >>> assign = func[3][0]
    >>> var_y, plus = assign
    >>> var_x, int_4 = plus

Moving upwards towards the root of the tree is done using the
:py:attr:`~matlab2cpp.Node.parent` reference::

    >>> block = assign.parent
    >>> print(assign is var_y.parent)
    True

The node provided in the node function is the current node for which the parser
is trying to translate. This gives each node full control over context of which
is is placed. For example, consider the following::

    >>> print(mc.qtree("x(end, end)", core=True)) # doctest: +NORMALIZE_WHITESPACE
     1  1Block      code_block   TYPE
     1  1| Statement  code_block   TYPE
     1  1| | Get        unknown      TYPE    x
     1  3| | | End        expression   int
     1  8| | | End        expression   int
    >>> def End(node):
    ...     if node is node.parent[0]:
    ...         return node.parent.name + ".n_rows"
    ...     if node is node.parent[1]:
    ...         return node.parent.name + ".n_cols"
    ...
    >>> print(mc.qscript("x(end, end)", End=End))
    x(x.n_rows, x.n_cols) ;

Here the rule `End` was called twice, where the if-test produces two different
results. Also, information about the parent is used in the value returned.

See also:
    :py:class:`~matlab2cpp.Builder`
"""
import matlab2cpp as mc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
