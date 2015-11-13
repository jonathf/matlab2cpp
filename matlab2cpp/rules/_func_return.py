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
    Contains: Var, ...

Declares : Declarations in the beginning of function
    Contains: Var, ...
    Rule: func_return.py (if one variable return)
          func_returns.py (if multiple return)

Get : Function call
    Example: "y(4)"
    Contains: Gets
    Property: name

Var : Function call hidden as variable
    Example "y"
    Contains: nothing
    property: name
"""

import matlab2cpp as mc

from function import type_string
from variables import Get

def Var(node):
    """Function call as variable
    
Writing a function as if a variable, is equivalent to calling the function
without arguments.

Examples:
    >>> print mc.qscript("function y=f(); y=1; end; function g(); f")
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

def Params(node):
    """Parameters in functions with one return

Examples:
    >>> code = "function y(a,b,c,d,e)"
    >>> builder = mc.Builder()
    >>> builder.load("unamed", code)
    >>> builder[0].ftypes = {"y":{"a": "int", "b":"double", "c":"cx_mat",
    ...     "d":"func_lambda", "e":"struct", "f":"structs"}}
    >>> print mc.qscript(builder)
    void y(int a, double b, cx_mat c, std::function d, _E e)
    {
      // Empty block
    }
    """

    out = ""
    for child in node:
        out += ", " + type_string(child) + " " + str(child)
    return out[2:]


def Declares(node):

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

    # type is same as returned
    node.type = node[1][0].type

    # function ends with a return statement
    if node[-1][-1] and node[-1][-1][-1].cls == "Return":
        return """%(type)s %(name)s(%(2)s)
{
%(0)s
%(3)s
}"""

    return """%(type)s %(name)s(%(2)s)
{
%(0)s
%(3)s
return %(1)s ;
}"""


def Main(node):

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
