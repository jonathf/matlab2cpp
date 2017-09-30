import matlab2cpp as mc
from . import armadillo as arma

def Assign(node):
    """
Assignment (General case)

Args:
    node (Assign): Current position in node-tree.

Returns:
    str : Translation of current node.

Examples:
    >>> print(mc.qscript("a = b"))
    a = b ;
    >>> print(mc.qscript("a=[1,2]; b=[1;2]; a=b"))
    sword _a [] = {1, 2} ;
    a = irowvec(_a, 2, false) ;
    sword _b [] = {1, 2} ;
    b = ivec(_b, 2, false) ;
    a = arma::strans(b) ;
    >>> print(mc.qscript("a=[1,2,2,1]; b=[2,1;1,2]; a=b"))
    sword _a [] = {1, 2, 2, 1} ;
    a = irowvec(_a, 4, false) ;
    sword _b [] = {2, 1, 1, 2} ;
    b = arma::strans(imat(_b, 2, 2, false)) ;
    a = b ;
    """

    # left-hand-side and right-hand-side
    lhs, rhs = node

    # unknown datatype
    if "TYPE" in (lhs.type, rhs.type) or lhs.type == rhs.type:
        return "%(0)s = %(1)s ;"

    # numerical
    if lhs.num and rhs.num:
        
        # mismatch between colvec and rowvec, do transpose
        if (lhs.dim == 2 and rhs.dim == 1) or\
                (lhs.dim == 1 and rhs.dim == 2): #or lhs.mem != rhs.mem:
            #out = "arma::conv_to<" + lhs.type + ">::from(%(1)s)"
            out = "arma::strans(%(1)s)"
        else:
            out = "%(1)s"

        # both scalar
        if lhs.dim == 0 and rhs.dim == 0:

            if lhs.mem >= rhs.mem:
                out = "" + lhs.type + "(" + out + ")"
            else:
                node.warning("Type reduction from %s to %s" %\
                        (rhs.type, lhs.type))

        # fill array with scalar value
        elif lhs.dim > 0 and rhs.dim == 0:
            return arma.scalar_assign(node)

        # dimensions that works just fine
        #elif lhs.dim in (1,2) and rhs.dim in (3, 4):
        #    pass
        elif lhs.dim == 0 and rhs.dim > 0:
            out = lhs.type + "(arma::as_scalar(%(1)s))"

        # Added this elif to handle assignment of: complex type = non_complex type
        elif  lhs.mem > rhs.mem:
            if lhs.dim > 0 and rhs.dim > 0:
                out = "conv_to<" + lhs.type + ">::from(%(1)s)"
            elif lhs.dim == 0 and rhs.dim == 0:
                if lhs.mem == 4:
                    out = "" + lhs.type + "" + "(%(1)s)"

        # all the ways things are wrong
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
    import doctest
    doctest.testmod()
