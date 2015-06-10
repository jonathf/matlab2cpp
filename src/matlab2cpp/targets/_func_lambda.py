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

from _func_common import *
from _assign_common import Assign as A


def Lambda(node):

    lfunc = node.reference
    ldeclares, lreturns, lparams, lblock = lfunc
    lnames = lparams.names + ldeclares.names
    expr = lblock[0][1]

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

        if node_["class"] in ["Var", "Cvar", "Fvar",
                "Get", "Cget", "Fget", "Nget"]:
            name = node_.name
            if name not in lnames:
                if name in params.names:
                    type = params[params.names.index(name)].type
                    node_.type = type
                    node_.declare.type = type

                elif name in declares.names:
                    type = declares[declares.names.index(name)].type
                    node_.type = type
                    node_.declare.type = type


    out = ""

    for declare in declares:
        if declare not in ldeclares:
            continue

        name = declare.name
        if name != "_retval":
            out += ", " + name
        else:
            node.type = declare.type

    expr.translate_tree()
    lfunc.translate_tree()

    out = "[" + out[2:] + "] "
    out += "(" + str(lparams) + ") {" + str(expr) + " ; }"
    return out

Declare = "std::function %(name)s ;"

