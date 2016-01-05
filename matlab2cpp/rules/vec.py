from variables import *
import armadillo as arma

def Get(node):

    if len(node) != 1:

        if not len(node):
            node.error("Zero arguments in a vec call")
            return "%(name)s()"

        elif len(node) == 2 and node[1].cls == "Int" and node[1].value == "1":
            pass

        else:
            node.error("More than one arguments in a vec call")
            return "%(name)s(", "-1, ", "-1)"


    arg, dim = arma.configure_arg(node[0], 0)

    if dim == -1:
        return "%(name)s(%(0)s)"

    #if dim == 0:
    #    node.dim = 0

    return "%(name)s(" + arg + ")"

def Set(node):

    if len(node) != 1:

        if not len(node):
            node.error("Zero arguments in a vec call")
            return "%(name)s()"

        elif len(node) == 2 and node[1].cls == "Int" and node[1].value == "1":
            pass

        else:
            node.error("More than one arguments in a vec call")
            return "%(name)s(", "-1, ", "-1)"

    arg, dim = arma.configure_arg(node[0], 0)

    if dim == -1:
        return "%(name)s(%(0)s)"

    #if dim == 0:
    #    node.dim = 0

    return "%(name)s(" + arg + ")"
