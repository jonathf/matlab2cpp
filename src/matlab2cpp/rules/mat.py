from . import armadillo as arma

def Get(node):
    """
    Statement
        Get (a)

    a()

    Assign
        Var (b)
        Get (a)

    b = a()
    """

    # number of args not correct
    if len(node) not in (1,2):

        if not len(node):
            node.error("Zero arguments in a matrix call")
        else:
            node.error("More than two arguments in a matrix call")

        return "%(name)s(", "-1, ", "-1)"

    # Single argument
    if len(node) == 1:

        arg, dim = arma.configure_arg(node[0], 0)

        # unknown input
        if dim == -1:
            return "%(name)s(%(0)s-1)"

        # scalar begets scalar
        #if dim == 0:
        #    node.dim = 0

        return "%(name)s(" + arg + ")"

    # Double argument
    elif len(node) == 2:

        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)

        # unknown input
        if -1 in (dim0, dim1):
            return "%(name)s(", "-1, ", "-1)"

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

            index = node[1].str.index('(')
            return "%(name)s(m2cpp::span<uvec>(" + arg0 + ", " + arg0 + ")" + ", " \
                   + "m2cpp::span<uvec>" + node[1].str[index:] + ")"
            #return "%(name)s.col(" + arg0 + ").rows(" + arg1 + ")"


        # uvec + scalar
        elif dim0 > 0 and dim1 == 0:
            return "%(name)s(" + arg0 + ", m2cpp::span<uvec>(" + arg1 + ", " + arg1 + "))"
            #index = node[0].str.index('(')
            #return "%(name)s(" + "m2cpp::span<uvec>" + node[0].str[index:] + ", m2cpp::span<uvec>(" + arg1 + ", " + arg1 + "))"
            #return "%(name)s.row(" + arg0 + ").cols(" + arg1 + ")"

        # uvec + uvec
        if dim0 > 0 and dim1 > 0:
            a0 = node[0].str.replace("arma::span", "m2cpp::span<uvec>")
            a1 = node[1].str.replace("arma::span", "m2cpp::span<uvec>")

            return "%(name)s(" + a0 + ", " + a1 + ")"

        return "%(name)s(" + arg0 + ", " + arg1 + ")"


def Set(node):
    """
    Assign
        Set (a)
            Var (n)
        Var (b)

    a(n) = b
    """

    # wrong number of argumets
    if len(node) not in (1,2):

        if not len(node):
            node.error("Zero arguments in a matrix set")
        else:
            node.error("More than two arguments in a matrix set")

        return "%(name)s(", "-1, ", "-1)"

    # Single argument
    if len(node) == 1:

        arg, dim = arma.configure_arg(node[0], 0)

        # scalar arg is scalar
        #if dim == 0:
        #    node.dim = 0

        # unknown datatype
        if dim == -1:
            return "%(name)s(", "-1, ", "-1)"

        return "%(name)s(" + arg + ")"


    # Double argument
    elif len(node) == 2:

        arg0, dim0 = arma.configure_arg(node[0], 0)
        arg1, dim1 = arma.configure_arg(node[1], 1)

        # unknown datatype
        if -1 in (dim0, dim1):
            return "%(name)s(", "-1, ", "-1)"

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
            index = node[1].str.index('(')
            return "%(name)s(m2cpp::span<uvec>(" + arg0 + ", " + arg0 + ")" + ", " \
                   + "m2cpp::span<uvec>" + node[1].str[index:] + ")"
            #return "%(name)s.col(" + arg0 + ").rows(" + arg1 + ")"


        # uvec + scalar
        elif dim0 > 0 and dim1 == 0:
            index = node[0].str.index('(')
            return "%(name)s(" + "m2cpp::span<uvec>" + node[0].str[index:] + \
                   ", m2cpp::span<uvec>(" + arg1 + ", " + arg1 + "))"
            #return "%(name)s.row(" + arg0 + ").cols(" + arg1 + ")"

        # uvec + uvec
        if dim0 > 0 and dim1 > 0:
            a0 = node[0].str.replace("arma::span", "m2cpp::span<uvec>")
            a1 = node[1].str.replace("arma::span", "m2cpp::span<uvec>")

            return "%(name)s(" + a0 + ", " + a1 + ")"

        return "%(name)s(" + arg0 + ", " + arg1 + ")"

