from .assign import Assign
from .variables import *
from . import armadillo as arma

Declare = "TYPE %(name)s ;"

def Assigns(node):
    lhs = map(str, node[:-1])
    lhs = "[" + ", ".join(lhs) + "]"
    rhs = str(node[-1])
    return lhs + " = " + rhs + " ;"

def Matrix(node):
    return "", ", ", ""

def Get(node):

    if len(node) == 2:
        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)

        # All + All
        if node[0].cls == node[1].cls == "All":
            return "%(name)s"

        # All + ...
        if node[0].cls == "All":
            # All + uvec
            if dim1:
                return "%(name)s.cols(" + arg1 + ")"
            # All + scalar
            return "%(name)s.col(" + arg1 + ")"

        # ... + All
        elif node[1].cls == "All":
            # uvec + All
            if dim0:
                return "%(name)s.rows(" + arg0 + ")"
            # scalar + All
            return "%(name)s.row(" + arg0 + ")"

    return "%(name)s(", ", ", ")"

def Set(node):
    node.error("unknown data type")

    # Double argument
    if len(node) == 2:

        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)

        # All + All
        if node[0].cls == node[1].cls == "All":
            return "%(name)s"

        # All + ...
        if node[0].cls == "All":
            # All + uvec
            if dim1:
                return "%(name)s.cols(" + arg1 + ")"
            # All + scalar
            return "%(name)s.col(" + arg1 + ")"

        # ... + All
        elif node[1].cls == "All":
            # uvec + All
            if dim0:
                return "%(name)s.rows(" + arg0 + ")"
            # scalar + All
            return "%(name)s.row(" + arg0 + ")"

        # scalar + uvec
        if dim0 == 0 and dim1 > 0:
            #arg0 = "m2cpp::asuvec(" + arg0 + ")"
            return "%(name)s.col(" + arg0 + ").rows(" + arg1 + ")"

        # uvec + scalar
        elif dim0 > 0 and dim1 == 0:
            #arg1 = "m2cpp::asuvec(" + arg1 + ")"
            return "%(name)s.row(" + arg0 + ").cols(" + arg1 + ")"

        return "%(name)s(" + arg0 + ", " + arg1 + ")"

    return "%(name)s(", ", ", ")"
