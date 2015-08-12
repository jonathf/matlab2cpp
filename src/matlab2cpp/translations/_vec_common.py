from _variables import *
from _arma_common import configure_arg

def Get(node):

    if len(node) != 1:

        if not len(node):
            node.error("Zero arguments in a vec call")
        else:
            node.error("More than one arguments in a vec call")

        return "%(name)s(", ", ", ")"


    arg, dim = configure_arg(node[0], 0)

    if dim == -1:
        return "%(name)s(%(0)s)"

    if dim == 0:
        node.dim = 0

    return "%(name)s(" + arg + ")"

def Set(node):

    if len(node) != 1:

        if not len(node):
            node.error("Zero arguments in a vec set")
        else:
            node.error("More than one arguments in a vec set")

        return "%(name)s(", ", ", ")"

    arg, dim = configure_arg(node[0], 0)

    if dim == -1:
        return "%(name)s(%(0)s)"

    if dim == 0:
        node.dim = 0

    return "%(name)s(" + arg + ")"
