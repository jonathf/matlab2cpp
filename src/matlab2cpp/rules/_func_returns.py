"""
Functions with multiple returns
"""

import matlab2cpp as mc
from .function import type_string
from .variables import Get


def Func(node):
    """Function declaration

Contains: Declares Returns Params Block
Property: name (of function)

Examples:
    >>> print(mc.qscript("function f()"))
    void f()
    {
      // Empty block
    }
    """

    if len(node[1]) and len(node[2]):
        if len(node[0])>len(node[1]):
            return """void %(name)s(%(2)s, %(1)s)
{
%(0)s
%(3)s
}"""
        return """void %(name)s(%(2)s, %(1)s)
{
%(3)s
}"""

    # one of returns or params are missing
    if len(node[0])>len(node[1]):
        return """void %(name)s(%(2)s%(1)s)
{
%(0)s
%(3)s
}"""
    return """void %(name)s(%(2)s%(1)s)
{
%(3)s
}"""



def Var(node):
    """Function call as variable
    
Writing a function as if a variable, is equivalent to calling the function
without arguments.

Property: name (of variable)

Examples:
    >>> print(mc.qscript("function f(); end; function g(); f"))
    void f()
    {
      // Empty block
    }
    <BLANKLINE>
    void g()
    {
      f() ;
    }
"""
    # push the job over to Get
    return Get(node)

def Assign(node):
    """The function have multiple returns, but only one lhs return.

    """
    return Assigns(node)

def Assigns(node):
    """Assignment where rhs is a function call and lhs are multiple returns.

Concatinates return variables after the parameters, if any.

Property: name (of function)
Contains: Expression Expression+ Get

Examples:
    >>> print(mc.qscript('''function [a,b]=f(c,d); a=c; b=d)
    ...     function g(); [a,b] = f(1,2.)''')
    void f(int c, double d, int& a, double& b)
    {
      a = c ;
      b = d ;
    }
    <BLANKLINE>
    void g()
    {
      double b ;
      int a ;
      f(1, 2., a, b) ;
    }
    """

    # existence of parameters in function call
    if node[-1]:
        params = [s.str for s in node[-1]]
        params = ", ".join(params) + ", "

    else:
        params = ""

    returns = [s.str for s in node[:-1]]
    returns = ", ".join(returns)

    return "%(name)s(" + params + returns + ") ;"

def Returns(node):
    """Return value in function definition with zero or multiple returns

Adds type prefix and '&' (since they are to be placed in parameters)

Contains: Return*

Examples:
    >>> print(mc.qscript("function [a,b]=f(); a=1, b=2."))
    void f(int& a, double& b)
    {
      a = 1 ;
      b = 2. ;
    }
    """

    out = ""
    for child in node[:]:
        out += ", " + type_string(child) + "& " + str(child)
    return out[2:]


def Params(node):
    """Parameters in function definition with zero or multiple returns

Adds type prefix.

Contains: Var*

Examples:
    >>> ftypes = {"f": {"a":"int", "b":"double"}}
    >>> print(mc.qscript("function f(a,b)", ftypes=ftypes))
    void f(int a, double b)
    {
      // Empty block
    }
    """

    # Create list of parameters
    out = ""

    # if -ref, -reference flag option
    if node.project.builder.reference:

        out += ", ".join(["const " + type_string(child) + "& " + child.name if child.dim > 0 else
                           type_string(child) + " " + child.name for child in node])

        return out

    else:
        out = ", ".join([type_string(child) + " " + child.name for child in node])

    return out


def Declares(node):
    """Variables declared on the top of the function

Contains: Declare*

Examples:
    >>> print(mc.qscript("function f(); a=1; b.c='2'; d.e(1)=[4,5]"))
    void f()
    {
      _B b ;
      _D d ;
      int a ;
      a = 1 ;
      b.c = "2" ;
      sword _d [] = {4, 5} ;
      d.e[0] = irowvec(_d, 2, false) ;
    }
    """

    # nothing to declare
    if not node:
        return ""

    returns = node.parent[1]

    declares = {}   # {"int" : ["a", "b"]} -> int a, b ;
    structs = {}    # {"_A" : "a"} -> _A a;

    # fill declares and structs
    for child in node[:]:

        # return values in multi-returns are declared as parameter
        if child.name in returns:
            continue

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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
