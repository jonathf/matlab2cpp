"""
Functions with single return

Nodes
-----
Func : Function definition
    Contains: Declares, Returns, Params, Block
    Property: name

Returns : Function return variables
    Contains: Var, ...

Params : Function parameter variables

Get : Function call
    Example: "y(4)"
    Contains: Gets
    Property: name

Var : Function call hidden as variable
    Example "y"
    Contains: nothing
"""

import matlab2cpp as mc

from .function import type_string
from .variables import Get
from .assign import Assign


def Var(node):
    """Function call as variable
    
Writing a function as if a variable, is equivalent to calling the function
without arguments.

property: name (of variable)

Examples:
    >>> print(mc.qscript("function y=f(); y=1; end; function g(); f"))
    int f()
    {
      int y ;
      y = 1 ;
      return y ;
    }
    <BLANKLINE>
    void g()
    {
      f() ;
    }
"""
    # push the job over to Get
    return Get(node)

Returns = "", ""
"single return value are used varbatim"

def Params(node):
    """Parameters in functions with one return

Adds type prefix.

Contains: Var*

Examples:
    >>> code = "function y=f(a,b,c,d,e); y=1"
    >>> builder = mc.Builder()
    >>> builder.load("unamed", code)
    >>> builder[0].ftypes = {"f":{"a": "int", "b":"double", "c":"cx_mat",
    ...     "d":"func_lambda", "e":"struct", "y":"int"}}
    >>> print(mc.qscript(builder))
    int f(int a, double b, cx_mat c, std::function d, _E e)
    {
      int y ;
      y = 1 ;
      return y ;
    }
    """

    out = ""

    # if -ref, -reference flag option
    if node.project.builder.reference:
        out += ", ".join(["const " + type_string(child) + "& " + child.name if child.dim > 0 else
                           type_string(child) + " " + child.name for child in node])

    else:
        out = ", ".join([type_string(child) + " " + child.name for child in node])

    return out


def Declares(node):
    """Declarations in the beginning of function

Contains: Var*

Examples:
    >>> print(mc.qscript("function d=f(); a=1; b.c='2'; d.e(1)=[4,5]"))
    _D f()
    {
      _B b ;
      _D d ;
      int a ;
      a = 1 ;
      b.c = "2" ;
      sword _d [] = {4, 5} ;
      d.e[0] = irowvec(_d, 2, false) ;
      return d ;
    }
    """

    if not node:
        return ""

    returns = node.parent[1]

    declares = {}   # {"int" : ["a", "b"]} -> int a, b ;
    structs = {}    # {"_A" : "a"} -> _A a;

    # fill declares and structs
    for child in node[:]:

        type = type_string(child)
        
        if type not in declares:
            declares[type] = []

        declares[type].append(child)

        if child.type == "structs":
            structs[child.name] = child

    # create output
    out = ""
    keys = declares.keys()
    keys.sort()
    for key in keys:
        val = declares[key]
        val.sort(cmp=lambda x,y: cmp(x.name, y.name))

        # datatype
        out += "\n" + key + " "

        # all variables with that type
        for v in val:

            out += str(v)
            if v.name in structs:

                structs_ = node.program[3]
                struct = structs_[structs_.names.index(v.name)]
                size = struct[struct.names.index("_size")].value
                out += "[%s]" % size

            out += ", "

        out = out[:-2] + " ;"

    return out[1:]


def Func(node):
    """Function declaration

Contains: Declares Returns Params Block
Property: name (of function)

Examples:
    >>> print(mc.qscript("function y=f(); y=1"))
    int f()
    {
      int y ;
      y = 1 ;
      return y ;
    }
    """


    # type information is in params and declare, not return
    retname = node[1][0].name
    if retname in node[0].names:
        retval = node[0][node[0].names.index(retname)]
    if retname in node[2].names:
        retval = node[2][node[1].names.index(retname)]
    rettype = type_string(retval)

    # empty code_block function with return statement
    if len(node[-1]) == 0:
        return rettype + """ %(name)s(%(2)s)
{
return %(1)s
}"""
    
    # function ends with a return statement
    if node[-1][-1] and node[-1][-1][-1].cls == "Return":
        return rettype + """ %(name)s(%(2)s)
{
%(0)s
%(3)s
}"""

    return rettype + """ %(name)s(%(2)s)
{
%(0)s
%(3)s
return %(1)s ;
}"""


def Main(node):
    """
Main function

Contains: Declares Returns Params Block
Property: name (of function)

Examples:
    >>> print(mc.qcpp("4"))
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    int main(int argc, char** argv)
    {
      4 ;
      return 0 ;
    }
    """

    # has variables to declare
    if node[0]:
        return """int main(int argc, char** argv)
{
%(0)s
%(3)s
return 0 ;
}"""
    return """int main(int argc, char** argv)
{
%(3)s
return 0 ;
}"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()
