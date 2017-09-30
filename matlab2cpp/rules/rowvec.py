from . import armadillo as arma

def Get(node):

    if len(node) != 1:

        if not len(node):
            node.error("Zero arguments in a rowvec call")
            return "%(name)s()"

        elif len(node) == 2 and node[0].cls == "Int" and node[0].value == "1":
            node_ = node[1]
            
        #special case hh = h0F(:,ones(1,M)) with h0F rowvec, and ones
        elif len(node) == 2 and node[0].name == "ones" or \
            node[1].name == "ones":
            out = "%(name)s("
            if node[0].name == "ones":
                out = out + "%(0)s-1, "
                #return "%(name)s(%(0)s-1, %(1)s)"
            else:
                out = out + "%(0)s, "
            if node[1].name == "ones":
                out = out + "%(1)s-1)"
                #return "%(name)s(%(0)s, %(1)s-1)"
            else:
                out = out + "%(1)s)"
            return out
            
        else:
            node.error("More than one arguments in a rowvec call")
            return "%(name)s(", "-1, ", "-1)"
    else:
        node_ = node[0]


    arg, dim = arma.configure_arg(node_, 0)

    if dim == -1:
        return "%(name)s(", "-1, ", "-1)"

    #if dim == 0:
    #    node.dim = 0

    # a(uvec array) or a(1:2:5)
    if (node[0].type == "uvec" and node[0].cls == "Var") or \
        node[0].cls == "Colon" and len(node[0]) == 3:
        return "arma::strans(%(name)s(" + arg + "))"

    return "%(name)s(" + arg + ")"


def Set(node):
    if len(node) != 1:

        if not len(node):
            node.error("Zero arguments in a rowvec call")
            return "%(name)s()"

        elif len(node) == 2 and node[0].cls == "Int" and node[0].value == "1":
            node_ = node[1]

        else:
            node.error("More than one arguments in a rowvec call")
            return "%(name)s(", "-1, ", "-1)"
    else:
        node_ = node[0]


    arg, dim = arma.configure_arg(node_, 0)

    #if dim == 0:
    #    node.dim = 0

    if dim == -1:
        return "%(name)s(", "-1, ", "-1)"

    return "%(name)s(" + arg + ")"
