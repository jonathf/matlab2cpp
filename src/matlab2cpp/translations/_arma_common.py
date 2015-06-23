
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
    >>> print mc.qtranslate('x=[1,2]; x(:)')
    int _x [] = {1, 2} ;
    x = irowvec(_x, 2, false) ;
    x(span::all) ;
    >>> print mc.qtranslate('x=[1,2]; x(1)')
    int _x [] = {1, 2} ;
    x = irowvec(_x, 2, false) ;
    x(0) ;
    >>> print mc.qtranslate('x=[1,2]; x([1,2])')
    int _x [] = {1, 2} ;
    x = irowvec(_x, 2, false) ;
    uword __aux_urowvec_1 [] = {1, 2} ;
    _aux_uvec_1 = urowvec(__aux_uvec_1, 2, false) ;
    x(_aux_uvec_1-1) ;
    >>> print mc.qtranslate('x=[1,2]; x([1,2;2,1])')
    int _x [] = {1, 2} ;
    x = irowvec(_x, 2, false) ;
    int __aux_imat_1 [] = {1, 2, 2, 1} ;
    _aux_imat_1 = imat(__aux_imat_1, 2, 2, false) ;
    x(_aux_imat_1-1) ;
    >>> print mc.qtranslate("x=[1,2]; x(x')")
    int _x [] = {1, 2} ;
    x = irowvec(_x, 2, false) ;
    x(arma::trans(x)-1) ;
    """

    out = "%(" + str(index) + ")s"

    if node.cls == "All":
        return "span::all", 1
    elif node.type == "TYPE":
        return out, -1

    if node.mem > 1 and node.dim == 0:
        out = "(uword) " + out

    if node.dim == 2:
        out = "arma::trans(" + out + ")"

    elif node.dim > 2:
        # TODO: multi-index arguments through snippits
        # out = "vectorise(" + out + ")"
        pass

    if node.dim == 0:
        if node.cls in ("Int", "Float"):
            out = str(int(node.value)-1)
        else:
            out = out + "-1"
        dim = 0
    else:
        dim = 1
        if node.cls != "Colon":
            out = out + "-1"

    return out, dim

def scalar_assign(node):
    lhs, rhs = node

    if lhs.mem < rhs.mem:
        node.warning("Type reduction from %s to %s" % (rhs.type, lhs.type))

    if rhs.cls == "Matrix":
        rhs = str(rhs[0][0])
    else:
        rhs = "%(1)s"

    if lhs.dim == 0:
        pass
    elif lhs.dim == 1:
        node.include("scol")
        rhs = "m2cpp::scol(" + rhs + ")"
    elif lhs.dim == 2:
        node.include("srow")
        rhs = "m2cpp::srow(" + rhs + ")"
    elif lhs.dim == 3:
        node.include("smat")
        rhs = "m2cpp::smat(" + rhs + ")"
    elif lhs.dim == 4:
        node.include("scube")
        rhs = "m2cpp::scube(" + rhs + ")"
    return "%(0)s = " + rhs + " ;"


if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()
