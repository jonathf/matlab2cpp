
Var = "%(name)s"

def Assign(node):

    if node[1]["decomposed"]:
        return "%(0)s << %(1)s ;"

    return "%(0)s = %(1)s ;"



def Get(node):

    assert len(node) == 1
    node.type = "urowvec"
    arg = node[0]

    if arg["class"] == "All":
        return "%(name)s"

    elif not arg.num:
        return "%(name)s(%(0)s)"

    elif arg.dim == 0:
        node.dim = 0
        out = str(arg)+"-1"

    elif arg.mem != 0:
        out = str(arg.auxillary((arg.dim, 0), convert=True))

    else:
        out = str(arg)

    if arg.dim == 2:
        out = out + ".t()"
    elif arg.dim > 2:
        out = "vectorise(" + out + ")"

    out = "%(name)s(" + out + ")"

    return out


def Set(node):

    sets, expr = node
    assert len(sets) == 1
    arg = sets[0]

    if expr.dim == 1:
        rhs = str(expr) + ".t()"
    else:
        rhs = str(expr)

    if arg["class"] == "All":
        if expr.dim == 0:
            return "%(name)s.fill(" + rhs + ") ;"
        return "%(name)s = " + rhs + " ;"

    elif arg.dim == 0: # constant
        out = str(arg)+"-1"

    elif not arg.num:
        return "%(name)s(%(0)s) = " + rhs + " ;"

    elif arg.mem != 0:
        out = str(arg.auxillary((arg.dim, 0), convert=True))

    else:
        out = str(arg)

    if arg.dim == 2:
        out = out + ".t()"
    elif arg.dim > 2:
        out = "vectorise(" + out + ")"

    out = "%(name)s(" + out + ") = " + rhs + " ;"

    return out

