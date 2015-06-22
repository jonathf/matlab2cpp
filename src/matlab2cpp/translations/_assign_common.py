from _arma_common import scalar_assign

def Assign(node):
    """
Assignment (General case)

Args:
    node (Assign): Current position in node-tree.

Returns:
    str : Translation of current node.

Examples:
    >>> print mc.qtranslate("a = b")
    a = b ;
    >>> print mc.qtranslate("a=[1,2]; b=[1;2]; a=b")
    int _a [] = {1, 2} ;
    a = ivec(_a, 2, false) ;
    int _b [] = {1, 2} ;
    b = irowvec(_b, 2, false) ;
    a = arma::trans(b) ;
    >>> print mc.qtranslate("a=[1,2,2,1]; b=[2,1;1,2]; a=b")
    int _a [] = {1, 2, 2, 1} ;
    a = ivec(_a, 4, false) ;
    int _b [] = {2, 1, 1, 2} ;
    b = imat(_b, 2, 2, false) ;
    a = arma::vectorise(b) ;
    """

    lhs, rhs = node
    if "TYPE" in (lhs.type, rhs.type) or lhs.type == rhs.type:
        return "%(0)s = %(1)s ;"

    if lhs.num and rhs.num:

        if (lhs.dim == 2 and rhs.dim == 1) or\
                (lhs.dim == 1 and rhs.dim == 2):
            out = "arma::trans(%(1)s)"
        else:
            out = "%(1)s"

        if lhs.dim == 0 and rhs.dim == 0:

            if lhs.mem >= rhs.mem:
                out = "(" + lhs.type + ") " + out
            else:
                node.warning("Type reduction from %s to %s" %\
                        (rhs.type, lhs.type))

        elif lhs.dim > 0 and rhs.dim == 0:
            return scalar_assign(node)

        elif lhs.dim in (1,2) and rhs.dim in (3, 4):
            out = "arma::vectorise(" + out + ")"

        elif lhs.dim > 0 and rhs.dim > 0:

            if lhs.mem >= rhs.mem:
                node.warning("Possible size incompatibility "+\
                        "%s and %s" % (lhs.type, rhs.type))
            else:
                node.warning("Type reduction and possible size "+\
                        "incompatible %s and %s" % (lhs.type, rhs.type))

        else:
            node.error("Types incompatible %s and %s" % (lhs.type, rhs.type))

    else:
        node.error("Types incompatible %s and %s" % (lhs.type, rhs.type))
        out = "%(1)s"

    out = "%(0)s = " + out + " ;"
    return out


if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()
