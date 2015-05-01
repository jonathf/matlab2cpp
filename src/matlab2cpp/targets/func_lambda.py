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

from variables import *
import func_return as fr

def Func(node):
#      return fr.Func(node)
    return ""#// placeholder for %(name)s"

def Lambda(node):

    lfunc = node.reference
    ldeclares, lreturns, lparams, lblock = lfunc
    lnames = lparams["names"] + ldeclares["names"]
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
            name = node_["name"]
            if name not in lnames:
                if name in params["names"]:
                    type = params[params["names"].index(name)].type
                    node_.type = type
                    node_.declare()

                elif name in declares["names"]:
                    type = declares[declares["names"].index(name)].type
                    node_.type = type
                    node_.declare()


    out = ""

    expr.generate()
    lfunc.generate()

    for declare in ldeclares:
        name = declare["name"]
        if name != "_retval":
            out += ", " + name
        else:
            node.type = declare.type

#      out = node["name"] + " = " + 
    out = "[" + out[2:] + "] "
    out += "(" + str(lparams) + ") {" + str(expr) + " ; }"
    return out


def Params(node):
    return ", ".join(["%s %s" % (n.type, n["name"]) for n in node])


def Returns(node):
    return ""

def Declares(node):
    return ", ".join(["%s %s" % (n.type, n["name"]) for n in node])


Declare = "std::function %(name)s ;"

def Var(node):
    return "%(name)s"

def Assign(node):
    return "%(0)s = %(1)s ;"

def Get(node):
    return "%(name)s(", ", ", ")"
