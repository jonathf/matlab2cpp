from variables import *
from arma_common import configure_arg

def Get(node):

    # Single argument
    if len(node) == 1:

        arg, dim = configure_arg(node[0], 0)
        if dim == -1:
            return "%(name)s(%(0)s)"

        if dim == 0:
            node.dim = 0

        return "vectorise(%(name)s)(" + arg + ")"


    # Double argument
    elif len(node) == 2:

        arg0, dim0 = configure_arg(node[0], 0)
        arg1, dim1 = configure_arg(node[1], 1)

        if -1 in (dim0, dim1):
            return "%(name)s(", ", ", ")"

        # Configure dimensions
        if dim0:
            if dim1:
                node.dim = 3
            else:
                node.dim = 1
                arg1 = "span("+arg1+")"
        else:
            if dim1:
                node.dim = 2
                arg0 = "span("+arg0+")"
            else:
                node.dim = 0

        node.resize()
        return "_%(name)s(" + arg0 + ", " + arg1 + ")"

    elif len(node) == 3:

        arg0, dim0 = configure_arg(node[0], 0)
        arg1, dim1 = configure_arg(node[1], 1)
        arg2, dim2 = configure_arg(node[2], 2)

        if -1 in (dim0, dim1, dim2):
            return "%(name)s(", ", ", ")"

        # Configure dimensions
        if dim0:
            if dim1:
                if dim2:
                    node.dim = 4
                else:
                    node.dim = 3
                    arg2 = "span("+arg2+")"
            else:
                if dim2:
                    node.dim = 3
                    arg1 = "span("+arg1+")"
                else:
                    node.dim = 1
                    arg1 = "span("+arg1+")"
                    arg2 = "span("+arg2+")"

        else:
            if dim1:
                if dim2:
                    node.dim = 3
                    arg0 = "span("+arg0+")"
                else:
                    node.dim = 1
                    arg0 = "span("+arg0+")"
                    arg2 = "span("+arg2+")"
            else:
                if dim2:
                    node.dim = 1
                    arg0 = "span("+arg0+")"
                    arg1 = "span("+arg1+")"
                else:
                    node.dim = 0

        return "%(name)s(" + arg0 + ", " + arg1 + ", " + arg2 + ")"


def Set(node):

    # Single argument
    if len(node) == 1:

        arg, dim = configure_arg(node[0], 0)

        if dim == -1:
            return "%(name)s(%(0)s)"

        if dim == 0:
            node.dim = 0

        return "vectorise(%(name)s)(" + arg + ")"


    # Double argument
    elif len(node) == 2:

        arg0, dim0 = configure_arg(node[0], 0)
        arg1, dim1 = configure_arg(node[1], 1)

        if -1 in (dim0, dim1):
            return "%(name)s(", ", ", ")"
        node = node.resize()

        # Configure dimensions
        if dim0:
            if dim1:
                node.dim = 3
            else:
                node.dim = 1
                arg1 = "span("+arg1+")"
        else:
            if dim1:
                node.dim = 2
                arg0 = "span("+arg0+")"
            else:
                node.dim = 0

        return "%(name)s(" + arg0 + ", " + arg1 + ", 1)"

    elif len(node) == 3:

        arg0, dim0 = configure_arg(node[0], 0)
        arg1, dim1 = configure_arg(node[1], 1)
        arg2, dim2 = configure_arg(node[2], 2)

        if -1 in (dim0, dim1, dim2):
            return "%(name)s(", ", ", ")"

        # Configure dimensions
        if dim0:
            if dim1:
                if dim2:
                    node.dim = 4
                else:
                    node.dim = 3
                    arg2 = "span("+arg2+")"
            else:
                if dim2:
                    node.dim = 3
                    arg1 = "span("+arg1+")"
                else:
                    node.dim = 1
                    arg1 = "span("+arg1+")"
                    arg2 = "span("+arg2+")"

        else:
            if dim1:
                if dim2:
                    node.dim = 3
                    arg0 = "span("+arg0+")"
                else:
                    node.dim = 1
                    arg0 = "span("+arg0+")"
                    arg2 = "span("+arg2+")"
            else:
                if dim2:
                    node.dim = 1
                    arg0 = "span("+arg0+")"
                    arg1 = "span("+arg1+")"
                else:
                    node.dim = 0

        return "%(name)s(" + arg0 + ", " + arg1 + ", " + arg2 + ")"


def Resize(node):
    return "%(type)s_%(name)s(%(name)s.memptr(), %(name)s.n_rows, " +\
            "%(name)s.n_cols*%(name)s.n_slices, false) ;"
