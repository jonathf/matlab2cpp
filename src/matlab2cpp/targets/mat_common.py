
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

    # Single argument
    if len(node)==1:

        arg = node[0]
        ad = arg.type(retd=True)
        nd = node.type(retd=True)

        if arg["class"] == "All":
            node.type((1, nd.type))
            return "vectorise(%(name)s)"

        if not ad.numeric:
            return "%(name)s(%(0)s)"

        if ad.dim == 0:
            node.type((0, nd.type))
            arg = str(arg)+"-1"

        elif ad.type != 0:
            arg = str(arg.auxillary("uvec", convert=True))

        else:
            arg = str(arg)

        out = "%(name)s(" + arg + ")"
        return out


    # double argument
    elif len(node) == 2:

        arg0, arg1 = node
        a0 = arg0.type(retd=True)
        a1 = arg0.type(retd=True)
        nd = node.type(retd=True)
        name = node["name"]

        if arg0["class"] == "All":

            if arg1["class"] == "All":
                return "%(name)s"

            if a1.dim == 0:
                node.type((1, nd.type))
                arg1 = str(arg1) + "-1"

            elif a1.type != 0:
                arg1 = str(arg1.auxillary("uvec", convert=True))

            else:
                arg1 = str(arg1)

            if a1.dim == 0:
                return name + ".col(" + arg1 + ")"

            return name + ".cols(" + arg1 + ")"

        elif arg1["class"] == "All":

            if a0.dim == 0:
                node.type((2, nd.type))
                arg0 = str(arg0) + "-1"

            elif a0.type != 0:
                arg0 = str(arg0.auxillary("uvec", convert=True))

            else:
                arg0 = str(arg0)

            if a0.dim == 0:
                return name + ".row(" + arg1 + ")"

            return name + ".row(" + arg1 + ")"

        elif not a0.numeric or not a1.numeric:
            return "%(name)s(%(0)s, %(1)s)"

        if a0.dim == 0:
            arg0 = str(arg0)+"-1"
        elif a0.type != 0:
            arg0 = str(arg0.auxillary("uvec", convert=True))
        else:
            arg0 = str(arg0)

        if a1.dim == 0:
            arg1 = str(arg1)+"-1"
        elif a1.type != 0:
            arg1 = str(arg1.auxillary("uvec", convert=True))
        else:
            arg1 = str(arg1)

        if a0.dim == 0:
            if a1.dim == 0:
                node.type((0, nd.type))
            else:
                node.type((2, nd.type))
        else:
            node.type((1, nd.type))

        return name + "(" + arg0 + ", " + arg1 + ")"



def Set(node):

    sets, expr = node

    if len(sets) == 1:

        arg = sets[0]

        ed = expr.type(retd=True)
        ad = arg.type(retd=True)

        if ad.dim == 0:
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
            expr = "(" + str(expr) + ").t()"
        else:
            expr = str(expr)

        out = "%(name)s(" + arg + ") = " + expr + " ;"

        return out

    if len(sets) == 2:

        arg0, arg1 = sets

        ed = expr.type(retd=True)
        a0 = arg0.type(retd=True)
        a1 = arg1.type(retd=True)
        nd = node.type(retd=True)
        name = node["name"]

        if arg0["class"] == "All":

            if arg1["class"] == "All":
                if ed.type == 0:
                    return "%(name)s.fill(%(1)s)"
                return "%(name)s = %(1)s ;"

            if a1.dim == 0:
                node.type((1, nd.type))
                arg1 = str(arg1) + "-1"

            elif a1.type != 0:
                arg1 = str(arg1.auxillary("uvec", convert=True))

            else:
                arg1 = str(arg1)

            if a1.dim == 0:
                lhs = name + ".col(" + arg1 + ")"

            lhs = name + ".cols(" + arg1 + ")"

        elif arg1["class"] == "All":

            if a0.dim == 0:
                node.type((2, nd.type))
                arg0 = str(arg0) + "-1"

            elif a0.type != 0:
                arg0 = str(arg0.auxillary("uvec", convert=True))

            else:
                arg0 = str(arg0)

            if a0.dim == 0:
                lhs = name + ".row(" + arg1 + ")"

            lhs = name + ".row(" + arg1 + ")"

        elif not a0.numeric or not a1.numeric:
            return "%(name)s(%(0)s) = %(1)s ;"

        else:
            if a0.dim == 0:
                arg0 = str(arg0)+"-1"
            elif a0.type != 0:
                arg0 = str(arg0.auxillary("uvec", convert=True))
            else:
                arg0 = str(arg0)

            if a1.dim == 0:
                arg1 = str(arg1)+"-1"
            elif a1.type != 0:
                arg1 = str(arg1.auxillary("uvec", convert=True))
            else:
                arg1 = str(arg1)

            lhs = name + "(" + arg0 + ", " + arg1 + ")"

        rhs = str(expr)

        if a0.dim == 0:
            if a1.dim == 0:
                node.type((0, nd.type))
            else:
                node.type((2, nd.type))
                if ed.type == 1:
                    rhs = rhs + ".t()"
        else:
            node.type((1, nd.type))
            if ed.type == 2:
                rhs = rhs + ".t()"

        return lhs + " = " + rhs + " ;"
