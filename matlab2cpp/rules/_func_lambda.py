"""
Anonymous/Lambda Functions
"""

import matlab2cpp as mc
from function import type_string
from variables import *
from assign import Assign


def Lambda(node):
    """Lambda function statement

During construction, builder creates a full function for lambda expression.
These functions are available through node.reference.

Property: name (of function)

Examples:
    >>> print mc.qscript("f = @() 4")
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

    # Lambda creates a local scope
    # e.g. in expressions like '@(x) x*y'
    # 'x' is in one scope and 'y' is in another.
    # This little hack iterates the expression of the function in
    # search for vars/calls etc. like 'y' and declares them with
    # the right types.
    nodes = [expr]
    for node_ in nodes:
        nodes.extend(node_[:])

        # a variable
        if node_.cls in ["Var", "Cvar", "Fvar",
                "Get", "Cget", "Fget", "Nget"]:
            name = node_.name

            # not in lambda scope
            if name not in lnames:

                # defined as a parameter in function
                if name in params.names:
                    type = params[params.names.index(name)].type
                    node_.type = type
                    node_.declare.type = type

                # declared in function
                elif name in declares.names:
                    type = declares[declares.names.index(name)].type
                    node_.type = type
                    node_.declare.type = type


    out = ""

    # declare list in lambda function
    for declare in declares:
        if declare not in ldeclares:
            continue

        name = declare.name
        if name != "_retval":
            out += ", " + name
        else:
            node.type = declare.type

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
    >>> print mc.qscript("f = @(x,y,z) x+y+z; f(1,2.,'3')")
    f = [] (int x, double y, string z) {x+y+z ; } ;
    f(1, 2., "3") ;
    """
    return ", ".join(["%s %s" % (type_string(n), n.name) for n in node])

def Declares(node):
    """Variable scope in lambda function

If variables

Examples:
    >>> print mc.qscript("x = 4; f = @() x+2")
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
