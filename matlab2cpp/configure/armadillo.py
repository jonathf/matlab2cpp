import matlab2cpp.rules.armadillo as arma

def vec(node):
    if len(node) != 1:

        if not len(node):
            return

        elif len(node) == 2 and node[1].cls == "Int" and node[1].value == "1":
            pass

        else:
            return

    
    arg, dim = arma.configure_arg(node[0], 0)

    if dim == 0:
        node.dim = 0

def rowvec(node):
    if len(node) != 1:

        if not len(node):
            return

        elif len(node) == 2 and node[0].cls == "Int" and node[0].value == "1":
            node_ = node[1]

        else:
            return
    else:
        node_ = node[0]
        
    
    arg, dim = arma.configure_arg(node_, 0)

    if dim == 0:
        node.dim = 0

def mat(node):
    # Single argument
    if len(node) == 1:

        arg, dim = arma.configure_arg(node[0], 0)
        
        # scalar begets scalar
        if dim == 0:
            node.dim = 0

    # Double argument
    elif len(node) == 2:

        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)

        # unknown input
        if -1 in (dim0, dim1):
            return

        # Configure dimensions
        if dim0:
            if dim1:
                node.dim = 3#matrix
            else:
                node.dim = 1#colvec
        else:
            if dim1:
                node.dim = 2#rowvec
            else:
                node.dim = 0#scalar

def cube(node):
    # Single argument
    if len(node) == 1:

        arg, dim = arma.configure_arg(node[0], 0)

        # scalar input
        if dim == 0:
            node.dim = 0

    # Double argument
    elif len(node) == 2:

        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)

        # unkonwn input
        if -1 in (dim0, dim1):
            return

        # Configure dimensions
        if dim0:
            if dim1:
                node.dim = 3
            else:
                node.dim = 1
        else:
            if dim1:
                node.dim = 2
            else:
                node.dim = 0

    # Triple argument
    elif len(node) == 3:

        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)
        arg2, dim2 = arma.configure_arg(node[2], 2)

        # unknown arguments
        if -1 in (dim0, dim1, dim2):
            return

        # Configure dimensions
        if dim0:
            if dim1:
                if dim2:
                    node.dim = 4#cube
                else:
                    node.dim = 3#matrix
            else:
                if dim2:
                    node.dim = 3#matrix
                else:
                    node.dim = 1#colvec

        else:
            if dim1:
                if dim2:
                    node.dim = 3#matrix
                else:
                    node.dim = 1#colvec
            else:
                if dim2:
                    node.dim = 1#colvec
                else:
                    node.dim = 0#scalar
