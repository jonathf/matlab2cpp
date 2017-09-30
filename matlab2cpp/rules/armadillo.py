"""
filler for Armadillo
"""

import matlab2cpp as mc

def configure_arg(node, index):
    """
Configure an argument of an vector, matrix or cube.

Args:
    node (Get, Set): Current possition in node-tree
    index (int): argument index (starting from 0)

Returns:
    tuple: A string representation of argument and an index (-1,0,1) indicating
    if the argument was unknown, scalar or a vector, respectively.

Examples:
    >>> print(mc.qscript('x=[1,2]; x(:)'))
    sword _x [] = {1, 2} ;
    x = irowvec(_x, 2, false) ;
    x(span(0, x.n_rows-1)) ;
    >>> print(mc.qscript('x=[1,2]; x(1)'))
    sword _x [] = {1, 2} ;
    x = irowvec(_x, 2, false) ;
    x(0) ;
    >>> print(mc.qscript('x=[1,2]; x([1,2])'))
    sword _x [] = {1, 2} ;
    x = irowvec(_x, 2, false) ;
    uword __aux_urowvec_1 [] = {1, 2} ;
    _aux_urowvec_1 = urowvec(__aux_urowvec_1, 2, false) ;
    x(arma::strans(_aux_urowvec_1)-1) ;
    >>> print(mc.qscript('x=[1,2]; x([1,2;2,1])'))
    sword _x [] = {1, 2} ;
    x = irowvec(_x, 2, false) ;
    uword __aux_umat_1 [] = {1, 2, 2, 1} ;
    _aux_umat_1 = arma::strans(umat(__aux_umat_1, 2, 2, false)) ;
    x(_aux_umat_1-1) ;
    >>> print(mc.qscript("x=[1,2]; x(x')"))
    sword _x [] = {1, 2} ;
    x = irowvec(_x, 2, false) ;
    x(arma::trans(x)-1) ;
    """

    out = "%(" + str(index) + ")s"

    # the full range ':'
    if node.cls == "All":

        arg = node.parent.name

        # first axis
        if index == 0:

            # axis and dim does not match for colvec and rowvec
            if node.parent.dim == 1:
                arg += ".n_cols"
            else:
                arg += ".n_rows"

        # second axis
        elif index == 1:
            arg += ".n_cols"

        # third axis
        elif index == 2:
            arg += ".n_slices"

        return "span(0, " + arg + "-1)", 1

    # undefined type
    elif node.type == "TYPE":
        return out, -1

    # float point scalar
    elif node.mem > 1 and node.dim == 0:
        out = "(uword) " + out

    #Float or double, vec or rowvec
        """
    elif node.mem not in (0, 4) and node.dim in (1, 2):
        out = "arma::conv_to<uvec>::from(" + out + ")"
        """
    # rowvec (-> colvec)
    elif node.dim == 2:
        out = "arma::strans(" + out + ")"

    # scalar done verbatim
    if node.dim == 0:
        if node.cls == "Int":
            out = str(int(node.value)-1)
        elif node.cls == "Float":
            out = str(float(node.value)-1)
        else:
            out = out + "-1"
        dim = 0

    # matrices and cubes 
    elif node.dim > 2:
        dim = node.dim
        out = out + "-1"

    else:
        dim = 1

        if len(node) > 0 and node[0].cls == "Paren":
            pass
        elif node.cls not in ["Colon", "Paren"]:
            out = out + "-1"

    return out, dim


def scalar_assign(node):
    """
convert scalar to various array types
    """

    # left-hand-side and right-hand-side
    lhs, rhs = node

    if lhs.mem < rhs.mem:
        node.warning("Type reduction from %s to %s" % (rhs.type, lhs.type))

    # matrix suround are ignored
    if rhs.cls == "Matrix":
        rhs = str(rhs[0][0])

    else:
        rhs = "%(1)s"

    if lhs.cls == "Set":
        return "%(0)s.fill(" + rhs + ") ;"

    #Earlier stuff, replaced with code right above
    """
    if lhs.dim == 0:
        pass

    # as colvec
    elif lhs.dim == 1:
        node.include("m2cpp")
        rhs = "m2cpp::scol(" + rhs + ")"

    # as rowvec
    elif lhs.dim == 2:
        node.include("m2cpp")
        rhs = "m2cpp::srow(" + rhs + ")"

    # as matrix
    elif lhs.dim == 3:
        node.include("m2cpp")
        rhs = "m2cpp::smat(" + rhs + ")"

    # as cube
    elif lhs.dim == 4:
        #scube is not implemented in mconvert.h, namespace m2cpp at the moment
        node.include("m2cpp")
        rhs = "m2cpp::scube(" + rhs + ")"
    """
    
    return "%(0)s = " + rhs + " ;"


def include(node):
    """Add armadillo to header"""

    program = node.program
    includes = program[0]

    arma = "#include <armadillo>"
    namespace = "using namespace arma ;"

    if arma in includes and namespace in includes:
        return

    if arma not in includes:
        include = mc.collection.Include(includes, arma, value=includes.value)
        include.backend = "program"

    if namespace not in includes:
        include = mc.collection.Include(includes, namespace, value=includes.value)
        include.backend = "program"

    includes.translate()



if __name__ == "__main__":
    import doctest
    doctest.testmod()
