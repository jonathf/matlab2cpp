"""
Functions with multiple returns

Nodes
-----
Func : Function
    Contains: Declares, Returns, Params, Block
    Property: name

Returns : Function return variables
    Contains: Var, ...

Params : Function parameter variables
    Contains: Var, ...

Get : Function/Array retrieval
    Example: "y(4)"
    Contains: Gets
    Property: name
"""
from _func_common import *


def Assigns(node):

    assigness = str(node[0])
    name = node["name"]
    if node[1]:
        args = str(node[1])
        return name + "("+assigness+", "+args+") ;\n"
    return name + "("+assigness+") ;\n"
