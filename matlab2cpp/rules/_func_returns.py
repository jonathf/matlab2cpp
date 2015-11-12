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
from function import *

def Assigns(node):

    # existence of parameters in function call
    if node[-1]:
        params = [s.str for s in node[-1]]
        params = ", ".join(params) + ", "

    else:
        params = ""

    returns = [s.str for s in node[:-1]]
    returns = ", ".join(returns)

    return "%(name)s(" + params + returns + ") ;"
