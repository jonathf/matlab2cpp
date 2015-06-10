
def configure_arg(node, index):
    """
Examples:
    >>> print mc.qtranslate('x=[1,2]; x(:)')
    int _x [] = {1, 2} ;
    x = ivec(_x, 2, false) ;
    x(span::all) ;
    >>> print mc.qtranslate('x=[1,2]; x(1)')
    int _x [] = {1, 2} ;
    x = ivec(_x, 2, false) ;
    x(0) ;
    >>> print mc.qtranslate('x=[1,2]; x([1,2])')
    int _x [] = {1, 2} ;
    x = ivec(_x, 2, false) ;
    uword __aux_uvec_1 [] = {1, 2} ;
    _aux_uvec_1 = uvec(__aux_uvec_1, 2, false) ;
    x(_aux_uvec_1-1) ;
    >>> print mc.qtranslate('x=[1,2]; x([1,2;2,1])')
    int _x [] = {1, 2} ;
    x = ivec(_x, 2, false) ;
    uword __aux_uvec_1 [] = {1, 2, 2, 1} ;
    _aux_uvec_1 = uvec(__aux_uvec_1, 4, false) ;
    x(_aux_uvec_1-1) ;
    >>> print mc.qtranslate("x=[1,2]; x(x')")
    int _x [] = {1, 2} ;
    x = ivec(_x, 2, false) ;
    x(arma::trans(arma::trans(x))-1) ;
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
        out = "vectorise(" + out + ")"

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


if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()
