"""
Not all translation is carried out successfully. There are many reasons for
this. The most basic is to provide the interpreter with invalid Matlab code.
For example if one provides invalid Matlab code to the interpreter, it will
create an error:

    >>> print mc.qcpp("a**b")
    Traceback (most recent call last):
        ...
    SyntaxError: line 1 in Matlab code:
    a**b
      ^
    Expected: expression start

The interpreter highlights the line it crashed on and explain as far as it can
why it crashed. In this example `**` is not a valid operator and the
interpreter expects an expression after the first `*`.

Beyond the invalid syntax, the interpreter is able to construct a full tree
representation of the code, which is then converted into C++ code.  The basic
translation will as far as possible make a full translation. For example:

    >>> print mc.qhpp("function f(x)")
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    void f(TYPE x)
    {
      // Empty block
    }

Without a context, the variable type of `x` in the function argument is unknown.
The default data type `TYPE` is therefore used. This obviously isn't correct,
but is a filler such that the data type can be defined later through for example
the `.py` file. The program is awere of this and log error in the log file. The
function `mc.qlog` can be used to observe this log:

    >>> print mc.qlog("function f(x)")
    Error in class Var on line 1:
    function f(x)
               ^
    unknown data type

Like syntax error, the log specifies the line number, points at the cursor
location and describe the problem at hand.  In addition it also specifies the
class of the node.  This allows the user easy access to the problems that
program had during translation.
"""

import supplement
import tree

__all__ = ["build", "qcpp", "qhpp", "qpy", "qlog", "qtree", "qscript"]

def build(code, disp=False, retall=False, suggest=False, comments=False, **kws):

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
Quick code translation of matlab script to C++ executable.
It is the simplest way of translating code.

Args:
    code (str, Node): A string or tree representation of Matlab code.

Kwargs:
    suggest (bool): If true, use the suggest engine to guess data types.

Returns:
    str: Best estimate of script. If code is a module, return an empty string.

Example:

    >>> print mc.qcpp("a = 4; b = 5.; c = 'abc'", suggest=False)
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
    >>> print mc.qcpp("a = 4; b = 5.; c = 'abc'", suggest=True)
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
    """

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True, **kws)[0]

        tree_.translate()
    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]

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
Quick module translation of matlab script to C++ executable.
It is the simplest way of translating code.

Args:
    code (str, Node): A string or tree representation of Matlab code.

Kwargs:
    suggest (bool): If true, use the suggest engine to guess data types.

Returns:
    str: Best estimate of script. If code is a module, return an empty string.

Example:

    """

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True)[0]
        tree_.translate()

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]
        else:
            tree_ = tree_.program

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

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True)[0]

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]
        else:
            tree_ = tree_.program

    tf, ts, ti, sugs = supplement.get_variables(tree_)
    out = supplement.str_variables(tf, ts, ti, sugs, prefix=prefix)
    out = out.replace("__percent__", "%")

    return out


def qlog(code, suggest=False):

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True)[0]
        tree_.translate()

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]
        else:
            tree_ = tree_.program

    out = tree_[5].str
    out = out.replace("__percent__", "%")

    return out

def qtree(code, suggest=False):

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True)[0]
        tree_.translate()

    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]
        else:
            tree_ = tree_.program

    return tree_.summary()

def qscript(code, suggest=False, **kws):

    if isinstance(code, str):
        tree_ = build(code, suggest=suggest, retall=True, **kws)[0]
        tree_.translate()
    else:
        tree_ = code
        if isinstance(tree_, tree.builder.Builder):
            tree_ = tree_[0]
        else:
            tree_ = tree_.program

    out = ""
    if tree_[1] and tree_[1][0].name == "main":
        out = tree_[1][0][-1].str
        out = out.replace("__percent__", "%")

    return out


if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()
