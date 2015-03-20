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

# Requires C++11
INLINE_MODE = True

def Func(node):
    if INLINE_MODE:
        return ""#// placeholder for %(name)s"

def Lambda(node):

    if INLINE_MODE:

        program = node.program
        func = program[program["names"].index(node["name"])+1]
        declares, returns, params, block = func
        expr = block[0][1]

        return "[" + str(declares) + "] (" + str(params) +\
                ") {" + str(expr) + "; }"


def Params(node):

    if INLINE_MODE:
        return ", ".join(["%s %s" % (n.type(), n["name"]) for n in node])


def Returns(node):

    if INLINE_MODE:
        return ""

def Declares(node):

    if INLINE_MODE:
        return ", ".join(["%s" % (n["name"]) for n in node])
