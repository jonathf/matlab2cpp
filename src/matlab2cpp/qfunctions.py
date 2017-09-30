
"""
For simplest use of the module, these function works as an alternative frontend
to the ``mconvert`` script.

+--------------------------------+-----------------------------------------+
| Function                       | Description                             |
+================================+=========================================+
| :py:func:`~matlab2cpp.build`   | Build token tree representation of code |
+--------------------------------+-----------------------------------------+
| :py:func:`~matlab2cpp.qcpp`    | Create content of `.cpp` file           |
+--------------------------------+-----------------------------------------+
| :py:func:`~matlab2cpp.qhpp`    | Create content of `.hpp` file           |
+--------------------------------+-----------------------------------------+
| :py:func:`~matlab2cpp.qpy`     | Create content of supplement `.py` file |
+--------------------------------+-----------------------------------------+
| :py:func:`~matlab2cpp.qlog`    | Create content of `.log` file           |
+--------------------------------+-----------------------------------------+
| :py:func:`~matlab2cpp.qscript` | Create script translation               |
+--------------------------------+-----------------------------------------+
| :py:func:`~matlab2cpp.qtree`   | Create summary of node tree             |
+--------------------------------+-----------------------------------------+
"""

import os
import matlab2cpp as mc

from . import supplement, tree
from .rules._program import add_indenting, number_fix, strip

__all__ = ["build", "qcpp", "qhpp", "qpy", "qlog", "qtree", "qscript"]

def build(code, disp=False, retall=False, suggest=True, comments=True,
        vtypes=None, **kws):
    """
Build a token tree out of Matlab code.  This function is used by the other
quick-functions as the first step in code translation.

The function also handles syntax errors in the Matlab code.  It will highlight
the line it crashed on and explain as far as it can why it crashed.

Args:
    code (str): Code to be interpreted
    disp (bool): If true, print out diagnostic information while interpreting.
    retall (bool): If true, return full token tree instead of only code related.
    suggest (bool): If true, suggestion engine will be used to fill in datatypes.
    comments (bool): If true, comments will be striped away from the solution.
    vtypes (dict): Verbatim translations added to tree before process.
    **kws: Additional arguments passed to :py:obj:`~matlab2cpp.Builder`.

Returns:
    Builder,Node: The tree constructor if `retall` is true, else the root node for code.

Example use::
    >>> builder = mc.build("a=4", retall=True)
    >>> print(isinstance(builder, mc.Builder))
    True
    >>> node = mc.build("a=4", retall=False)
    >>> print(isinstance(node, mc.Node))
    True
    >>> print(mc.build("a**b"))
    Traceback (most recent call last):
        ...
    SyntaxError: File: unamed, line 1 in Matlab code:
    a**b
      ^
    Expected: expression start

See also:
    :py:func:`~matlab2cpp.qtree`,
    :py:class:`~matlab2cpp.Builder`,
    :py:class:`~matlab2cpp.Node`

    """

    code = code + "\n\n\n\n"

    if vtypes:
        code = supplement.verbatim.set(vtypes, code)
    
    builder = tree.builder.Builder(disp=disp, comments=comments, **kws)
    builder.load("unamed", code)
    builder.configure(2*suggest)

    if retall:
        return builder

    if builder[0][1][0].name == "main":
        out = builder[0][1][0][3]
        return out

    return builder[0][1]


def qcpp(code, suggest=True, **kws):
    """
Quick code translation of matlab script to C++ executable. For Matlab modules,
code that only consists of functions, will be placed in the
:py:func:`~matlab2cpp.qhpp`. In most cases, the two functions must be used
together to create valid runnable code.

Args:
    code (str, Node, Builder): A string or tree representation of Matlab code.
    suggest (bool): If true, use the suggest engine to guess data types.
    **kws: Additional arguments passed to :py:obj:`~matlab2cpp.Builder`.

Returns:
    str: Best estimate of script. If code is a module, return an empty string.

Example::
    >>> code = "a = 4; b = 5.; c = 'abc'"
    >>> print(mc.qcpp(code, suggest=False))
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    int main(int argc, char** argv)
    {
      TYPE a, b, c ;
      a = 4 ;
      b = 5. ;
      c = "abc" ;
      return 0 ;
    }
    >>> print(mc.qcpp(code, suggest=True))
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    int main(int argc, char** argv)
    {
      double b ;
      int a ;
      std::string c ;
      a = 4 ;
      b = 5. ;
      c = "abc" ;
      return 0 ;
    }
    >>> build = mc.build(code, retall=True)
    >>> print(mc.qcpp(build) == mc.qcpp(code))
    True

See also:
    :py:func:`~matlab2cpp.qscript`,
    :py:func:`~matlab2cpp.qhpp`,
    :py:obj:`~matlab2cpp.Builder`
    """

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True, **kws)[0]

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]

    tree_ = tree_.program

    if not tree_.str:
        tree_.translate()

    includes, funcs, inlines, structs, headers, log = tree_.program

    out = ""

    if funcs and funcs[0].name == "main":

        if includes.str:
            out += includes.str + "\n\n"

        if len(headers) > 1:
            out += headers.str + "\n\n"

        if structs.str:
            out += structs.str + "\n\n"

        if funcs.str:
            out += funcs.str + "\n\n"

        out = out.replace("__percent__", "%")

        out =  out[:-2]

        out = strip(out)
        out = number_fix(out)
        out = add_indenting(out)

    return out


def qhpp(code, suggest=False):
    """
Quick module translation of Matlab module to C++ library. If the code is
a script, executable part of the code will be placed in
:py:func:`~matlab2cpp.qcpp`.

Args:
    code (str, Node, Builder): A string or tree representation of Matlab code.
    suggest (bool): If true, use the suggest engine to guess data types.
    **kws: Additional arguments passed to :py:obj:`~matlab2cpp.Builder`.

Returns:
    str: C++ code of module.

Example::
    >>> code = "function y=f(x); y=x+1; end; function g(); f(4)"
    >>> print(mc.qhpp(code))
    #ifndef F_M_HPP
    #define F_M_HPP
    <BLANKLINE>
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    TYPE f(TYPE x) ;
    void g() ;
    <BLANKLINE>
    TYPE f(TYPE x)
    {
      TYPE y ;
      y = x+1 ;
      return y ;
    }
    <BLANKLINE>
    void g()
    {
      f(4) ;
    }
    #endif
    >>> print(mc.qhpp(code, suggest=True))
    #ifndef F_M_HPP
    #define F_M_HPP
    <BLANKLINE>
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    int f(int x) ;
    void g() ;
    <BLANKLINE>
    int f(int x)
    {
      int y ;
      y = x+1 ;
      return y ;
    }
    <BLANKLINE>
    void g()
    {
      f(4) ;
    }
    #endif

See also:
    :py:func:`~matlab2cpp.qcpp`,
    :py:class:`~matlab2cpp.Builder`
    """

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True)[0]

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]

    tree_ = tree_.program

    if not tree_.str:
        tree_.translate()

    includes, funcs, inlines, structs, headers, log = tree_

    out = ""

    if funcs and funcs[0].name == "main":
        return out

    if funcs and funcs[0].name != "main":
        name = funcs[0].name + "_M_HPP"
        name = name.upper()
        name.replace(".", "_")
        out = "#ifndef " + name + "\n#define " + name + "\n\n"

    if includes.str:
        out += includes.str + "\n\n"

    if len(headers) > 1:
        out += headers.str + "\n\n"

    if structs.str:
        out += structs.str + "\n\n"

    if funcs.str:
        out += funcs.str + "\n\n"

    out = out[:-2]

    if funcs and funcs[0].name != "main":
        out += "\n#endif"

    out = out.replace("__percent__", "%")
    out = strip(out)
    out = number_fix(out)
    out = add_indenting(out)

    return out


def qpy(code, suggest=True, prefix=False):
    """
Create annotation string for the supplement file containing datatypes for the
various variables in various scopes.

Args:
    code (str, Builder, Node): Representation of the node tree.
    suggest (bool): Use the suggestion engine if appropriate.
    prefix (bool): include a helpful comment in the beginning of the string.

Returns:
	str: Supplement string

Example::
    >>> code = "a = 4; b = 5.; c = 'abc'"
    >>> print(mc.qpy(code, suggest=False))
    functions = {
      "main" : {
        "a" : "", # int
        "b" : "", # double
        "c" : "", # string
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]
    >>> print(mc.qpy(code, suggest=True))
    functions = {
      "main" : {
        "a" : "int",
        "b" : "double",
        "c" : "string",
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]

See also:
    :py:mod:`~matlab2cpp.supplement`,
    :py:mod:`~matlab2cpp.datatype`
    """

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True)[0]
        tree_.translate()

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]
        if tree_.cls != "Program":
            raise KeyError(
        "Argument code should be code string, Builder or Program-node")

    ftypes = supplement.functions.get(tree_)
    stypes = supplement.structs.get(tree_)
    itypes = supplement.includes.get(tree_)
    itypes = [i for i in itypes if supplement.includes.write_to_includes(i)]

    vtypes = supplement.verbatim.get(tree_)
    suggestions = supplement.suggests.get(tree_)

    #print("ITYPASDASDA")
    #itypes = ["#include \"" + itype.split(os.path.sep)[-1] if ".hpp" in itype else itype for itype in itypes]
    #print(itypes)
    #print(".........;;;;;;;;-----")
    #itypes = [itype.split(os.path.sep)[-1] if ".hpp" in itype else itype for itype in itypes]

    out = supplement.str_variables(ftypes, stypes, itypes, suggestions, prefix, vtypes)
    out = out.replace("__percent__", "%")

    return out


def qlog(code, suggest=False, **kws):
    """
Retrieve all errors and warnings generated through the code translation and
summarize them into a string. Each entry uses four lines. For example: ::

    Error in class Var on line 1:
    function f(x)
               ^
    unknown data type

First line indicate at what node and line-number the error occured. The second
and third prints the Matlab-code line in question with an indicator to where the
code failed. The last line is the error or warning message generated.

Args:
    code (str, Builder, Node): Representation of the node tree.
    suggest (bool): Use suggestion engine where appropriate.
    **kws: Additional arguments passed to :py:obj:`~matlab2cpp.Builder`.

Returns:
	str: A string representation of the log

Example::
    >>> print(mc.qlog("function f(x); x=4"))
    Error in class Var on line 1:
    function f(x); x=4
               ^
    unknown data type
    <BLANKLINE>
    Error in class Var on line 1:
    function f(x); x=4
                   ^
    unknown data type

See alse:
    :py:func:`~matlab2cpp.Node.error`,
    :py:func:`~matlab2cpp.Node.warning`
    """

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True)[0]

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]
        if tree_.cls != "Program":
            raise KeyError(
        "Argument code should be code string, Builder or Program-node")

    tree_.translate()
    out = tree_[5].str
    out = out.replace("__percent__", "%")

    return out

def qtree(code, suggest=False, core=False):
    """
Summarize the node tree with relevant information, where each line represents
a node.  Each line will typically look as follows::

      1  10 | | | Var        unknown      TYPE    y

The line can be interpreted as follows:

+--------+-------------------------------+------------------------------------+
| Column | Description                   | Object                             |
+========+===============================+====================================+
| 1      | Matlab code line number       | :py:obj:`~matlab2cpp.Node.line`    |
+--------+-------------------------------+------------------------------------+
| 2      | Matlab code cursor number     | :py:obj:`~matlab2cpp.Node.cur`     |
+--------+-------------------------------+------------------------------------+
| 3      | The node categorization type  | :py:class:`~matlab2cpp.Node.cls`   |
+--------+-------------------------------+------------------------------------+
| 4      | The rule used for translation | :py:obj:`~matlab2cpp.Node.backend` |
+--------+-------------------------------+------------------------------------+
| 5      | The data type of the node     | :py:mod:`~matlab2cpp.Node.type`    |
+--------+-------------------------------+------------------------------------+
| 6      | Name of the node (if any)     | :py:obj:`~matlab2cpp.Node.name`    |
+--------+-------------------------------+------------------------------------+

The vertical bars represents branches. The right most bar on each line points
upwards towards its node parent.

Args:
    code (str, Builder, Node): Representation of the node tree.
    suggest (bool): Use suggestion engine where appropriate.
    core (bool): Unly display nodes generated from Matlab code directly.
    **kws: Additional arguments passed to :py:obj:`~matlab2cpp.Builder`.

Returns:
    str: A summary of the node tree.

Example::
    >>> print(mc.qtree("function y=f(x); y=x+4") #doctest: +NORMALIZE_WHITESPACE)
          Program    program      TYPE    unamed
          | Includes   program      TYPE
          | | Include    program      TYPE    #include <armadillo>
          | | Include    program      TYPE    using namespace arma ;
     1   1| Funcs      program      TYPE    unamed
     1   1| | Func       func_return  TYPE    f
     1   1| | | Declares   func_return  TYPE
     1   1| | | | Var        unknown      TYPE    y
     1   1| | | Returns    func_return  TYPE
     1  10| | | | Var        unknown      TYPE    y
     1  13| | | Params     func_return  TYPE
     1  14| | | | Var        unknown      TYPE    x
     1  16| | | Block      code_block   TYPE
     1  18| | | | Assign     expression   TYPE
     1  18| | | | | Var        unknown      TYPE    y
     1  20| | | | | Plus       expression   TYPE
     1  20| | | | | | Var        unknown      TYPE    x
     1  22| | | | | | Int        int          int
          | Inlines    program      TYPE    unamed
          | Structs    program      TYPE    unamed
          | Headers    program      TYPE    unamed
          | | Header     program      TYPE    f
          | Log        program      TYPE    unamed
          | | Error      program      TYPE    Var:0
          | | Error      program      TYPE    Var:9
          | | Error      program      TYPE    Var:13
          | | Error      program      TYPE    Var:17
          | | Error      program      TYPE    Var:19
          | | Error      program      TYPE    Plus:19

See also:
    :py:mod:`matlab2cpp.tree`,
    :py:mod:`matlab2cpp.node`
    """

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True)[0]
        tree_.translate()

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]

    if core:
        if tree_.cls == "Program":
            if tree_[1] and tree_[1][0].name == "main":
                tree_ = tree_[1][0][-1]
            else:
                tree_ = tree_[1]

    return tree_.summary()

def qscript(code, suggest=True, ftypes={}, **kws):
    """
Perform a full translation (like :py:func:`~matlab2cpp.qcpp` and
:py:func:`~matlab2cpp.qhpp`), but only focus on the object of interest.
If for example code is provided, then only the code part of the translation will
be include, without any wrappers. It will be as close to a one-to-one
translation as you can get.  If a node tree is provided, current node position
will be source of translation.

Args:
    code (str, Builder, Node): Representation of the node tree.
    suggest (bool): Use suggestion engine where appropriate.
    **kws: Additional arguments passed to :py:obj:`~matlab2cpp.Builder`.

Returns:
	str: A code translation in C++.

Example:
    >>> print(mc.qscript("a = 4"))
    a = 4 ;
    """

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True, **kws)[0]
    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]

    if ftypes:
        tree_.ftypes = ftypes

    tree_.translate()

    out = ""
    if tree_.cls == "Program":
        if tree_[1] and tree_[1][0].name == "main":
            out = tree_[1][0][-1].str
        else:
            out = tree_[1].str
    else:
        out = tree_.str


    out = out.replace("__percent__", "%")
    out = strip(out)
    out = number_fix(out)
    out = add_indenting(out)

    return out


if __name__ == "__main__":
    import doctest
    doctest.testmod()
