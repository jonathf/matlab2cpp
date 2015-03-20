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

    program = node.program
    func = program[program["names"].index(node["name"])]
    declares, returns, params, block = func
    expr = block[0][1]

    out = ""

    # Hack: add more declared variables
    nodes = [expr]
    for node in nodes:
        nodes.extend(node.children)
        if node["class"] in ["Get", "Get2", "Get3"] and\
                node["name"] not in params["names"]+declares["names"]:
            node.declare()

    for name, declare in zip(declares["names"], declares):
        if name != "_retval":
            out += ", " + name
        else:
            node.type(declare.type())

    print out
    out = "[" + out[2:]
    out += "] (" + str(params)
    out += ") {" + str(expr) + " ; }"
    return out


def Params(node):

    return ", ".join(["%s %s" % (n.type(), n["name"]) for n in node])


def Returns(node):

    return ""

def Declares(node):

    return ", ".join(["%s" % (n["name"]) for n in node])
