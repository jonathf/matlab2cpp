from _variables import *
from _arma_common import configure_arg

def Get(node):

    if len(node) != 1:

        if not len(node):
            node.error("Zero arguments in a rowvec call")
            return "%(name)s(", ", ", ")"

        elif len(node) == 2 and node[0].cls == "Int" and node[0].value == "1":
            node_ = node[1]

        else:
            node.error("More than one arguments in a rowvec call")
            return "%(name)s(", ", ", ")"
    else:
        node_ = node[0]


    arg, dim = configure_arg(node_, 0)

    if dim == -1:
        return "%(name)s(", ", ", ")"

    if dim == 0:
        node.dim = 0

    return "%(name)s(" + arg + ")"


def Set(node):
    if len(node) != 1:

        if not len(node):
            node.error("Zero arguments in a rowvec call")
            return "%(name)s(", ", ", ")"

        elif len(node) == 2 and node[0].cls == "Int" and node[0].value == "1":
            node_ = node[1]

        else:
            node.error("More than one arguments in a rowvec call")
            return "%(name)s(", ", ", ")"
    else:
        node_ = node[0]


    arg, dim = configure_arg(node_, 0)

    if dim == 0:
        node.dim = 0

    if dim == -1:
        return "%(name)s(", ", ", ")"

    return "%(name)s(" + arg + ")"
