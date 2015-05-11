from variables import *

def Get(node):

    # Single argument

    if len(node) == 1:

        arg = node[0]
        out = "%(0)s"

        if arg["class"] == "All":
            node.dim = 1
            return "vectorise(%(name)s)"

        if not arg.num:
            return "%(name)s(%(0)s)"

        if arg.dim == 0:
            node.dim = 0
            out = out + "-1"

        elif arg.mem != 0:
            arg.auxillary((arg.dim, 0), convert=True)

        if arg.dim > 2:
            out = "vectorise(" + out + ")"

        out = "vectorize(%(name)s(" + out + "))"
        return out


    # double argument
    elif len(node) == 2:

        arg0, arg1 = node
        out0, out1 = "%(0)s", "%(1)s"

        if not arg0.num or not arg1.num:
            return "%(name)s(%(0)s, %(1)s)"

        if arg0["class"] == "All":

            if arg1["class"] == "All":
                return "%(name)s"

            if arg1.dim == 0:
                node.dim = 1
                out1 = out1 + "-1"

            elif arg1.mem != 0:
                arg1.auxillary((arg1.dim, 0), convert=True)

            if arg1.dim == 0:
                return name + ".col(" + out1 + ")"

            elif arg1.dim == 2:
                out1 = out1 + ".t()"

            elif arg1.dim > 2:
                out1 = "vectorise(" + out1 + ")"

            return "%(name)s.cols(" + out1 + ")"

        elif arg1["class"] == "All":

            if arg0.dim == 0:
                node.dim = 2
                out0 = out0 + "-1"

            elif arg0.mem != 0:
                arg0.auxillary((arg0.dim, 0), convert=True)

            if arg0.dim == 0:
                return "%(name)s.row(" + out0 + ")"

            elif arg0.dim == 2:
                out0 = out0 + ".t()"

            elif arg0.dim > 2:
                out0 = "vectorise(" + out0 + ")"

            return name + ".rows(" + out0 + ")"

        if arg0.dim == 0:
            if arg1.dim == 0:
                out0 = out0+"-1"

        elif arg0.mem != 0:
            arg0.auxillary((arg0.dim, 0), convert=True)

        if arg1.dim == 0:
            if arg0.dim == 0:
                out1 = out1+"-1"

        elif arg1.mem != 0:
            arg1.auxillary((arg1.dim, 0), convert=True)

        if arg0.dim == 0:
            if arg1.dim == 0:
                node.dim = 0
            else:
                node.dim = 2
        else:
            if arg1.dim == 0:
                node.dim = 1
            else:
                node.dim = 3

        if arg0.dim == 2:
            out0 = out0 + ".t()"
        elif arg0.dim > 2:
            out0 = "vectorise(" + out0 + ")"

        if arg1.dim == 2:
            out1 = out1 + ".t()"
        elif arg1.dim > 2:
            out1 = "vectorise(" + out1 + ")"

        return "%(name)s(" + out0 + ", " + out1 + ")"


    # triple argument
    elif len(node) == 2:

        arg0, arg1 = node
        out0, out1 = "%(0)s", "%(1)s"

        if not arg0.num or not arg1.num:
            return "%(name)s(%(0)s, %(1)s)"

        if arg0["class"] == "All":

            if arg1["class"] == "All":
                return "%(name)s"

            if arg1.dim == 0:
                node.dim = 1
                out1 = out1 + "-1"

            elif arg1.mem != 0:
                arg1.auxillary((arg1.dim, 0), convert=True)

            if arg1.dim == 0:
                return name + ".col(" + out1 + ")"

            elif arg1.dim == 2:
                out1 = out1 + ".t()"

            elif arg1.dim > 2:
                out1 = "vectorise(" + out1 + ")"

            return "%(name)s.cols(" + out1 + ")"

        elif arg1["class"] == "All":

            if arg0.dim == 0:
                node.dim = 2
                out0 = out0 + "-1"

            elif arg0.mem != 0:
                arg0.auxillary((arg0.dim, 0), convert=True)

            if arg0.dim == 0:
                return "%(name)s.row(" + out0 + ")"

            elif arg0.dim == 2:
                out0 = out0 + ".t()"

            elif arg0.dim > 2:
                out0 = "vectorise(" + out0 + ")"

            return name + ".rows(" + out0 + ")"

        if arg0.dim == 0:
            if arg1.dim == 0:
                out0 = out0+"-1"

        elif arg0.mem != 0:
            arg0.auxillary((arg0.dim, 0), convert=True)

        if arg1.dim == 0:
            if arg0.dim == 0:
                out1 = out1+"-1"

        elif arg1.mem != 0:
            arg1.auxillary((arg1.dim, 0), convert=True)

        if arg0.dim == 0:
            if arg1.dim == 0:
                node.dim = 0
            else:
                node.dim = 2
        else:
            if arg1.dim == 0:
                node.dim = 1
            else:
                node.dim = 3

        if arg0.dim == 2:
            out0 = out0 + ".t()"
        elif arg0.dim > 2:
            out0 = "vectorise(" + out0 + ")"

        if arg1.dim == 2:
            out1 = out1 + ".t()"
        elif arg1.dim > 2:
            out1 = "vectorise(" + out1 + ")"

        return "%(name)s(" + out0 + ", " + out1 + ")"


def Assign(node):

    if node[1]["decomposed"]:
        return "%(0)s << %(1)s ;"

    if node[0].cls == "Var":
        return "%(0)s = %(1)s ;"

    node.type = "umat"

    sets, expr = node

    if (expr.dim == 2 and sets.dim == 1) or\
            (expr.dim == 1 and sets.dim == 2):
        rhs = "(%(1)s).t()"
    else:
        rhs = "%(1)s"


    out = "%(0)s = " + rhs + " ;"
    return out


def Set(node):

    if len(node) == 1:

        arg = node[0]
        out = "%(0)s"

        if arg.dim == 0:
            out = out + "-1"

        elif arg["class"] == "All":
            return "%(name)s"

        elif not arg.num:
            return "%(name)s(%(0)s)"

        elif arg.mem != 0:
            arg.auxillary((arg.dim, 0), convert=True)

        if arg.dim == 2:
            out = "(" + out + ").t()"
        elif arg.dim > 2:
            out = "vectorise(" + out + ")"

        out = "%(name)s(" + out + ")"

        return out

    if len(node) == 2:

        arg0, arg1 = node
        out0, out1 = "%(0)s", "%(1)s"

        if not arg0.num or not arg1.num:
            return "%(name)s(%(0)s)"

        if arg0["class"] == "All":

            if arg1["class"] == "All":
                return "%(name)s"


            if arg1.dim == 0:
                node.dim = 1
                out1 = out1 + "-1"

            elif arg1.dim and arg1.mem:
                arg1.auxillary((arg1.dim, 0), convert=True)

            if arg1.dim == 2:
                out1 = "(" + out1 + ").t()"
            elif arg1.dim > 2:
                out1 = "vectorise(" + out1 + ")"

            if arg1.dim == 0:
                lhs = "%(name)s.col(" + out1 + ")"
            else:
                lhs = "%(name)s.cols(" + out1 + ")"

        elif arg1["class"] == "All":

            if arg0.dim == 0:
                node.dim = 2
                out0 = out0 + "-1"

            elif arg0.mem != 0:
                arg0.auxillary((arg0.dim, 0), convert=True)

            if arg0.dim == 2:
                out0 = "(" + out0 + ").t()"
            elif arg0.dim > 2:
                out0 = "vectorise(" + out0 + ")"

            if arg0.dim == 0:
                lhs = name + ".row(" + out0 + ")"
            else:
                lhs = name + ".rows(" + out0 + ")"

        elif not arg0.num or not arg1.num:
            return "%(name)s(%(0)s, %(1)s)"

        else:
            if arg0.dim == 0:
                if arg1.dim == 0:
                    out0 = out0+"-1"
                else:
                    out0 = "span("+out0+"-1)"

            elif arg0.mem != 0:
                arg0.auxillary((arg0.dim, 0), convert=True)

            if arg1.dim == 0:
                if arg0.dim == 0:
                    out1 = out1+"-1"
                else:
                    out1 = "span("+out1+"-1)"

            elif arg1.mem != 0:
                arg1.auxillary((arg1.dim, 0), convert=True)

            if arg0.dim == 2:
                out0 = out0 + ".t()"
            elif arg0.dim > 2:
                out0 = "vectorise(" + out0 + ")"

            if arg1.dim == 2:
                out1 = out1 + ".t()"
            elif arg1.dim > 2:
                out1 = "vectorise(" + out1 + ")"

            lhs = "%(name)s(" + out0 + ", " + out1 + ")"

        if arg0.dim == 0:
            if arg1.dim == 0:
                node.dim = 0
            else:
                node.dim = 2
        else:
            node.dim = 1

        return lhs
