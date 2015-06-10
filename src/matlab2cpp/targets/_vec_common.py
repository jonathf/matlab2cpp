from _variables import *
from _arma_common import configure_arg

def Get(node):

    arg, dim = configure_arg(node[0], 0)

    if dim == -1:
        return "%(name)s(%(0)s)"

    if dim == 0:
        node.dim = 0

    return "%(name)s(" + arg + ")"

def Set(node):

    arg, dim = configure_arg(node[0], 0)

    if dim == -1:
        return "%(name)s(%(0)s)"

    if dim == 0:
        node.dim = 0

    return "%(name)s(" + arg + ")"
