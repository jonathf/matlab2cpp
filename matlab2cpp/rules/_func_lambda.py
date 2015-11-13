"""
Lambda Functions

Nodes
-----
Lambda : Function
    Contains: Returns, Params, Block
    Property: name

Func : Function
    Contains: Returns, Params, Block
    Property: name

Returns : Function return variables
    Contains: Var, ...

Params : Function parameter variables
    Contains: Var, ...

Declares : Declarations in the beginning of function
    Contains: Var, ...
    Rule: func_return.py (if one variable return)
          func_returns.py (if multiple return)

Get : Function/Array retrieval
    Example: "y(4)"
    Contains: Gets
    Property: name
"""

from function import *
from assign import Assign


def Lambda(node):

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

Declare = "std::function %(name)s ;"

