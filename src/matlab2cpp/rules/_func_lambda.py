"""
Anonymous/Lambda Functions
"""

import matlab2cpp as mc

from .function import type_string
from .assign import Assign

def Get(node):
    """Function call of an lambda function

Contains: Expression*

Examples:
    >>> print(mc.qscript("x = 4; f = @() x; y = f()"))
    x = 4 ;
    f = [x] () {x ; } ;
    y = f() ;
    """
    return "%(name)s(", ", ", ")"

Var = "%(name)s"



def Lambda(node):
    """Lambda function statement

During construction, builder creates a full function for lambda expression.
These functions are available through node.reference.

Property: name (of function)

Examples:
    >>> print(mc.qscript("f = @() 4"))
    f = [] () {4 ; } ;
    """

    # lambda function are created as full functions, but referenced to be
    # written inline
    lfunc = node.reference
    ldeclares, lreturns, lparams, lblock = lfunc
    lnames = lparams.names + ldeclares.names
    expr = lblock[0][1]

    # location for where lambda is created
    func = node.func
    declares, returns, params, block = func

    out = ""

    # declare list in lambda function
    for declare in declares:
        if declare not in ldeclares:
            continue

        name = declare.name
        out += ", " + name

    # translate again where datatypes updated
    expr.translate()
    lfunc.translate()

    # return string
    out = "[" + out[2:] + "] "
    out += "(" + str(lparams) + ") {" + str(expr) + " ; }"
    return out

Returns = ""

def Params(node):
    """Parameter structure in lambda functions

Contains: Var*

Examples:
    >>> print(mc.qscript("f = @(x,y,z) x+y+z; f(1,2.,'3')"))
    f = [] (int x, double y, std::string z) {x+y+z ; } ;
    f(1, 2., "3") ;
    """
    return ", ".join(["%s %s" % (type_string(n), n.name) for n in node])

def Declares(node):
    """Variable scope in lambda function

If variables

Examples:
    >>> print(mc.qscript("x = 4; f = @() x+2"))
    x = 4 ;
    f = [x] () {x+2 ; } ;
    """

    # handle in Lambda
    return ""

# Actual lambda function is hidden
Func = ""

if __name__ == "__main__":
    import doctest
    doctest.testmod()
