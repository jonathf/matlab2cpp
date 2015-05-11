
def configure_arg(node, index):

    if node.cls == "All":
        return "span::all", 1

    out = "%(" + str(index) + ")s"

    if node.dim == 0:
        out = out + "-1"
        dim = 0
    else:
        dim = 1

    if node.mem != 0 and node.dim != 0:
        node.auxiliary((node.dim, 0), convert=True)

    if node.dim == 2:
        out = out + ".t()"

    elif node.dim > 2:
        out = "vectorise(" + out + ")"

    return out, dim


def Assign(node):

    if node[1]["decomposed"]:
        return "%(0)s = %(1)s ;"

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

