from variables import *
from arma_common import Assign, configure_arg

def Get(node):

    if node[0].type == "TYPE":
        return "%(name)s(%(0)s)"

    arg, dim = configure_arg(node[0], 0)
    if dim == 0:
        node.dim = 0

    return "%(name)s(" + arg + ")"

def Set(node):

    if node[0].type == "TYPE":
        return "%(name)s(", ", ", ")"

    arg, dim = configure_arg(node[0], 0)
    if dim == 0:
        node.dim = 0

    return "%(name)s(" + arg + ")"
