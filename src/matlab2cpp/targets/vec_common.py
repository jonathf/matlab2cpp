
Var = "%(name)s"

def Assign(node):

    t0 = node[0].type()
    t1 = node[1].type()

    if t0 == "TYPE" and t1 != "TYPE":
        node[0].suggest(t1)

    if node[1]["decomposed"]:
        return "%(0)s << %(1)s ;"

    return "%(0)s = %(1)s ;"



def Get(node):

    assert len(node) == 1
    arg = node[0]

    nd = node.type(retd=True)
    ad = arg.type(retd=True)

    if arg["class"] == "All":
        return "%(name)s"

    elif not ad.numeric:
        return "%(name)s(%(0)s)"

    elif ad.dim == 0:
        node.type((0, nd.type))
        arg = str(arg)+"-1"

    elif ad.type != 0:
        arg = str(arg.auxillary("uvec", convert=True))

    else:
        arg = str(arg)

    out = "%(name)s(" + arg + ")"

    return out


def Set(node):

    sets, expr = node
    assert len(sets) == 1
    arg = sets[0]

    ed = expr.type(retd=True)
    ad = arg.type(retd=True)

    if ad.dim == 0: # constant
        arg = str(arg)+"-1"

    elif arg["class"] == "All":
        if ed.type == 0:
            return "%(name)s.fill(%(1)s)"
        return "%(name)s = %(1)s ;"

    elif not ad.numeric:
        return "%(name)s(%(0)s) = %(1)s"

    elif ad.type != 0:
        arg = str(arg.auxillary("uvec", convert=True))

    else:
        arg = str(arg)

    if ed.dim == 2:
        expr = str(expr) + ".t()"
    else:
        expr = str(expr)

    out = "%(name)s(" + arg + ") = " + expr + " ;"

    return out

