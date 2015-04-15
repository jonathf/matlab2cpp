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

def Func(node):
    return ""#// placeholder for %(name)s"

def Lambda(node):

    lfunc = node.reference.reference
    ldeclares, lreturns, lparams, lblock = lfunc
    expr = lblock[0][1]

    func = node.func
    declares, returns, params, block = func

    # Lambda is creates a local scope
    # e.g. in expressions like '@(x) x*y'
    # 'x' is in one scope and 'y' is in another.
    # This little hack iterates the expression of the function in
    # search for vars/calls etc. like 'y' and declares them with
    # the right types.
    nodes = [expr]
    for node_ in nodes:
        nodes.extend(node_.children) 

        if node_["class"] in ["Var", "Get", "Get2", "Get3"]:
            name = node_["name"]
            lnames =lparams["names"] + ldeclares["names"]
            if name not in lnames:
                if name in params["names"]:
                    type = params[params["names"].index(name)].type()
                    node_.type(type)
                    node_.declare()

                elif name in declares["names"]:
                    type = declares[declares["names"].index(name)].type()
                    node_.type(type)
                    node_.declare()


    out = ""

    for declare in ldeclares:
        name = declare["name"]
        if name != "_retval":
            out += ", " + name
        else:
            node.type(declare.type())

    out = node["name"] + " = " + "[" + out[2:] + "] "
    out += "(" + str(lparams) + ") {" + str(expr) + " ; }"
    return out


def Params(node):

    return ", ".join(["%s %s" % (n.type(), n["name"]) for n in node])


def Returns(node):

    return ""

def Declares(node):

    return ", ".join(["%s" % (n["name"]) for n in node])


Declare = "std::function %(name)s ;"

def Var(node):
    return "%(name)s"

def Assign(node):
    return "%(0)s = %(1)s ;"

def Get(node):
    return "%(name)s(", ", ", ")"
