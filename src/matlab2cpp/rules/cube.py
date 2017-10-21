from .variables import *
from . import armadillo as arma

def Get(node):

    # number of argument not legal for cube
    if len(node) not in (1,2,3):

        if not len(node):
            node.error("Zero arguments in a cube call")
        else:
            node.error("More than three arguments in a cube call")

        return "%(name)s(", "-1, ", "-1)"


    # Single argument
    if len(node) == 1:

        arg, dim = arma.configure_arg(node[0], 0)

        # unknown input
        if dim == -1:
            return "%(name)s(%(0)s-1)"

        # scalar input
        #if dim == 0:
        #    node.dim = 0

        return "%(name)s(" + arg + ")"


    # Double argument
    elif len(node) == 2:

        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)

        # unkonwn input
        if -1 in (dim0, dim1):
            return "%(name)s(", "-1, ", "-1)"

        # Configure dimensions
        #if dim0:
        #    if dim1:
        #        node.dim = 3
        #    else:
        #        node.dim = 1
        #else:
        #    if dim1:
        #        node.dim = 2
        #    else:
        #        node.dim = 0

        node = node.resize() # matlab to armadillo fix for cubes

        return "_%(name)s(" + arg0 + ", " + arg1 + ")"

    # Triple argument
    elif len(node) == 3:

        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)
        arg2, dim2 = arma.configure_arg(node[2], 2)

        # unknown arguments
        if -1 in (dim0, dim1, dim2):
            return "%(name)s(", "-1, ", "-1)"

        # Configure dimensions
        #if dim0:
        #    if dim1:
        #        if dim2:
        #            node.dim = 4#cube
        #        else:
        #            node.dim = 3#matrix
        #    else:
        #        if dim2:
        #            node.dim = 3#matrix
        #        else:
        #            node.dim = 1#colvec
        
        #else:
        #    if dim1:
        #        if dim2:
        #            node.dim = 3#matrix
        #        else:
        #            node.dim = 1#colvec
        #    else:
        #        if dim2:
        #            node.dim = 1#colvec
        #        else:
        #            node.dim = 0#scalar
        
        return "%(name)s(" + arg0 + ", " + arg1 + ", " + arg2 + ")"


def Set(node):

    if len(node) not in (1,2,3):

        if not len(node):
            node.error("Zero arguments in a cube set")
        else:
            node.error("More than three arguments in a cube set")

        return "%(name)s(", "-1, ", "-1)"

    # Single argument
    if len(node) == 1:

        arg, dim = arma.configure_arg(node[0], 0)

        # unknown arguments
        if dim == -1:
            return "%(name)s(%(0)s-1)"

        # if scalar arg, set node as scalar
        #if dim == 0:
        #    node.dim = 0

        return "%(name)s(" + arg + ")"


    # Double argument
    elif len(node) == 2:

        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)

        # unknown args
        if -1 in (dim0, dim1):
            return "%(name)s(", "-1, ", "-1)"

        node = node.resize() # matlab to armadillo fix for cubes

        # Configure dimensions
        #if dim0:
        #    if dim1:
        #        node.dim = 3#matrix
        #    else:
        #        node.dim = 1#colvec
        #else:
        #    if dim1:
        #        node.dim = 2#rowvec
        #    else:
        #        node.dim = 0#scalar
        
        return "%(name)s(" + arg0 + ", " + arg1 + ", 1)"

    # triple argument
    elif len(node) == 3:

        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)
        arg2, dim2 = arma.configure_arg(node[2], 2)

        # unkown input
        if -1 in (dim0, dim1, dim2):
            return "%(name)s(", ", ", ")"

        # Configure dimensions
        #if dim0:
        #    if dim1:
        #        if dim2:
        #            node.dim = 4#cube
        #        else:
        #            node.dim = 3#matrix
        #    else:
        #        if dim2:
        #            node.dim = 3#matrix
        #        else:
        #            node.dim = 1#colvec
        
        #else:
        #    if dim1:
        #        if dim2:
        #            node.dim = 3#matrix
        #        else:
        #            node.dim = 1#colvec
        #    else:
        #        if dim2:
        #            node.dim = 1#colvec
        #        else:
        #            node.dim = 0#scaler
        
        return "%(name)s(" + arg0 + ", " + arg1 + ", " + arg2 + ")"


def Resize(node):
    """Special resizing of cube such that properly tranlsation between matlab
    and armadillo."""

    return "%(type)s_%(name)s(%(name)s.memptr(), %(name)s.n_rows, " +\
            "%(name)s.n_cols*%(name)s.n_slices, false) ;"
