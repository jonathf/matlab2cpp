
Var = "%(name)s"

def Assign(node):

    if node[1]["decomposed"]:
        return "%(0)s << %(1)s ;"

    return "%(0)s = %(1)s ;"


def Get(node):

    # Single argument

    if len(node) == 1:

        arg = node[0]

        if arg["class"] == "All":
            node.dim = 1
            return "vectorise(%(name)s)"

        if not arg.num:
            return "%(name)s(%(0)s)"

        if arg.dim == 0:
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


    # double argument
    elif len(node) == 2:

        arg0, arg1 = node
        name = node["name"]

        if arg0["class"] == "All":

            if arg1["class"] == "All":
                return "%(name)s"

            if arg1.dim == 0:
                node.dim = 1
                out1 = str(arg1) + "-1"

            elif arg1.mem != 0:
                out1 = str(arg1.auxillary((arg1.dim, 0), convert=True))

            else:
                out1 = str(arg1)

            if arg1.dim == 0:
                return name + ".col(" + out1 + ")"

            elif arg1.dim == 2:
                out1 = out1 + ".t()"

            elif arg1.dim > 2:
                out1 = "vectorise(" + out1 + ")"

            return name + ".cols(" + out1 + ")"

        elif arg1["class"] == "All":

            if arg0.dim == 0:
                node.dim = 2
                out0 = str(arg0) + "-1"

            elif arg0.mem != 0:
                out0 = str(arg0.auxillary((arg0.dim, 0), convert=True))

            else:
                out0 = str(arg0)

            if arg0.dim == 0:
                return name + ".row(" + out0 + ")"

            elif arg0.dim == 2:
                out0 = out0 + ".t()"

            elif arg0.dim > 2:
                out0 = "vectorise(" + out0 + ")"

            return name + ".rows(" + out0 + ")"

        elif not arg0.num or not arg1.num:
            return "%(name)s(%(0)s, %(1)s)"

        if arg0.dim == 0:
            if arg1.dim == 0:
                out0 = str(arg0)+"-1"
            else:
                out0 = "span("+str(arg0)+"-1)"

        elif arg0.mem != 0:
            out0 = str(arg0.auxillary((arg0.dim, 0), convert=True))

        else:
            out0 = str(arg0)

        if arg1.dim == 0:
            if arg0.dim == 0:
                out1 = str(arg1)+"-1"
            else:
                out1 = "span("+str(arg1)+"-1)"

        elif arg1.mem != 0:
            out1 = str(arg1.auxillary((arg1.dim, 0), convert=True))

        else:
            out1 = str(arg1)

        if arg0.dim == 0:
            if arg1.dim == 0:
                node.dim = 0
            else:
                node.dim = 2
        else:
            node.dim = 1

        if arg0.dim == 2:
            out0 = out0 + ".t()"
        elif arg0.dim > 2:
            out0 = "vectorise(" + out0 + ")"

        if arg1.dim == 2:
            out1 = out1 + ".t()"
        elif arg1.dim > 2:
            out1 = "vectorise(" + out1 + ")"

        return name + "(" + out0 + ", " + out1 + ")"



def Set(node):

    node.type = "umat"
    sets, expr = node

    if len(sets) == 1:

        arg = sets[0]

        if arg.dim == 0:
            out = str(arg)+"-1"

        elif arg["class"] == "All":
            if expr.dim == 0:
                return "%(name)s.fill(%(1)s)"
            return "%(name)s = %(1)s ;"

        elif not arg.num:
            return "%(name)s(%(0)s) = %(1)s ;"

        elif arg.mem != 0:
            out = str(arg.auxillary((arg.dim, 0), convert=True))

        else:
            out = str(arg)

        if arg.dim == 2:
            out = out + ".t()"
        elif arg.dim > 2:
            out = "vectorise(" + out + ")"

        if expr.dim == 2:
            expr = "(" + str(expr) + ").t()"
        else:
            expr = str(expr)

        out = "%(name)s(" + out + ") = " + expr + " ;"

        return out

    if len(sets) == 2:

        arg0, arg1 = sets

        name = node["name"]

        if arg0["class"] == "All":

            if arg1["class"] == "All":
                if expr.dim == 0:
                    return "%(name)s.fill(%(1)s)"
                return "%(name)s = %(1)s ;"

            if arg1.dim == 0:
                node.dim = 1
                out1 = str(arg1) + "-1"

            elif arg1.dim and arg1.mem:
                out1 = str(arg1.auxillary((arg1.dim, 0), convert=True))

            else:
                out1 = str(arg1)

            if arg1.dim == 2:
                out1 = out1 + ".t()"
            elif arg1.dim > 2:
                out1 = "vectorise(" + out1 + ")"

            if arg1.dim == 0:
                lhs = name + ".col(" + out1 + ")"
            else:
                lhs = name + ".cols(" + out1 + ")"

        elif arg1["class"] == "All":

            if arg0.dim == 0:
                node.dim = 2
                out0 = str(arg0) + "-1"

            elif arg0.mem != 0:
                out0 = str(arg0.auxillary((arg0.dim, 0), convert=True))

            else:
                out0 = str(arg0)

            if arg0.dim == 2:
                out0 = out0 + ".t()"
            elif arg0.dim > 2:
                out0 = "vectorise(" + out0 + ")"

            if arg0.dim == 0:
                lhs = name + ".row(" + out0 + ")"
            else:
                lhs = name + ".rows(" + out0 + ")"

        elif not arg0.num or not arg1.num:
            return "%(name)s(%(0)s) = %(1)s ;"

        else:
            if arg0.dim == 0:
                if arg1.dim == 0:
                    out0 = str(arg0)+"-1"
                else:
                    out0 = "span("+str(arg0)+"-1)"

            elif arg0.mem != 0:
                out0 = str(arg0.auxillary((arg0.dim, 0), convert=True))

            else:
                out0 = str(arg0)

            if arg1.dim == 0:
                if arg0.dim == 0:
                    out1 = str(arg1)+"-1"
                else:
                    out1 = "span("+str(arg1)+"-1)"

            elif arg1.mem != 0:
                out1 = str(arg1.auxillary((arg1.dim, 0), convert=True))

            else:
                out1 = str(arg1)

            if arg0.dim == 2:
                out0 = out0 + ".t()"
            elif arg0.dim > 2:
                out0 = "vectorise(" + out0 + ")"

            if arg1.dim == 2:
                out1 = out1 + ".t()"
            elif arg1.dim > 2:
                out1 = "vectorise(" + out1 + ")"

            lhs = name + "(" + out0 + ", " + out1 + ")"

        rhs = str(expr)

        if arg0.dim == 0:
            if arg1.dim == 0:
                node.dim = 0
            else:
                node.dim = 2
                if expr.dim == 1:
                    rhs = rhs + ".t()"
        else:
            node.dim = 1
            if expr.dim == 2:
                rhs = rhs + ".t()"

        return lhs + " = " + rhs + " ;"
