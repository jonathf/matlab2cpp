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

    if node[-1]:
        indices = ["%("+str(d)+")s" for d in xrange(len(node))]
        return "%(name)s(" + indices[-1] + ", " + ", ".join(indices[:-1]) + ") ;\n"
    else:
        indices = ["(%"+str(d)+")s" for d in xrange(len(node))]
        return "%(name)s(" + ", ".join(indices[:-1]) + ") ;\n"

