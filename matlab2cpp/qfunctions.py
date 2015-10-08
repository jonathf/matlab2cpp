"""
Quick functions collection of frontend tools for performing code translation.

Functions
~~~~~~~~~

build       Convert Matlab-code into a token tree
qcpp        Create script-conversion of code or token tree
qhpp        Create function modules of code or token tree
qpy         Create supplement file of code or token tree
qlog        Create error and warning log of code or token tree
qtree       Create a summary of a token tree representation
qscript     Create core script converions of code or token tree


"""

import supplement
import tree
import node

__all__ = ["build", "qcpp", "qhpp", "qpy", "qlog", "qtree", "qscript"]

def build(code, disp=False, retall=False, suggest=False, comments=False, **kws):
    """
Build a token tree out of Matlab code.  This function is used by the other
quick-functions as the first step in code translation.

The function also handles syntax errors in the Matlab code.  It will highlight
the line it crashed on and explain as far as it can why it crashed.

Args:
    code (str): Code to be interpreted

Kwargs:
    disp (bool): If true, print out diagnostic information while interpreting
    retall (bool): If true, return full token tree instead of only code related.
    suggest (bool): If true, suggestion engine will be used to fill in datatypes.
    comments (bool): If true, comments will be striped away from the solution.

Returns:
	Builder,Node: The tree constructor if `retall` is true, else the root node for code.

Example:
    >>> builder = mc.build("a=4", retall=True)
    >>> print isinstance(builder, mc.Builder)
    True
    >>> node = mc.build("a=4", retall=False)
    >>> print isinstance(node, mc.Node)
    True
    >>> print mc.build("a**b")
    Traceback (most recent call last):
        ...
    SyntaxError: line 1 in Matlab code:
    a**b
      ^
    Expected: expression start

See also:
    `mc.builder`
    """

    code = code + "\n\n\n\n"
    tree_ = tree.builder.Builder(disp=disp, comments=comments, **kws)
    tree_.load("unamed", code)
    tree_.configure(2*suggest)
    if retall:
        return tree_
    if tree_[0][1][0].name == "main":
        out = tree_[0][1][0][3]
        return out
    return tree_[0][1]


def qcpp(code, suggest=True, **kws):
    """
Quick code translation of matlab script to C++ executable. For Matlab modules,
code that only consists of functions, will be placed in the `mc.hpp`. In most
cases, the two functions must be used together to create valid runnable code.

Args:
    code (str, Node, Builder): A string or tree representation of Matlab code.

Kwargs:
    suggest (bool): If true, use the suggest engine to guess data types.

Returns:
    str: Best estimate of script. If code is a module, return an empty string.

Example:
    >>> code = "a = 4; b = 5.; c = 'abc'"
    >>> print mc.qcpp(code, suggest=False)
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
    >>> print mc.qcpp(code, suggest=True)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    int main(int argc, char** argv)
    {
      int a ;
      double b ;
      string c ;
      a = 4 ;
      b = 5. ;
      c = "abc" ;
      return 0 ;
    }
    >>> build = mc.build(code, retall=True)
    >>> build.configure()
    >>> print mc.qcpp(build) == mc.qcpp(code)
    True

See also:
    `mc.qscript`
    `mc.hpp`
    """

    if isinstance(code, str):
        build_ = build(code, suggest=suggest, retall=True, **kws)
        tree_ = build_[0]

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]
        if tree_.cls != "Program":
            raise KeyError(
        "Argument code should be code string, Builder or Program-node")

    tree_.translate()

    out = ""
    if tree_[1] and tree_[1][0].name == "main":
        out += tree_[0].str
        if out:
            out += "\n\n"
        out += tree_[1].str

        out = out.replace("__percent__", "%")

    return out


def qhpp(code, suggest=False):
    """
Quick module translation of Matlab module to C++ library. If the code is
a script, executable part of the code will be placed in `mc.cpp`.

Args:
    code (str, Node, Builder): A string or tree representation of Matlab code.

Kwargs:
    suggest (bool): If true, use the suggest engine to guess data types.

Returns:
    str: Best estimate of script. If code is a module, return an empty string.

Example:
    >>> code = "function y=f(x); y=x+1; end; function g(); f(4)"
    >>> print mc.qhpp(code)
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
    >>> print mc.qhpp(code, suggest=True)
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

See also:
    `mc.qcpp`
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

    if not tree_.str:
        tree_.translate()

    out = ""
    if tree_[1] and tree_[1][0].name == "main":

        if len(tree_[4]) > 1:
            out += tree_[4].str + "\n\n"

        if tree_[2].str:
            out += tree_[2].str + "\n\n"

        if tree_[3].str:
            out += tree_[3].str + "\n\n"

        if out[-2:] == "\n\n":
            out = out[:-2]

    else:
        if tree_[0]:
            out += tree_[0].str + "\n\n"

        if tree_[3].str:
            out += tree_[3].str + "\n\n"

        if tree_[2].str:
            out += tree_[2].str + "\n\n"

        if len(tree_[4]) > 1:
            out += tree_[4].str + "\n\n"

        out += tree_[1].str

    out = out.replace("__percent__", "%")

    return out


def qpy(code, suggest=True, prefix=False):
    """
Create annotation string for the supplement file containing datatypes for the
various variables in various scopes.

Args:
    code (str, Builder, Node): Representation of the node tree.

Kwargs:
    suggest (bool): Use the suggestion engine if appropriate.
    prefix (bool): include a helpful comment in the beginning of the string.

Returns:
	str: Supplement string

Example:
    >>> code = "a = 4; b = 5.; c = 'abc'"
    >>> print mc.qpy(code, suggest=False)
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
    >>> print mc.qpy(code, suggest=True)
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
    `mc.supplement`
    `mc.datatype`
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

    tf, ts, ti, sugs = supplement.get_variables(tree_)
    out = supplement.str_variables(tf, ts, ti, sugs, prefix=prefix)
    out = out.replace("__percent__", "%")

    return out


def qlog(code, suggest=False):
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

Kwargs:
    suggest (bool): Use suggestion engine where appropriate.

Returns:
	str: A string representation of the log

Example:
    >>> print mc.qlog("function f(x); x=4")
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
    `mc.Node.error`
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

    out = tree_[5].str
    out = out.replace("__percent__", "%")

    return out

def qtree(code, suggest=False):
    """
Summarize the node tree with relevant information, where each line represents
a node.
Each line will typically look as follows: ::

      1  10 | | | Var        unknown      TYPE    y

The first number represents code line in the Matlab file the node was taken from
(if appropriate). The second number represents the cursor position on the same
line. The vertical bars and the following indentation represents tree structure.
Children of a node is indented with two spaces. All siblings will have the same
level of indentation. The first string is the node type. The second string is
the rule used to translate the node. The third string is the datatype of the
node. Parenthesis will suround the string if the type is only suggested. The
last string is the name of the node (if appropriate).

Args:
    code (str, Builder, Node): Representation of the node tree.

Kwargs:
    suggest (bool): Use suggestion engine where appropriate.

Returns:
	str: A summary of the node tree.
Example:
    >>> print mc.qtree("function y=f(x); y=x+4")
            Program    program      TYPE    unamed
            Includes   program      TYPE    
            | Include    program      TYPE    #include <armadillo>
            | Include    program      TYPE    using namespace arma ;
      1   1 Funcs      program      TYPE    unamed
      1   1 | Func       func_return  TYPE    f
      1   1 | | Declares   func_return  TYPE    
      1   1 | | | Var        unknown      TYPE    y
      1   1 | | Returns    func_return  TYPE    
      1  10 | | | Var        unknown      TYPE    y
      1  13 | | Params     func_return  TYPE    
      1  14 | | | Var        unknown      TYPE    x
      1  16 | | Block      code_block   TYPE    
      1  18 | | | Assign     unknown      TYPE    
      1  18 | | | | Var        unknown      TYPE    y
      1  20 | | | | Plus       expression   TYPE    
      1  20 | | | | | Var        unknown      TYPE    x
      1  22 | | | | | Int        int          int     
            Inlines    program      TYPE    unamed
            Structs    program      TYPE    unamed
            Headers    program      TYPE    unamed
            | Header     program      TYPE    f
            Log        program      TYPE    unamed
            | Error      program      TYPE    Var:0
            | Error      program      TYPE    Var:9
            | Error      program      TYPE    Var:13
            | Error      program      TYPE    Var:17
            | Error      program      TYPE    Var:19
            | Error      program      TYPE    Plus:19

See also:
    `mc.node`
    `mc.tree`
    """

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True)[0]
        tree_.translate()

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]

    if isinstance(tree_, node.Node):
        raise KeyError(
                "Argument code should be string, Builder or Node")

    return tree_.summary()

def qscript(code, suggest=False, **kws):
    """
Perform a full translation (like `mc.qcpp` and `mc.qhpp`), but only focus on the
object of interest.
If for example code is provided, then only the code part of the translation will
be include, without any wrappers. It will be as close to a 1-to-1 translation as
you can get.
If a node tree is provided, current node position will be source of translation.

Args:
    code (str, Builder, Node): Representation of the node tree.

Kwargs:
    suggest (bool): Use suggestion engine where appropriate.

Returns:
	str: A code translation in C++.

Example:
    >>> print mc.qscript("a = 4", suggest=True)
    a = 4 ;
    """

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True, **kws)[0]
        tree_.translate()
    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]

    out = ""
    if tree_.cls == "Program":
        if tree_[1] and tree_[1][0].name == "main":
            out = tree_[1][0][-1].str
        else:
            out = tree_[1].str

    out = out.replace("__percent__", "%")

    return out


if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()
