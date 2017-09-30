from .variables import *
from . import armadillo as arma

def Get(node):

    if len(node) != 1:

        if not len(node):
            node.error("Zero arguments in a vec call")
            return "%(name)s()"

        elif len(node) == 2 and node[1].cls == "Int" and node[1].value == "1":
            pass
        #special case hh = h0F(:,ones(1,M)) with h0F vec, and ones
        elif len(node) == 2 and node[0].name == "ones" or \
            node[1].name == "ones":
            out = "%(name)s("
            if node[0].name == "ones":
                out = out + "%(0)s-1, "
                #return "%(name)s(%(0)s-1, %(1)s)"
            else:
                out = out + "%(0)s, "
            if node[1].name == "ones":
                out = out + "%(1)s-1)"
                #return "%(name)s(%(0)s, %(1)s-1)"
            else:
                out = out + "%(1)s)"
            return out
            
        else:
            node.error("More than one arguments in a vec call")
            return "%(name)s(", ", ", ")"

    #if len(node) == 1:
    arg, dim = arma.configure_arg(node[0], 0)

    if dim == -1:
        return "%(name)s(", "-1, ", "-1)"

    #if dim == 0:
    #    node.dim = 0

    return "%(name)s(" + arg + ")"
    """
    elif len(node) == 2:
        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)

        if dim0 == -1:
            return "%(name)s(", "-1, ", "-1)"
        elif dim1 == -1:
            return "%(name)s(", "-1, ", "-1)"

        #if dim == 0:
        #    node.dim = 0

        return "%(name)s(" + arg0 + ", " + arg1 + ")"
    """ 

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
        return "%(name)s(", "-1, ", "-1)"

    #if dim == 0:
    #    node.dim = 0

    return "%(name)s(" + arg + ")"
