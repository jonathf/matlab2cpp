

def Assign(node):

    lhs, rhs = node
    if "TYPE" in (lhs.type, rhs.type) or lhs.type == rhs.type:
        return "%(0)s = %(1)s ;"

    if lhs.num and rhs.num:

        if (lhs.dim == 2 and rhs.dim == 1) or\
                (lhs.dim == 1 and rhs.dim == 2):
            out = "%(1)s.t()"
        else:
            out = "%(1)s"

        if lhs.dim == 0 and rhs.dim == 0:

            if lhs.mem >= rhs.mem:
                out = "(" + lhs.type + ") " + out
            else:
                node.warning("Type reduction from %s to %s" %\
                        (rhs.type, lhs.type))

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



